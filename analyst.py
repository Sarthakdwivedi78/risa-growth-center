"""Deterministic tools plus optional provider narration. No generated SQL or autonomous writes."""
import json, os, re
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import requests
import db
from analytics import snapshot

def fmt(v,kind='number'):
    if v is None or pd.isna(v): return 'unavailable'
    return f'{v:.1%}' if kind=='percent' else f'{v:,.2f}'
def answer(question,day='2025-04-20',context=None,path=None):
    explicit_date=re.search(r'\b(20\d{2}-\d{2}-\d{2})\b',question)
    if explicit_date:
        try: day=str(date.fromisoformat(explicit_date.group(1)))
        except ValueError: pass
    context=context or {}; q=question.lower(); s=snapshot(day,path=path); m=s['metrics']; perf=s['campaigns']; pending=None
    today=datetime.now(ZoneInfo('Asia/Kolkata')).date()
    if perf.empty:
        return {'text':f'No campaigns or outcomes are available as of {day}. Rates and recommendations are unavailable.','facts':m,'sources':['Campaigns.created_at and source reporting dates'],'context':context,'pending':None,'as_of':day,'mode':'deterministic'}
    selected=None
    for _,r in perf.iterrows():
        if re.search(r'\b'+re.escape(r.campaign_id.lower())+r'\b',q) or r.campaign.lower() in q: selected=r
    if selected is None and any(x in q for x in ['its ','that campaign','it?','this campaign','same campaign','its?']):
        rows=perf[perf.campaign_id==context.get('campaign_id')]
        if len(rows): selected=rows.iloc[0]
    if selected is not None: context['campaign_id']=selected.campaign_id
    refs=['Registrations.registration_id, person_id, campaign_id','Registration History: latest effective_at <= selected IST day','Check-ins: event_id, admitted + verified, distinct external person_id','Daily Marketing.activity_id, marketing_spend_inr (net credits)']
    text=''; facts={}
    if any(x in q for x in ['weather','profit','revenue','bank receipt','cash collected','gender','age breakdown','unique reach','caused','causal']):
        text='The dataset cannot answer this. It has no weather, ticket revenue, bank receipts, demographic ages/genders, cross-platform reach identities, or randomized causal outcomes. Campaign association does not establish incremental impact.'
    elif re.search(r'\b(set|change|update)\b.*\bbudget\b',q):
        amounts=re.findall(r'(?:to|inr|₹)\s*([\d,]+(?:\.\d+)?)',q)
        if selected is None or not amounts: text='Specify a campaign ID and amount, for example: Set C03 budget to INR 40000. I will prepare a confirmation before saving.'
        else:
            amount=float(amounts[-1].replace(',','')); pending={'type':'budget','campaign_id':selected.campaign_id,'amount':amount,'previous':None if pd.isna(selected.budget) else selected.budget}
            text=f'Proposed operational budget for {selected.campaign} ({selected.campaign_id}): INR {fmt(amount)}. Previous budget: {fmt(selected.budget)}. This does not change historical spend of INR {fmt(selected.spend)}. Confirm to save.'
    elif ('create' in q or 'add' in q) and 'task' in q:
        if selected is None: text='Specify a campaign ID so I can link the proposed task.'
        else:
            pending={'type':'task','campaign_id':selected.campaign_id,'title':f'Investigate {selected.campaign} conversion','description':f'Historical CPA INR {fmt(selected.cpa)} vs portfolio {fmt(m["cpa"])}. Audit form drop-off and test reminder treatment with holdout. Proposed work, not 2025 activity.','owner':selected.owner,'deadline':str(today+timedelta(days=7))}
            text=f'Proposed task for {selected.owner}: {pending["title"]}. Deadline {pending["deadline"]}. Confirm before saving.'
    elif 'experiment' in q and any(w in q for w in ['create','propose','generate','idea']):
        if selected is None:
            candidates=perf.dropna(subset=['cpa']).sort_values('cpa',ascending=False)
            selected=candidates.iloc[0] if len(candidates) else perf.iloc[0]
            context['campaign_id']=selected.campaign_id
        pending={'type':'experiment','campaign_id':selected.campaign_id,'name':f'{selected.campaign}: reminder holdout','hypothesis':'A consented itinerary reminder increases confirmed-to-attended rate by 5 percentage points.','audience':'Confirmed external registrants, randomized by person_id','metric':'Attendance percentage-point lift vs holdout','expected':5.0,'budget':5000.0,'start_date':str(date.today()),'end_date':str(date.today()+timedelta(days=14)),'notes':'Proposed future pilot. 50/50 holdout, one assignment per person. Minimum 200 per arm for directional review; power calculation needed before causal conclusion.'}
        text=f'Proposed experiment on {selected.campaign_id}: {pending["hypothesis"]} INR 5,000 cap. Historical attributed CPA is INR {fmt(selected.cpa)}. Expected lift is an assumption. Confirm to create.'
    elif 'task' in q:
        t=db.read('tasks',path); facts={'tasks':t.to_dict('records')}; text=f'{len(t)} tasks in the current database. '+('No tasks created yet.' if t.empty else t[['title','owner','status','deadline']].to_markdown(index=False))
        refs=['tasks: current operational records']
    elif 'experiment' in q:
        t=db.read('experiments',path); facts={'experiments':t.to_dict('records')}; text=f'{len(t)} experiments in the current database. '+('No experiment results recorded.' if t.empty else t[['name','metric','expected','actual','decision']].to_markdown(index=False)); refs=['experiments: current operational records']
    elif any(w in q for w in ['scale','stop','underperform','allocate','reallocat','recommend','investigate','improve','bottleneck','prioritize']):
        good=perf[(perf.attendees>=30)&(perf.spend>0)].sort_values('cpa')
        if good.empty:
            return {'text':'Insufficient verified attendance to recommend scaling or stopping by attendee cost. Collect outcomes or use an explicitly labelled pre-event registration pilot.','facts':m,'sources':refs,'context':context,'pending':None,'as_of':day,'mode':'deterministic'}
        best=good.iloc[0]; worst=good.iloc[-1]; target=selected if selected is not None else worst; context['campaign_id']=target.campaign_id
        text=f'{target.campaign} ({target.campaign_id}) generated {int(target.registrations)} registrations and {int(target.attendees)} attributed verified attendees from INR {fmt(target.spend)}: CPA INR {fmt(target.cpa)}, registration-to-attendance {fmt(target.reg_attendance,"percent")}. Portfolio CPA is INR {fmt(m["cpa"])}. {best.campaign} ({best.campaign_id}) is the lowest-CPA observed option: INR {fmt(best.spend)} / {int(best.attendees)} = INR {fmt(best.cpa)}. Propose a capped INR 10,000 next-cycle pilot there, implying {fmt(10000/best.cpa)} attendees only if historical average cost repeats. This is a scenario, not incremental causal evidence. Deprioritize expansion of {worst.campaign}; diagnose creative-to-form and reminder drop-off first. Use randomized mutually exclusive cohorts, minimum 200 per arm for directional review, and scale only if incremental CPA <= INR 120 with a positive confidence interval. Ask to create a task or propose an experiment for {target.campaign_id}.'
        facts={'investigated':target.to_dict(),'best':best.to_dict(),'worst':worst.to_dict()}
        if 'bottleneck' in q:
            losses={'identified people to registered people':m['identified_external_people']-s['registrations'].person_id.nunique(),'registered people to admitted registered people':s['registrations'].person_id.nunique()-m['registered_attendees']}
            stage=max(losses,key=losses.get)
            text=f'Largest measured person-count gap: {stage}, {losses[stage]} people. Reach-to-interest is unavailable because reach is not deduplicated. '+text
    elif 'trend' in q or 'weekly' in q or 'daily' in q:
        trend=s['trend'].copy(); trend.index=pd.to_datetime(trend.index)
        weekly=trend.resample('W-SUN').sum().tail(4); text='Last four observed weekly totals (week ends Sunday, Asia/Kolkata):\n'+weekly.to_markdown()+ '\nRegistration creation and first verified admission are separate event dates. Post-event flat counts do not imply live campaign failure.'; facts={'weekly':weekly.reset_index().astype(str).to_dict('records')}
    elif any(w in q for w in ['target','goal','achiev']):
        text=f'As of {day}: {m["attendees"]} / {s["targets"].get("unique_external_visitors_goal","unavailable")} distinct external visitors = {fmt(m["target_achievement"],"percent")}. Registrations {m["registrations"]} / {s["targets"].get("registration_goal","unavailable")}. Target version: {s["targets"].get("target_version","none")}. Approved budget INR {fmt(s["targets"].get("marketing_budget_inr"))}. Net spend INR {fmt(m["spend"])}.'; facts=s['targets']; refs+=['Targets.effective_at and target_version']
    elif selected is not None:
        text=f'{selected.campaign} ({selected.campaign_id}): {int(selected.registrations)} registrations, {int(selected.confirmed)} confirmed, {int(selected.attendees)} attributed attendees, net spend INR {fmt(selected.spend)}, CPR INR {fmt(selected.cpr)}, CPA INR {fmt(selected.cpa)}. First-touch cohort conversion {fmt(selected.conversion,"percent")}. Owner: {selected.owner}. Current operational budget: INR {fmt(selected.budget)}. Operational status: {selected.status}. Budget is not a source fact unless supplied by the user.'; facts=selected.to_dict(); refs+=['campaign_plan.budget, owner, status (current, not historical)']
    elif ('most' in q and 'registration' in q) or ('lowest' in q and ('cost' in q or 'cpr' in q or 'cpa' in q)) or ('worst' in q and 'conversion' in q):
        col='registrations' if 'most' in q else ('conversion' if 'worst' in q else ('cpa' if 'attendee' in q or 'cpa' in q else 'cpr'))
        candidates=perf.dropna(subset=[col]).sort_values(col,ascending=col!='registrations')
        if candidates.empty: return {'text':f'{col} is unavailable at this date: no eligible denominator.','facts':m,'sources':refs,'context':context,'pending':None,'as_of':day,'mode':'deterministic'}
        row=candidates.iloc[0]; context['campaign_id']=row.campaign_id; facts=row.to_dict()
        text=f'{row.campaign} ({row.campaign_id}): {col} = {fmt(row[col],"percent" if col=="conversion" else "number")}. {int(row.registrations)} registrations, {int(row.attendees)} attributed attendees, INR {fmt(row.spend)} net spend. Rates use matching observed cohorts and do not establish causal lift.'
    elif any(w in q for w in ['owner','budgets','campaign list','list campaigns']):
        fields=perf[['campaign_id','campaign','owner','budget','status','spend']].copy()
        text='Current operational campaign information (blank budget means not supplied):\n'+fields.to_markdown(index=False)+'\nSpend is historical through '+str(day)+'. Owners and allocations reflect current saved edits.'
        facts={'campaigns':fields.to_dict('records')}; refs+=['campaign_plan: current owner, budget and status']
    elif any(w in q for w in ['attendance','attend','confirmed','registration','cancel','conversion','spend','expenditure','people','funnel','budget','owner','campaign']):
        text=f'Historical snapshot {day} (Asia/Kolkata): {m["identified_external_people"]} external people; {m["registrations"]} registrations; {m["confirmed"]} confirmed; {m["cancelled"]} cancelled; {m["attendees"]} unique verified attendees. Confirmed-cohort attendance = {m["eligible_attendees"]}/{m["confirmed"]} = {fmt(m["attendance_rate"],"percent")}; registered-person attendance = {m["registered_attendees"]}/{m["registrations"]} = {fmt(m["registration_to_attendance"],"percent")}. {m["walk_ins"]} attendees have no registration and are excluded from those rates. Registration conversion = {fmt(m["registration_conversion"],"percent")}; confirmation = {fmt(m["confirmation_rate"],"percent")}. Net spend INR {fmt(m["spend"])}; CPR INR {fmt(m["cpr"])}; attributed CPA INR {fmt(m["cpa"])}. Anonymous CTR {fmt(m["ctr"],"percent")}; registrations/session {fmt(m["landing_conversion"],"percent")}; registrations/form-start event {fmt(m["start_conversion"],"percent")}. Ask about a campaign ID for its owner and operational budget.'; facts=m
    else:
        text='I cannot map that question reliably to the available analytics. Ask about a campaign ID, registrations, attendance, spend, targets, trends, tasks or experiments. Unavailable fields and causal effects will not be invented.'
    result={'text':text,'facts':facts,'sources':refs,'context':context,'pending':pending,'as_of':day,'mode':'deterministic'}
    return result

def apply_action(action,confirmed=False,path=None):
    if not confirmed: raise ValueError('Explicit confirmation required')
    a=dict(action); kind=a.pop('type')
    if kind=='budget':
        current=db.campaigns(path,True).set_index('campaign_id').loc[a['campaign_id'],'budget']; old=a.get('previous')
        if (pd.notna(current) and current!=old) or (pd.isna(current) and old is not None): raise ValueError('Budget changed since proposal. Ask again to refresh.')
        db.set_budget(a['campaign_id'],a['amount'],path)
    elif kind=='task': db.save_entity('tasks',{**a,'priority':'High','status':'To Do'},path)
    elif kind=='experiment': db.save_entity('experiments',{**a,'actual':None,'decision':'Pending'},path)
    else: raise ValueError('Unsupported action')

def narrate(question,result):
    """Optional model sees aggregate tool facts only; all actions remain deterministic."""
    provider=os.getenv('AI_PROVIDER','deterministic')
    if provider=='deterministic': return None
    prompt='Explain only the following current database tool result. Do not invent values. Clearly distinguish assumptions. Never claim to save changes. If unsupported, say unavailable. Question: '+question+'\n'+json.dumps({k:result[k] for k in ['text','facts','sources','as_of']},default=str)
    try:
        if provider=='gemini':
            key=os.getenv('GEMINI_API_KEY'); model=os.getenv('GEMINI_MODEL')
            if not key or not model: return 'Optional Gemini is not configured. Deterministic answer remains available.'
            r=requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'text':prompt}]}]},timeout=25); r.raise_for_status(); return r.json()['candidates'][0]['content']['parts'][0]['text']
        if provider=='openai_compatible':
            key=os.getenv('AI_API_KEY'); model=os.getenv('AI_MODEL')
            if not key or not model: return 'Optional provider is not configured. Deterministic answer remains available.'
            r=requests.post(os.getenv('AI_BASE_URL','https://api.openai.com/v1').rstrip('/')+'/chat/completions',headers={'Authorization':'Bearer '+key},json={'model':model,'messages':[{'role':'user','content':prompt}],'temperature':0},timeout=25); r.raise_for_status(); return r.json()['choices'][0]['message']['content']
        return 'Unknown provider. Using deterministic analytics.'
    except (requests.RequestException,KeyError,IndexError,ValueError): return 'Optional provider unavailable. The verified deterministic answer above is still usable.'

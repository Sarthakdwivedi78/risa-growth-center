import json, os, sqlite3
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import db, analytics, analyst

st.set_page_config(page_title='RISA Growth Center',page_icon='◈',layout='wide')
st.markdown('''<style>
.block-container{padding-top:4rem;max-width:1550px} h1{font-weight:750;letter-spacing:-1px} h2{letter-spacing:-.5px}
[data-testid="stMetric"]{background:white;border:1px solid #DFE7ED;border-radius:12px;padding:16px;min-height:115px}
[data-testid="stMetricLabel"]{color:#53677E} [data-testid="stSidebar"]{border-right:1px solid #DFE7ED}
.eyebrow{color:#177f72;font-size:12px;letter-spacing:2px;font-weight:700}.note{color:#63758A;font-size:14px}
</style>''',unsafe_allow_html=True)
try: db.initialize()
except Exception as e: st.error(f'Database initialization failed: {e}'); st.stop()
with st.sidebar:
    st.markdown('## ◈ RISA\n**GROWTH CENTER**')
    st.caption('CampusFest • Attendee Growth')
    page=st.radio('Workspace',['Overview','Growth Analytics','Campaign Management','Experimentation','Task Management','AI Growth Analyst','Data Management','Settings'],label_visibility='collapsed')
    st.divider()
    day=st.date_input('Historical as-of date',date(2025,4,20),min_value=date(2025,1,1),max_value=date(2030,12,31))
    st.caption('End of day • Asia/Kolkata')
    st.info('Fictional historical event\n12–13 April 2025\n\nOperational plans are proposals.')

st.markdown('<div class="eyebrow">RISA / GROWTH OPERATIONS</div>',unsafe_allow_html=True)
st.title(page)
st.caption(f'Historical results through {day:%d %b %Y} IST. Plans and tasks reflect current saved edits.')

def money(x): return 'Unavailable' if x is None or pd.isna(x) else f'₹{x:,.0f}'
def pct(x): return 'Unavailable' if x is None or pd.isna(x) else f'{x:.1%}'
def plot(fig):
    fig.update_layout(template='plotly_white',font=dict(family='Arial',color='#14263D'),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=15,r=15,t=40,b=15),colorway=['#177f72','#4775C5','#E6AA45','#9B6BA3'])
    st.plotly_chart(fig,width='stretch')
def run_save(fn):
    try: fn(); st.success('Saved to SQLite.'); st.rerun()
    except (ValueError,sqlite3.Error) as e: st.error(str(e))

if page in ['Overview','Growth Analytics']:
    allca=db.campaigns(include_deleted=True)
    f1,f2,f3=st.columns([2,2,1])
    chosen=f1.multiselect('Acquisition campaign',allca.campaign_id.tolist(),format_func=lambda k:allca.set_index('campaign_id').loc[k,'campaign_name'])
    channels=f2.multiselect('Channel',sorted(allca.channel.unique()))
    cohort=f3.checkbox('Acquisition cohort')
    start=st.date_input('Cohort first-seen / registration start',min(day,date(2025,3,1)),max_value=day) if cohort else None
    if cohort: st.caption('Includes identities first seen since the start, their registrations created since the start, and their subsequent admissions through the as-of date. Spend is the same date interval. Global targets are disabled.')
    with st.spinner('Calculating current database snapshot…'): s=analytics.snapshot(day,chosen,channels,start=start)
    m=s['metrics']; perf=s['campaigns']
    if chosen or channels: st.caption('People use fixed first-touch campaigns. Registrations and admissions use registration acquisition campaigns. Global registration conversion is unavailable for campaign filters; the campaign table uses a matched first-touch cohort.')
    cards=[('Identified external people',f'{m["identified_external_people"]:,}'),('Registrations',f'{m["registrations"]:,}'),('Confirmed',f'{m["confirmed"]:,}'),('Verified visitors',f'{m["attendees"]:,}'),('Cancelled',str(m['cancelled'])),('Registration conversion',pct(m['registration_conversion'])),('Confirmed-cohort attendance',pct(m['attendance_rate'])),('Net marketing spend',money(m['spend'])),('Cost / registration',money(m['cpr'])),('Cost / attributed attendee',money(m['cpa'])),('Visitor target achievement',pct(m['target_achievement'])),('Budget utilization',pct(m['budget_utilization']))]
    for i in range(0,len(cards),4):
        for col,(label,value) in zip(st.columns(4),cards[i:i+4]): col.metric(label,value)
    st.caption(f'{m["registered_attendees"]:,} registered visitors + {m["walk_ins"]:,} unregistered visitors. Eligible attendance denominator: distinct currently confirmed registrants; numerator: admitted members of that same cohort. All-visitor spend ratio: {money(m["all_visitor_cost"])}.')
    a,b=st.columns([1,1.4])
    with a:
        st.subheader('Observed funnel')
        plot(go.Figure(go.Funnel(y=['Identified external','Registrations','Confirmed','Registered attendees'],x=[m['identified_external_people'],m['registrations'],m['confirmed'],m['registered_attendees']],textinfo='value',marker=dict(color=['#98CFC4','#56B8A6','#248E7C','#145A50']))))
        st.caption(f'Identified interest actions: {m["identified_interest"]:,} people. Anonymous reported reach sums to {s["totals"]["reported_reach"]:,.0f} daily observations, not unique reach. Reach-to-person conversion is unavailable. Funnel stages are not necessarily nested after cancellations.')
    with b:
        st.subheader('Acquisition and first admission')
        if not s['trend'].empty: plot(px.line(s['trend'][['Registrations','Identified people','First admission']],labels={'value':'People / registrations','index':'IST date'}))
        else: st.info('No observations in this selection.')
    a,b=st.columns(2)
    with a:
        st.subheader('Campaign outcomes')
        plot(px.bar(perf,x='campaign',y=['registrations','attendees'],barmode='group'))
    with b:
        st.subheader('Spend and registrations')
        if len(perf): plot(px.scatter(perf,x='spend',y='registrations',size='attendees' if perf.attendees.max()>0 else None,hover_name='campaign',color='channel'))
        else: st.info('No campaigns exist at this historical cutoff.')
    st.subheader('Campaign performance')
    st.dataframe(perf,width='stretch',hide_index=True,column_config={'conversion':st.column_config.NumberColumn(format='percent'),'reg_attendance':st.column_config.NumberColumn(format='percent')})
    st.download_button('Download campaign report',perf.to_csv(index=False),'campaign_report.csv','text/csv')
    st.download_button('Download KPI snapshot',json.dumps({'metrics':m,'targets':s['targets'],'as_of':str(day),'definitions':'See README. Filtered cohorts are not comparable to event-wide goals.'},indent=2,default=str),'snapshot.json','application/json')
    if page=='Growth Analytics':
        a,b=st.columns(2)
        with a: st.subheader('Matched cohort conversion'); plot(px.bar(perf,x='campaign',y='conversion'))
        with b: st.subheader('Channel contribution'); plot(px.bar(perf.groupby('channel',as_index=False)[['spend','registrations','attendees']].sum(),x='channel',y='attendees'))
        if not s['filtered'] and s['targets']:
            target=pd.DataFrame({'Measure':['External people','Registrations','Visitors'],'Actual':[m['identified_external_people'],m['registrations'],m['attendees']],'Target':[s['targets']['identified_external_people_goal'],s['targets']['registration_goal'],s['targets']['unique_external_visitors_goal']]})
            st.subheader('Effective targets'); plot(px.bar(target,x='Measure',y=['Actual','Target'],barmode='group'))
        st.write({'Click-through rate':pct(m['ctr']),'Registrations / landing session':pct(m['landing_conversion']),'Registrations / form-start event':pct(m['start_conversion']),'Cancellation rate':pct(m['cancellation_rate']),'Confirmation rate':pct(m['confirmation_rate'])})
        st.caption('Session/start ratios compare anonymous event counts with registrations. They are aggregate efficiency ratios, not person-level causal conversion.')
        if not s['trend'].empty:
            daily=s['trend'].copy(); daily['Registration growth %']=daily.Registrations.pct_change().replace([float('inf'),-float('inf')],float('nan'))*100
            with st.expander('Daily growth and spend'): st.dataframe(daily,width='stretch')
            weekly=s['trend'].copy(); weekly.index=pd.to_datetime(weekly.index); weekly=weekly.resample('W-SUN').sum(); weekly['Registration growth %']=weekly.Registrations.pct_change().replace([float('inf'),-float('inf')],float('nan'))*100
            st.subheader('Weekly growth'); st.dataframe(weekly,width='stretch')
        st.subheader('Proposed next-edition scenario')
        a,b,c,d=st.columns(4); nr=a.number_input('Assumed registrations',0,100000,3600); rate=b.slider('Assumed registered show rate',0.,1.,.75); walk=c.number_input('Assumed walk-ins',0,10000,100); cap=d.number_input('Assumed total visitor capacity',1,100000,3200)
        f=analytics.forecast(s,rate,nr,walk,cap); st.metric('Projected visitors (assumption)',f['projected_visitors']); st.caption(f'Min(capacity, registrations × show rate + walk-ins). {pct(f["achievement"])} of the selected historical visitor goal, for context only. Venue capacity and funding require validation.')

elif page=='Campaign Management':
    s=analytics.snapshot(day); st.dataframe(s['campaigns'],width='stretch',hide_index=True)
    ca=db.campaigns(); keys=['New campaign']+ca.campaign_id.tolist(); choice=st.selectbox('Create or edit',keys)
    row={} if choice=='New campaign' else ca.set_index('campaign_id').loc[choice].to_dict()
    def val(k,default=''): return row.get(k,default) if pd.notna(row.get(k,default)) else default
    with st.form('campaign_form'):
        a,b=st.columns(2); name=a.text_input('Campaign name',val('campaign_name')); ch=b.text_input('Channel',val('channel','proposed'))
        audience=st.text_input('Target audience',val('target_audience')); objective=st.text_area('Objective',val('objective'))
        a,b,c=st.columns(3); owner=a.text_input('Owner',val('owner','Unassigned')); budget=b.number_input('Operational budget (INR)',min_value=0.,value=float(val('budget',0.))); status=c.selectbox('Status',['Proposed','Active','Paused','Completed','Historical'],index=['Proposed','Active','Paused','Completed','Historical'].index(val('status','Proposed')))
        a,b=st.columns(2); sd=a.date_input('Start',pd.Timestamp(val('planned_start_at',str(date.today()))).date()); ed=b.date_input('End',pd.Timestamp(val('planned_end_at',str(date.today()+timedelta(days=28)))).date()); notes=st.text_area('Plan notes',val('notes'))
        st.caption('Source workbooks remain unchanged. Campaign budget is a new operational allocation; historical campaign budgets were not supplied. Saving 0 records a deliberate zero.')
        if st.form_submit_button('Save campaign',type='primary'):
            import uuid
            key=choice if choice!='New campaign' else 'P-'+uuid.uuid4().hex[:8]
            run_save(lambda:db.save_campaign(dict(campaign_id=key,campaign_name=name,channel=ch,target_audience=audience,objective=objective,owner=owner,owner_name=owner,owner_id=val('owner_id','USER'),created_at=val('created_at',datetime.now(ZoneInfo('Asia/Kolkata')).isoformat()),planned_start_at=sd.isoformat()+'T00:00:00+05:30',planned_end_at=ed.isoformat()+'T23:59:59+05:30',budget=budget,status=status,notes=notes)))
    if choice!='New campaign':
        yes=st.checkbox('Confirm deletion from active management. Retain historical facts and linked tasks.')
        if st.button('Delete / archive campaign',disabled=not yes): run_save(lambda:db.delete_campaign(choice,yes))

elif page=='Task Management':
    tasks=db.read('tasks'); ca=db.campaigns(); statuses=['To Do','In Progress','Blocked','Completed']; today=datetime.now(ZoneInfo('Asia/Kolkata')).date()
    st.caption('Current execution board. Tasks are proposed work, separate from 2025 event observations.')
    for col,status in zip(st.columns(4),statuses):
        with col:
            subset=tasks[tasks.status==status]; st.subheader(f'{status} ({len(subset)})')
            for _,t in subset.iterrows():
                with st.container(border=True):
                    st.markdown('**'+t.title+'**'); st.caption(f'{t.owner} · {t.priority} · {t.deadline}')
                    if t.deadline and date.fromisoformat(t.deadline)<today and status!='Completed': st.error('Overdue')
                    st.write(t.description)
    choice=st.selectbox('Create or edit task',['New task']+tasks.id.tolist()); v={} if choice=='New task' else tasks.set_index('id').loc[choice].to_dict()
    with st.form('task'):
        title=st.text_input('Title',v.get('title','')); desc=st.text_area('Description',v.get('description','')); a,b,c=st.columns(3)
        owner=a.text_input('Assignee',v.get('owner','Unassigned')); priority=b.selectbox('Priority',['High','Medium','Low'],index=['High','Medium','Low'].index(v.get('priority','Medium'))); status=c.selectbox('Task status',statuses,index=statuses.index(v.get('status','To Do')))
        deadline=st.date_input('Deadline',date.fromisoformat(v.get('deadline',str(today+timedelta(days=7))))); links=['']+db.campaigns(include_deleted=True).campaign_id.tolist(); campaign=st.selectbox('Linked campaign',links,index=links.index(v.get('campaign_id') or ''))
        if st.form_submit_button('Save task',type='primary'): run_save(lambda:db.save_entity('tasks',dict(id=None if choice=='New task' else choice,title=title,description=desc,owner=owner,priority=priority,status=status,deadline=str(deadline),campaign_id=campaign or None)))

elif page=='Experimentation':
    ex=db.read('experiments'); st.caption('Proposed tests and manually recorded results. No simulated experiment is presented as observed history.')
    a,b,c=st.columns(3); a.metric('Experiments',len(ex)); b.metric('Scale decisions',int((ex.decision=='Scale').sum())); c.metric('Allocated test budget',money(ex.budget.sum()))
    st.dataframe(ex,width='stretch',hide_index=True)
    if len(ex): plot(px.bar(ex,x='name',y=['expected','actual'],barmode='group',title='Expected vs actual (compare only identical metrics)'))
    choice=st.selectbox('Create or edit experiment',['New experiment']+ex.id.tolist()); v={} if choice=='New experiment' else ex.set_index('id').loc[choice].to_dict()
    with st.form('experiment'):
        name=st.text_input('Experiment name',v.get('name','')); hypothesis=st.text_area('Hypothesis',v.get('hypothesis','')); audience=st.text_input('Target audience',v.get('audience',''))
        links=['']+db.campaigns(include_deleted=True).campaign_id.tolist(); campaign=st.selectbox('Campaign',links,index=links.index(v.get('campaign_id') or '')); metric=st.text_input('Success metric (include unit)',v.get('metric','Incremental verified attendees'))
        a,b,c=st.columns(3); expected=a.number_input('Expected result',value=float(v.get('expected',0))); budget=b.number_input('Experiment budget INR',min_value=0.,value=float(v.get('budget',0))); has_actual=c.checkbox('Actual result available',value=pd.notna(v.get('actual')))
        actual=st.number_input('Actual result',value=float(v.get('actual') or 0)) if has_actual else None
        a,b=st.columns(2); sd=a.date_input('Start date',date.fromisoformat(v.get('start_date',str(date.today())))); ed=b.date_input('End date',date.fromisoformat(v.get('end_date',str(date.today()+timedelta(days=14)))))
        decisions=['Pending','Scale','Iterate','Stop']; decision=st.selectbox('Decision',decisions,index=decisions.index(v.get('decision','Pending'))); notes=st.text_area('Design, thresholds, risks and evidence',v.get('notes',''))
        if st.form_submit_button('Save experiment',type='primary'): run_save(lambda:db.save_entity('experiments',dict(id=None if choice=='New experiment' else choice,name=name,hypothesis=hypothesis,audience=audience,campaign_id=campaign or None,metric=metric,expected=expected,budget=budget,start_date=str(sd),end_date=str(ed),actual=actual,decision=decision,notes=notes)))

elif page=='AI Growth Analyst':
    st.subheader('RISA AI GROWTH ANALYST')
    st.caption('Fresh database queries on every question. Deterministic analytics work without an API key. The optional provider explains the same aggregate evidence.')
    st.info('Try: Which campaign has the lowest cost per attendee? · Investigate C03 · What is its budget? · Set C03 budget to INR 40000 · Create a task for C03')
    if 'chat' not in st.session_state: st.session_state.chat=[]
    if st.button('Clear conversation'): st.session_state.chat=[]; st.session_state.context={}; st.session_state.pop('pending',None); st.rerun()
    for msg in st.session_state.chat:
        with st.chat_message(msg['role']): st.markdown(msg['text'])
    question=st.chat_input('Ask about performance or propose an action…')
    if question:
        st.session_state.chat.append({'role':'user','text':question})
        with st.chat_message('user'): st.write(question)
        with st.spinner('Reading the current database…'): result=analyst.answer(question,str(day),st.session_state.get('context',{})); extra=analyst.narrate(question,result)
        text=result['text']+'\n\n**Evidence:** '+ '; '.join(result['sources'])
        if extra: text+='\n\n**Optional model explanation (verify against evidence above):**\n'+extra
        st.session_state.chat.append({'role':'assistant','text':text}); st.session_state.context=result['context']; st.session_state.pending=result['pending']
        with st.chat_message('assistant'): st.markdown(text)
    if st.session_state.get('pending'):
        st.warning('Proposed action. Nothing has been changed.'); st.json(st.session_state.pending)
        a,b=st.columns(2)
        if a.button('Confirm and save',type='primary'):
            try:
                analyst.apply_action(st.session_state.pending,True); st.session_state.pending=None; st.session_state.chat.append({'role':'assistant','text':'Confirmed action saved. Ask a follow-up to read the updated database.'}); st.rerun()
            except (ValueError,sqlite3.Error) as e: st.error(str(e))
        if b.button('Cancel proposal'): st.session_state.pending=None; st.rerun()

elif page=='Data Management':
    st.subheader('Source data and working database')
    st.caption('Original workbooks are immutable copies. Working database changes are logged and do not overwrite source files.')
    table=st.selectbox('Inspect table',list(db.TABLES.values())+['campaign_plan','tasks','experiments','audit_log']); frame=db.read(table); st.dataframe(frame,width='stretch',hide_index=True); st.download_button('Export this table',frame.to_csv(index=False),table+'.csv','text/csv')
    with st.expander('Append a dated registration status'):
        st.caption('An explicit working-data correction. Earlier snapshots remain unchanged. No modification is written into the source workbook.')
        with st.form('status'):
            reg=st.text_input('Registration ID'); status=st.selectbox('New registration status',['confirmed','cancelled','waitlisted','interested']); effective=st.text_input('Effective IST timestamp','2025-04-20T23:00:00+05:30')
            confirm=st.checkbox('Confirm this working-data correction')
            if st.form_submit_button('Append status',disabled=not confirm): run_save(lambda:db.append_status(reg,status,effective))
    audit=db.ROOT/'reports/data_audit.md'
    if audit.exists():
        with st.expander('Data quality report'): st.markdown(audit.read_text(encoding='utf8'))
    st.download_button('Download original attendee workbook',(db.ROOT/'source/Attendee Dataset.xlsx').read_bytes(),'Attendee Dataset.xlsx')
    with db.connect() as con:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.db',delete=False) as f: backup_name=f.name
        dest=sqlite3.connect(backup_name); con.backup(dest); dest.close(); backup=Path(backup_name).read_bytes(); Path(backup_name).unlink()
    st.download_button('Download consistent database backup',backup,'risa-backup.db','application/octet-stream')

elif page=='Settings':
    st.subheader('Runtime and calculation settings')
    st.write({'Reporting timezone':'Asia/Kolkata','Currency':'INR','AI provider':os.getenv('AI_PROVIDER','deterministic'),'Source period':'15 Jan–20 Apr 2025','Event':'12–13 Apr 2025 (fictional)'})
    st.markdown('Configure optional AI using server environment variables in `.env.example`. Keys stay on the server. The app does not need a paid API. Provider calls send only aggregate analytics, not person records. Model output cannot write to the database.')
    st.markdown('**Storage:** SQLite persists across local app restarts. Download backups before moving hosts. Streamlit Community Cloud does not guarantee local-file persistence; durable hosted use needs persistent storage or a database adapter. This local demonstration has no authentication or multi-tenant isolation.')
    st.markdown('**Missing source fields:** campaign allocation budgets, venue capacity, unique cross-day reach, student college/age, experiment assignments, and ticket revenue. Missing values are unavailable, not zero. Newly entered plan budgets are explicitly operational.')
    st.link_button('Streamlit deployment documentation','https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy')

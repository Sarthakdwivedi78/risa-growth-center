"""Snapshot analytics. Source times interpreted in Asia/Kolkata, never host time."""
import pandas as pd
import numpy as np
import db

def ratio(n,d): return float(n/d) if d and pd.notna(d) else None
def dates(s): return pd.to_datetime(s,utc=True,format='mixed').dt.tz_convert('Asia/Kolkata')
def cutoff(day): return pd.Timestamp(str(day)[:10],tz='Asia/Kolkata')+pd.Timedelta(days=1)
def snapshot(day='2025-04-20',campaign_ids=None,channel=None,path=None,start=None):
    end=cutoff(day); begin=pd.Timestamp(str(start)[:10],tz='Asia/Kolkata') if start else pd.Timestamp('1900-01-01',tz='Asia/Kolkata')
    p=db.read('people',path).drop_duplicates('person_id'); p=p[(p.person_type=='external')&(dates(p.first_seen_at)<end)]
    r=db.read('registrations',path).drop_duplicates('registration_id'); r=r[(dates(r.registered_at)<end)&r.person_id.isin(p.person_id)]
    h=db.read('registration_history',path).drop_duplicates('history_id'); h=h[dates(h.effective_at)<end].copy(); h['_t']=dates(h.effective_at)
    h=h.sort_values(['_t','history_id']).drop_duplicates('registration_id',keep='last')
    r=r.merge(h[['registration_id','status']],on='registration_id',how='left'); r.status=r.status.fillna('unknown')
    c=db.read('checkins',path).drop_duplicates('event_id'); c=c[(dates(c.occurred_at)<end)&c.person_id.isin(p.person_id)&(c.result=='admitted')&(c.verification=='verified')]
    # Acquisition attribution comes only from registration, never the check-in or engagement campaign.
    c=c.drop(columns=['campaign_id','campaign_name','registration_id']).merge(r[['person_id','campaign_id','registration_id']],on='person_id',how='left')
    # Multiple registrations for one person: earliest eligible registration owns attribution.
    if r.person_id.duplicated().any():
        rr=r.sort_values(['registered_at','registration_id']).drop_duplicates('person_id')
        c=c.drop(columns=['campaign_id','registration_id']).drop_duplicates('event_id').merge(rr[['person_id','campaign_id','registration_id']],on='person_id',how='left')
    d=db.read('daily',path).drop_duplicates('activity_id'); d=d[(dates(d.activity_date)<end)&(dates(d.activity_date)>=begin)]
    ca=db.campaigns(path,include_deleted=True); ca=ca[dates(ca.created_at)<end]
    ids=set(ca.campaign_id)
    if channel: ids &=set(ca[ca.channel.isin(channel)].campaign_id)
    if campaign_ids: ids &=set(campaign_ids)
    filtered=bool(campaign_ids or channel)
    if filtered:
        p=p[p.first_campaign_id.isin(ids)]; r=r[r.campaign_id.isin(ids)]; c=c[c.campaign_id.isin(ids)]
    d=d[d.campaign_id.isin(ids)]
    ca=ca[ca.campaign_id.isin(ids)]
    # A start date defines an acquisition cohort. Attendance follows those registrations to as-of.
    if start:
        p=p[dates(p.first_seen_at)>=begin]; r=r[(dates(r.registered_at)>=begin)&r.person_id.isin(p.person_id)]
        c=c[c.person_id.isin(r.person_id)]
    admitted=set(c.person_id); reg_people=set(r.person_id)
    eligible=r[r.status=='confirmed']; eligible_people=set(eligible.person_id)
    attendance_eligible=len(admitted&eligible_people)
    spend=float(d.marketing_spend_inr.sum()); totals=d[['impressions','clicks','reported_reach','landing_page_sessions','registration_starts']].sum()
    registered_admitted=len(admitted&reg_people)
    target=db.read('targets',path); target=target[dates(target.effective_at)<end].sort_values('effective_at'); target=target.iloc[-1].to_dict() if len(target) else {}
    metrics={'identified_external_people':len(p),'registrations':len(r),'confirmed':len(eligible),'cancelled':int((r.status=='cancelled').sum()),'waitlisted':int((r.status=='waitlisted').sum()),'unknown_status':int((r.status=='unknown').sum()),'attendees':len(admitted),'registered_attendees':registered_admitted,'eligible_attendees':attendance_eligible,'walk_ins':len(admitted-reg_people),'spend':spend,'registration_conversion':ratio(r.person_id.nunique(),len(p)) if not filtered else None,'confirmation_rate':ratio(len(eligible),len(r)),'attendance_rate':ratio(attendance_eligible,len(eligible_people)),'registration_to_attendance':ratio(registered_admitted,len(reg_people)),'cancellation_rate':ratio((r.status=='cancelled').sum(),len(r)),'cpr':ratio(spend,len(r)),'cpa':ratio(spend,registered_admitted),'all_visitor_cost':ratio(spend,len(admitted)),'ctr':ratio(totals.clicks,totals.impressions),'landing_conversion':ratio(len(r),totals.landing_page_sessions),'start_conversion':ratio(len(r),totals.registration_starts),'target_achievement':ratio(len(admitted),target.get('unique_external_visitors_goal')) if not filtered and not start else None,'budget_utilization':ratio(spend,target.get('marketing_budget_inr')) if not filtered and not start else None}
    rows=[]
    for _,x in ca.iterrows():
        cr=r[r.campaign_id==x.campaign_id]; cp=p[p.first_campaign_id==x.campaign_id]; cd=d[d.campaign_id==x.campaign_id]; cc=c[c.campaign_id==x.campaign_id]; s=float(cd.marketing_spend_inr.sum()); a=cc.person_id.nunique()
        matched=cr[cr.person_id.isin(cp.person_id)].person_id.nunique()
        rows.append(dict(campaign_id=x.campaign_id,campaign=x.campaign_name,channel=x.channel,owner=x.owner,budget=x.budget,status=x.status,people=len(cp),registrations=len(cr),confirmed=int((cr.status=='confirmed').sum()),attendees=a,spend=s,cpr=ratio(s,len(cr)),cpa=ratio(s,a),conversion=ratio(matched,len(cp)),reg_attendance=ratio(a,cr.person_id.nunique()),budget_utilization=ratio(s,x.budget),deleted=x.deleted))
    perf=pd.DataFrame(rows,columns=['campaign_id','campaign','channel','owner','budget','status','people','registrations','confirmed','attendees','spend','cpr','cpa','conversion','reg_attendance','budget_utilization','deleted'])
    perf['performance']=np.where(perf.cpa.isna(),'No outcomes',np.where(perf.cpa>metrics['cpa'] if metrics['cpa'] else False,'Review','Efficient'))
    def daily(frame,col,key):
        if frame.empty:return pd.Series(dtype='int64')
        return frame.assign(date=dates(frame[col]).dt.date).groupby('date')[key].nunique()
    trend=pd.concat([daily(r,'registered_at','registration_id').rename('Registrations'),daily(c.sort_values('occurred_at').drop_duplicates('person_id'),'occurred_at','person_id').rename('First admission'),daily(p,'first_seen_at','person_id').rename('Identified people'),d.assign(date=dates(d.activity_date).dt.date).groupby('date').marketing_spend_inr.sum().rename('Spend')],axis=1).fillna(0).sort_index()
    engagement=db.read('interactions',path); engagement=engagement[(dates(engagement.occurred_at)<end)&engagement.person_id.isin(p.person_id)].drop_duplicates('interaction_id')
    interests=engagement[engagement.event_type.isin(['page_visit','brochure_download','registration_start','event_question_submitted'])].person_id.nunique()
    metrics['identified_interest']=int(interests)
    interested=set(engagement[engagement.event_type.isin(['page_visit','brochure_download','registration_start','event_question_submitted'])].person_id)
    metrics['interest_to_registration']=ratio(len(interested&reg_people),len(interested))
    return {'metrics':metrics,'campaigns':perf,'targets':target,'totals':totals.to_dict(),'trend':trend,'people':p,'registrations':r,'admissions':c,'engagement':engagement,'as_of':str(day),'filtered':filtered or bool(start)}

def forecast(s,conversion=.75,registrations=3600,walk_ins=100,capacity=3200):
    """Explicit scenario, never a claim of future observation or fitted causal model."""
    visitors=min(capacity,round(registrations*conversion+walk_ins))
    return {'projected_visitors':visitors,'registrations_assumed':registrations,'show_rate_assumed':conversion,'walk_ins_assumed':walk_ins,'capacity_assumed':capacity,'achievement':ratio(visitors,s['targets'].get('unique_external_visitors_goal'))}

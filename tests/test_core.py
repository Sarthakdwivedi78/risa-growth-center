import sys, shutil, sqlite3
from pathlib import Path
import pandas as pd
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import db, analytics, analyst

@pytest.fixture
def database(tmp_path):
    db.initialize(); p=tmp_path/'test.db'
    with db.connect() as src,sqlite3.connect(p) as dest: src.backup(dest)
    dest.close()
    return p

def test_baseline(database):
    s=analytics.snapshot(path=database); m=s['metrics']
    assert {k:m[k] for k in ['identified_external_people','registrations','confirmed','cancelled','attendees','registered_attendees','walk_ins','spend']}==dict(identified_external_people=3625,registrations=2800,confirmed=2500,cancelled=183,attendees=2050,registered_attendees=1925,walk_ins=125,spend=274000)
    assert m['registration_conversion']==pytest.approx(2800/3625)
    assert m['cpr']==pytest.approx(274000/2800)
    assert m['cpa']==pytest.approx(274000/1925)
    assert m['target_achievement']==pytest.approx(2050/2200)
    assert s['campaigns'].attendees.sum()==1925
    assert s['campaigns'].registrations.sum()==2800

@pytest.mark.parametrize('day',['2025-01-14','2025-02-15','2025-03-14','2025-03-15','2025-04-11','2025-04-12','2025-04-13','2025-04-20'])
def test_historical_sql_oracle(database,day):
    s=analytics.snapshot(day,path=database); end=day+'T23:59:59+05:30'
    with db.connect(database) as c:
        count=c.execute('''WITH ranked AS (SELECT registration_id,status,ROW_NUMBER() OVER(PARTITION BY registration_id ORDER BY effective_at DESC,history_id DESC) rn FROM registration_history WHERE effective_at<=?) SELECT COUNT(*) FROM registrations r JOIN people p USING(person_id) JOIN ranked h USING(registration_id) WHERE h.rn=1 AND h.status='confirmed' AND p.person_type='external' AND r.registered_at<=? AND p.first_seen_at<=?''',(end,end,end)).fetchone()[0]
        actual=c.execute("SELECT COUNT(DISTINCT c.person_id) FROM checkins c JOIN people p USING(person_id) WHERE c.occurred_at<=? AND c.result='admitted' AND c.verification='verified' AND p.person_type='external' AND p.first_seen_at<=?",(end,end)).fetchone()[0]
    assert s['metrics']['confirmed']==count
    assert s['metrics']['attendees']==actual
    if day<'2025-04-12': assert actual==0
    if day>='2025-03-15': assert s['targets']['marketing_budget_inr']==300000
    elif day>='2025-01-15': assert s['targets']['marketing_budget_inr']==240000

def test_duplicate_imports_and_credits(database):
    assert len(db.read('daily',database))==481
    assert len(db.read('registration_history',database))==5907
    assert len(db.read('checkins',database))==3370
    d=db.read('daily',database); assert d[d.marketing_spend_inr<0].marketing_spend_inr.sum()==-6500
    with db.connect(database) as c:
        with pytest.raises(sqlite3.IntegrityError): c.execute('INSERT INTO daily SELECT * FROM daily LIMIT 1')

def test_filters_empty_and_attribution(database):
    s=analytics.snapshot(campaign_ids=['C05'],path=database)
    assert s['metrics']['attendees']==275 and s['metrics']['spend']==19000
    assert s['metrics']['target_achievement'] is None
    assert analytics.ratio(1,0) is None
    assert analytics.snapshot('2025-01-01',path=database)['metrics']['cpr'] is None
    with db.connect(database) as c: c.execute("UPDATE checkins SET campaign_id='C02' WHERE campaign_id='C05'")
    assert analytics.snapshot(campaign_ids=['C05'],path=database)['metrics']['attendees']==275

def test_campaign_crud(database):
    v=dict(campaign_id='NEW',campaign_name='Proposed pilot',channel='referrals',target_audience='Students',objective='Test',owner='Owner',owner_name='Owner',owner_id='USER',created_at='2025-01-01T00:00:00+05:30',planned_start_at='2025-02-01',planned_end_at='2025-03-01',budget=10000,status='Proposed')
    db.save_campaign(v,database); v['budget']=12000; v['campaign_name']='Updated pilot'; db.save_campaign(v,database)
    assert db.campaigns(database).set_index('campaign_id').loc['NEW','budget']==12000
    with pytest.raises(ValueError): db.delete_campaign('NEW',path=database)
    db.delete_campaign('NEW',True,database); assert 'NEW' not in set(db.campaigns(database).campaign_id)
    assert 'NEW' in set(db.campaigns(database,True).campaign_id)
    with pytest.raises(ValueError): db.set_budget('C01',-1,database)

def test_tasks_experiments(database):
    task=dict(title='Pilot',description='Test',owner='Meera',priority='High',deadline='2027-01-01',status='To Do',campaign_id='C01')
    key=db.save_entity('tasks',task,database); task.update(id=key,status='Completed'); db.save_entity('tasks',task,database)
    assert db.read('tasks',database).set_index('id').loc[key,'status']=='Completed'
    exp=dict(name='Pilot',hypothesis='Lift',audience='Students',campaign_id='C01',metric='attendees',expected=20,budget=1000,start_date='2027-01-01',end_date='2027-01-10',actual=None,decision='Pending',notes='Proposed')
    key=db.save_entity('experiments',exp,database); exp.update(id=key,actual=25,decision='Scale'); db.save_entity('experiments',exp,database)
    assert db.read('experiments',database).set_index('id').loc[key,'actual']==25

def test_status_update_no_hindsight(database):
    before=analytics.snapshot('2025-04-13',path=database); reg=before['registrations'].query("status=='confirmed'").iloc[0].registration_id
    old=analytics.snapshot(path=database)['metrics']['confirmed']; db.append_status(reg,'cancelled','2025-04-20T23:00:00+05:30',database)
    assert analytics.snapshot(path=database)['metrics']['confirmed']==old-1
    assert analytics.snapshot('2025-04-13',path=database)['metrics']['confirmed']==before['metrics']['confirmed']

def test_confirmed_workflow_and_fresh_followup(database):
    r=analyst.answer('Investigate C03',path=database); assert r['facts']['investigated']['campaign_id']=='C03'
    proposal=analyst.answer('Set its budget to INR 40000',context=r['context'],path=database)
    with pytest.raises(ValueError): analyst.apply_action(proposal['pending'],path=database)
    analyst.apply_action(proposal['pending'],True,database)
    follow=analyst.answer('What is its budget?',context=r['context'],path=database)
    assert follow['facts']['budget']==40000
    assert analytics.snapshot(path=database)['campaigns'].set_index('campaign_id').loc['C03','budget']==40000
    with pytest.raises(ValueError): analyst.apply_action(proposal['pending'],True,database)
    task=analyst.answer('Create a task for C03',path=database); analyst.apply_action(task['pending'],True,database)
    exp=analyst.answer('Propose an experiment for C03',path=database); analyst.apply_action(exp['pending'],True,database)
    assert len(db.read('tasks',database))>=1 and len(db.read('experiments',database))>=1

QUESTIONS=[
 ('How many registrations?', '2800'),('How many confirmed registrations?', '2500'),
 ('What is actual attendance?', '2050'),('What is our marketing expenditure?', '274,000'),
 ('Which campaign generated the most registrations?', 'C02'),
 ('Which campaign has the lowest cost per registration?', 'C05'),
 ('Which campaign has the lowest cost per attendee?', 'C05'),
 ('Which campaign has the worst conversion rate?', 'C02'),
 ('Are we achieving targets?', '93.2%'),('Where is the biggest funnel bottleneck?', 'C03'),
 ('Where should we allocate additional budget?', 'C05'),('Who owns C01?', 'Meera'),
 ('Show weekly trends', 'weekly'),('What is the unique reach?', 'cannot answer'),
 ('How much bank receipt cash collected?', 'cannot answer'),('What was the weather?', 'cannot answer'),
 ('Tell me about quantum bananas', 'cannot map'),('What is C04 attendance?', '385'),
 ('What tasks exist?', 'tasks'),('What experiments exist?', 'experiments')]
@pytest.mark.parametrize('question,expected',QUESTIONS)
def test_analyst_questions(database,question,expected):
    r=analyst.answer(question,path=database); assert expected.lower() in r['text'].lower()

def test_new_record_changes_results(database):
    with db.connect(database) as c:
        c.execute("INSERT INTO people VALUES('New','external','2025-04-20T10:00:00+05:30','campaign','Campus Ambassadors','Meera Iyer','NEW-P','C01','T03')")
        c.execute("INSERT INTO registrations VALUES('New','Campus Ambassadors','Meera Iyer','2025-04-20T11:00:00+05:30','NEW-R','NEW-P','C01','T03')")
    db.append_status('NEW-R','confirmed','2025-04-20T12:00:00+05:30',database)
    s=analytics.snapshot(path=database); assert s['metrics']['registrations']==2801 and s['metrics']['confirmed']==2501
    assert '2801' in analyst.answer('How many registrations?',path=database)['text']
    assert analytics.snapshot('2025-04-19',path=database)['metrics']['registrations']==2800

@pytest.mark.parametrize('question',['Which campaign has lowest cost per attendee?','What should we scale?','Propose an experiment','Where is the bottleneck?'])
def test_early_analyst_has_no_future_outcomes(database,question):
    result=analyst.answer(question,'2025-02-01',path=database)
    assert result['text'] and '2050' not in result['text']

def test_cohort(database):
    s=analytics.snapshot('2025-04-20',start='2025-04-01',path=database)
    assert s['metrics']['target_achievement'] is None
    assert (analytics.dates(s['people'].first_seen_at)>=pd.Timestamp('2025-04-01',tz='Asia/Kolkata')).all()
    assert (analytics.dates(s['registrations'].registered_at)>=pd.Timestamp('2025-04-01',tz='Asia/Kolkata')).all()
    assert s['metrics']['attendees']<=s['metrics']['registrations']

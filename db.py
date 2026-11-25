"""Immutable source imports, validated operational writes and audit history."""
import os, json, sqlite3, uuid
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

ROOT=Path(__file__).resolve().parent
DEFAULT=ROOT/'data/risa.db'
TABLES={'Event':'event','Targets':'targets','Campaigns':'campaigns','Daily Marketing':'daily','People':'people','Interest and Engagement':'interactions','Registrations':'registrations','Registration History':'registration_history','Check-ins':'checkins'}
KEYS={'campaigns':'campaign_id','daily':'activity_id','people':'person_id','interactions':'interaction_id','registrations':'registration_id','registration_history':'history_id','checkins':'event_id'}
class Connection(sqlite3.Connection):
    def __exit__(self,typ,value,traceback):
        try: return super().__exit__(typ,value,traceback)
        finally: self.close()

def connect(path=None):
    p=Path(path or os.getenv('RISA_DB',str(DEFAULT))); p.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(p,timeout=20,factory=Connection); c.execute('PRAGMA foreign_keys=ON'); return c
def read(table,path=None):
    with connect(path) as c:
        allowed={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if table not in allowed: raise ValueError('Unknown table')
        return pd.read_sql_query(f'SELECT * FROM "{table}"',c)
def initialize(path=None):
    with connect(path) as c:
        if c.execute("SELECT name FROM sqlite_master WHERE name='campaigns'").fetchone(): return
        sheets=pd.read_excel(ROOT/'source/Attendee Dataset.xlsx',sheet_name=None)
        for sheet,table in TABLES.items():
            d=sheets[sheet].copy()
            for col in d:
                if pd.api.types.is_datetime64_any_dtype(d[col]):
                    # Excel serial dates lose timezone metadata. Source guide specifies IST.
                    d[col]=d[col].dt.strftime('%Y-%m-%dT%H:%M:%S+05:30')
            if table in KEYS:
                key=KEYS[table]
                if d.drop_duplicates()[key].duplicated().any(): raise ValueError(f'Conflicting IDs in {table}')
                d=d.drop_duplicates(key)
            d.to_sql(table,c,index=False)
            if table in KEYS: c.execute(f'CREATE UNIQUE INDEX "pk_{table}" ON "{table}"("{KEYS[table]}")')
        c.executescript('''
        CREATE TABLE campaign_plan(campaign_id TEXT PRIMARY KEY REFERENCES campaigns(campaign_id), budget REAL CHECK(budget>=0), status TEXT NOT NULL DEFAULT 'Historical', owner TEXT, notes TEXT DEFAULT '', deleted INTEGER DEFAULT 0);
        CREATE TABLE tasks(id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT, owner TEXT, priority TEXT, deadline TEXT, status TEXT, campaign_id TEXT REFERENCES campaigns(campaign_id));
        CREATE TABLE experiments(id TEXT PRIMARY KEY, name TEXT NOT NULL, hypothesis TEXT, audience TEXT, campaign_id TEXT REFERENCES campaigns(campaign_id), metric TEXT, expected REAL, budget REAL CHECK(budget>=0), start_date TEXT, end_date TEXT, actual REAL, decision TEXT, notes TEXT);
        CREATE TABLE audit_log(id INTEGER PRIMARY KEY, recorded_at TEXT, entity TEXT, entity_id TEXT, action TEXT, payload TEXT);
        CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
        INSERT INTO metadata VALUES('source','Fictional CampusFest 2025. Historical synthetic records.');
        ''')
        c.execute("INSERT INTO campaign_plan(campaign_id,owner) SELECT campaign_id,owner_name FROM campaigns")
        c.commit()
def log(c,entity,key,action,payload):
    c.execute('INSERT INTO audit_log(recorded_at,entity,entity_id,action,payload) VALUES(?,?,?,?,?)',(datetime.now(ZoneInfo('Asia/Kolkata')).isoformat(),entity,key,action,json.dumps(payload,default=str)))
def campaigns(path=None,include_deleted=False):
    a=read('campaigns',path).merge(read('campaign_plan',path),on='campaign_id',how='left')
    return a if include_deleted else a[a.deleted.fillna(0)==0]
def save_campaign(values,path=None):
    v=dict(values); key=v.pop('campaign_id'); budget=v.get('budget')
    if budget is not None and budget<0: raise ValueError('Budget must be nonnegative')
    if not v.get('campaign_name','').strip(): raise ValueError('Campaign name required')
    if v['planned_end_at']<v['planned_start_at']: raise ValueError('End must follow start')
    with connect(path) as c:
        exists=c.execute('SELECT 1 FROM campaigns WHERE campaign_id=?',(key,)).fetchone()
        cols=['campaign_name','channel','target_audience','objective','owner_name','created_at','planned_start_at','planned_end_at','owner_id']
        if not exists:
            c.execute('INSERT INTO campaigns(campaign_id,'+','.join(cols)+') VALUES('+','.join('?' for _ in range(10))+')',[key]+[v.get(x,'') for x in cols])
        else:
            # Historical facts remain intact; operational edits are separate where possible.
            editable=['campaign_name','channel','target_audience','objective','planned_start_at','planned_end_at']
            c.execute('UPDATE campaigns SET '+','.join(x+'=?' for x in editable)+' WHERE campaign_id=?',[v[x] for x in editable]+[key])
        c.execute('INSERT INTO campaign_plan(campaign_id,budget,status,owner,notes) VALUES(?,?,?,?,?) ON CONFLICT(campaign_id) DO UPDATE SET budget=excluded.budget,status=excluded.status,owner=excluded.owner,notes=excluded.notes',(key,budget,v.get('status','Proposed'),v.get('owner',v.get('owner_name','Unassigned')),v.get('notes','')))
        log(c,'campaign',key,'update' if exists else 'create',values)
def delete_campaign(key,confirmed=False,path=None):
    if not confirmed: raise ValueError('Confirmation required')
    with connect(path) as c:
        c.execute('UPDATE campaign_plan SET deleted=1 WHERE campaign_id=?',(key,)); log(c,'campaign',key,'archive',{})
def save_entity(table,values,path=None):
    if table not in ('tasks','experiments'): raise ValueError('Unsupported entity')
    v=dict(values); v['id']=v.get('id') or str(uuid.uuid4())[:12]
    allowed={'tasks':{'id','title','description','owner','priority','deadline','status','campaign_id'},'experiments':{'id','name','hypothesis','audience','campaign_id','metric','expected','budget','start_date','end_date','actual','decision','notes'}}[table]
    if set(v)-allowed: raise ValueError('Unexpected fields')
    if not v.get('title' if table=='tasks' else 'name','').strip(): raise ValueError('Name required')
    if table=='tasks' and v.get('status') not in ['To Do','In Progress','Blocked','Completed']: raise ValueError('Invalid status')
    if table=='experiments':
        if v.get('budget',0)<0: raise ValueError('Budget must be nonnegative')
        if v.get('end_date','')<v.get('start_date',''): raise ValueError('Invalid date range')
        if v.get('decision') not in ['Pending','Scale','Iterate','Stop']: raise ValueError('Invalid decision')
    with connect(path) as c:
        cols=list(v); c.execute(f'INSERT INTO {table}('+','.join(cols)+') VALUES('+','.join('?' for _ in cols)+') ON CONFLICT(id) DO UPDATE SET '+','.join(x+'=excluded.'+x for x in cols if x!='id'),list(v.values()))
        log(c,table,v['id'],'save',v)
    return v['id']
def append_status(registration_id,status,effective_at,path=None):
    if status not in ['interested','confirmed','cancelled','waitlisted']: raise ValueError('Invalid status')
    stamp=pd.Timestamp(effective_at)
    stamp=stamp.tz_localize('Asia/Kolkata') if stamp.tzinfo is None else stamp.tz_convert('Asia/Kolkata')
    with connect(path) as c:
        r=pd.read_sql_query('SELECT * FROM registrations WHERE registration_id=?',c,params=[registration_id])
        if r.empty: raise ValueError('Registration not found')
        if stamp<pd.Timestamp(r.iloc[0].registered_at): raise ValueError('Status precedes registration')
        v=r.iloc[0].to_dict(); v.pop('registered_at'); v.update(status=status,effective_at=stamp.isoformat(),history_id='EDIT-'+uuid.uuid4().hex)
        if c.execute('SELECT 1 FROM registration_history WHERE registration_id=? AND effective_at=?',(registration_id,stamp.isoformat())).fetchone(): raise ValueError('A status already exists at this timestamp')
        pd.DataFrame([v]).to_sql('registration_history',c,if_exists='append',index=False); log(c,'registration',registration_id,'status',v)
def set_budget(key,amount,path=None):
    if amount<0: raise ValueError('Budget must be nonnegative')
    with connect(path) as c:
        if not c.execute('SELECT 1 FROM campaign_plan WHERE campaign_id=?',(key,)).fetchone(): raise ValueError('Campaign not found')
        c.execute('UPDATE campaign_plan SET budget=? WHERE campaign_id=?',(amount,key)); log(c,'campaign',key,'budget',{'budget':amount})

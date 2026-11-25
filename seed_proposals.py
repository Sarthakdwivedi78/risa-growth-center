"""Optional reproducible proposed execution records. No fabricated outcomes."""
from datetime import date
import db
from build_reports import STRATEGIES

def seed():
    db.initialize()
    for i,s in enumerate(STRATEGIES,1):
        eid=f'PROPOSED-{i:02d}'; tid=f'PLAN-{i:02d}'
        if eid not in set(db.read('experiments').id):
            db.save_entity('experiments',dict(id=eid,name=s['name']+' (proposed)',hypothesis=f'The initiative delivers {s["net"]} incremental registrations after overlap allowance.',audience=s['audience'],campaign_id=s['campaign'],metric='Incremental registrations',expected=s['net'],budget=s['budget'],start_date='2027-02-01',end_date='2027-02-14',actual=None,decision='Pending',notes=f'PROPOSED, not historical. Dates are illustrative placeholders. {s["test"]}. Scale: {s["scale"]}. Stop: {s["stop"]}. Risk: {s["risk"]}. Allocation includes full initiative delivery, not just incremental acquisition.'))
        if tid not in set(db.read('tasks').id):
            db.save_entity('tasks',dict(id=tid,title='Validate '+s['name'],description=f'PROPOSED. Validate assumptions and dates before execution. Dependency: {s["dependency"]}. Resources: {s["resource"]}.',owner='Unassigned',priority='High' if i<=2 else 'Medium',deadline='2027-01-25',status='To Do',campaign_id=s['campaign']))

if __name__=='__main__': seed(); print('Proposed strategy records loaded; no actual outcomes fabricated.')

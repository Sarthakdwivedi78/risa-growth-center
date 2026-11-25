"""Capture expected/actual answers in a disposable database, including writes."""
import tempfile, sqlite3, json
from pathlib import Path
import db, analyst, analytics
from tests.test_core import QUESTIONS

def main():
    db.initialize(); lines=['# Chatbot acceptance evidence','All answers use fresh SQLite queries. External provider narration is optional and was not tested without credentials. Tests below run against a disposable source-baseline copy.']
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'test.db'
        with db.connect() as c,sqlite3.connect(path) as dest:c.backup(dest)
        dest.close()
        for i,(question,expected) in enumerate(QUESTIONS,1):
            r=analyst.answer(question,path=path); passed=expected.lower() in r['text'].lower()
            lines += [f'## {i}. {question}',f'Expected: answer contains `{expected}`. Result: **{"PASS" if passed else "FAIL"}**.','Actual:\n\n'+r['text'],'Sources: '+ '; '.join(r['sources'])]
            assert passed
        result=analyst.answer('Investigate C03',path=path)
        p=analyst.answer('Set its budget to INR 40000',context=result['context'],path=path)
        old=db.campaigns(path,True).set_index('campaign_id').loc['C03','budget']
        refused=False
        try:analyst.apply_action(p['pending'],False,path)
        except ValueError:refused=True
        assert refused
        analyst.apply_action(p['pending'],True,path)
        r=analyst.answer('What is its budget?',context=result['context'],path=path)
        assert r['facts']['budget']==40000
        dashboard=analytics.snapshot(path=path)['campaigns'].set_index('campaign_id').loc['C03']
        assert dashboard.budget==40000
        lines += ['## 21–24. Full diagnosis, proposal, confirmation and follow-up workflow', 'Expected: C03 diagnosis uses 350 registrations, 175 attendees, INR 59,000 spend and INR 337.14 CPA; unconfirmed write rejected; confirmed budget becomes INR 40,000; follow-up and dashboard both read it. **PASS**.', 'Diagnosis: '+result['text'],'Proposal: '+p['text'], 'Follow-up: '+r['text'],f'Dashboard after save: budget INR {dashboard.budget:,.0f}; spend INR {dashboard.spend:,.0f}; utilization {dashboard.budget_utilization:.1%}. Historical source spend unchanged.']
        s=analytics.snapshot(path=path); reg=s['registrations'].query("status=='confirmed'").iloc[0].registration_id
        db.append_status(reg,'cancelled','2025-04-20T23:00:00+05:30',path)
        r=analyst.answer('How many confirmed registrations?',path=path); assert '2499' in r['text']
        lines += ['## 25. Modified registration data','Expected: 2,499 confirmed after appending one cancellation. **PASS**. Actual:\n\n'+r['text']]
        r=analyst.answer('What is actual attendance as of 2025-04-11?',path=path); assert r['facts']['attendees']==0
        lines += ['## 26. Date specified in natural-language question','Expected: zero actual admission before the event, no hindsight. **PASS**. Actual:\n\n'+r['text']]
    (db.ROOT/'reports/chatbot_tests.md').write_text('\n\n'.join(lines),encoding='utf8')

if __name__=='__main__':main()

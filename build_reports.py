"""Reproduce audit artifacts, detailed strategy and exactly three PDF slides."""
import json, hashlib, sqlite3
from pathlib import Path
import pandas as pd
import db, analytics
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=db.ROOT; OUT=ROOT/'reports'; OUT.mkdir(exist_ok=True)
KEY={'Campaigns':'campaign_id','Daily Marketing':'activity_id','People':'person_id','Interest and Engagement':'interaction_id','Registrations':'registration_id','Registration History':'history_id','Check-ins':'event_id','Brands':'brand_id','Sponsor contacts':'contact_id','Sponsor campaigns':'sponsor_campaign_id','Sponsor interactions':'interaction_id','Brand qualification':'history_id','Partner opportunities':'opportunity_id','Opportunity history':'history_id','Sponsor activations':'activation_id'}
def audit():
    report=['# Data audit','All 23 sheets and all populated rows were scanned. Source files remain unchanged. Timestamps imported from timezone-naive Excel cells are localized to Asia/Kolkata as specified in the source guide.','## Selection','Challenge A measures actual attendance through verified admission events. Sponsor data has 180 brands, 270 contacts, 58 opportunities, 60 latest-qualified brands and 24 latest-confirmed opportunities. It contains no receipt ledger, so confirmed cash-type partnership value cannot establish pre-festival cash collected.','## Sheet inventory and quality']
    schemas={}; tables={}; hashes={}
    for name in ['Attendee','Sponsor']:
        file=ROOT/f'source/{name} Dataset.xlsx'; hashes[file.name]=hashlib.sha256(file.read_bytes()).hexdigest(); sheets=pd.read_excel(file,sheet_name=None); tables[name]=sheets
        for sheet,d in sheets.items():
            key=KEY.get(sheet); duplicates=int(d[key].duplicated().sum()) if key else int(d.duplicated().sum()); conflicts=int(d.drop_duplicates()[key].duplicated().sum()) if key else 0
            schemas[f'{name}/{sheet}']={'rows':len(d),'key':key,'duplicate_ids':duplicates,'conflicting_ids':conflicts,'fields':{col:{'pandas_type':str(d[col].dtype),'missing':int(d[col].isna().sum()),'distinct':int(d[col].nunique())} for col in d}}
            report += [f'### {name}: {sheet}',f'{len(d):,} rows. Stable key: {key or "metadata / effective_at for targets"}. Duplicate keys/rows: {duplicates}. Conflicting key payloads: {conflicts}.', '|Column|Observed type|Missing|Distinct|','|---|---|---:|---:|']
            report += [f'|{col}|{d[col].dtype}|{d[col].isna().sum()}|{d[col].nunique()}|' for col in d]
    a=tables['Attendee']; sp=tables['Sponsor']; links=[('Attendee','Registrations','person_id','People','person_id'),('Attendee','Registrations','campaign_id','Campaigns','campaign_id'),('Attendee','Registration History','registration_id','Registrations','registration_id'),('Attendee','Check-ins','registration_id','Registrations','registration_id'),('Attendee','Check-ins','person_id','People','person_id'),('Attendee','Interest and Engagement','person_id','People','person_id'),('Attendee','Interest and Engagement','campaign_id','Campaigns','campaign_id'),('Attendee','People','first_campaign_id','Campaigns','campaign_id'),('Attendee','Daily Marketing','campaign_id','Campaigns','campaign_id'),('Sponsor','Sponsor contacts','brand_id','Brands','brand_id'),('Sponsor','Sponsor interactions','brand_id','Brands','brand_id'),('Sponsor','Sponsor interactions','contact_id','Sponsor contacts','contact_id'),('Sponsor','Sponsor interactions','sponsor_campaign_id','Sponsor campaigns','sponsor_campaign_id'),('Sponsor','Brand qualification','brand_id','Brands','brand_id'),('Sponsor','Partner opportunities','brand_id','Brands','brand_id'),('Sponsor','Partner opportunities','primary_contact_id','Sponsor contacts','contact_id'),('Sponsor','Opportunity history','opportunity_id','Partner opportunities','opportunity_id'),('Sponsor','Sponsor activations','opportunity_id','Partner opportunities','opportunity_id')]
    report+=['## Relationships','Campaigns 1:N Daily Marketing / Registrations / Interactions. People 1:N Registrations / Interactions / Check-ins. Registrations 1:N full-state history. Check-ins.event_id is an admission-event key, not a festival identity. Sponsor brands 1:N contacts and opportunities; opportunities 1:N history. Activations link opportunities to attendee campaigns. Owner IDs are labels shared across sources; no separate owner table is supplied.','|Reference|Orphan nonblank IDs|','|---|---:|']
    for name,child,col,parent,pcol in links:
        data=tables[name]; orphan=set(data[child][col].dropna())-set(data[parent][pcol].dropna()); report.append(f'|{name}: {child}.{col} to {parent}.{pcol}|{len(orphan)}|')
    report += [f'|Sponsor activations.attendee_campaign_id to Attendee Campaigns|{len(set(sp["Sponsor activations"].attendee_campaign_id)-set(a["Campaigns"].campaign_id))}|']
    pr=a['People'].set_index('person_id'); reg=a['Registrations'].set_index('registration_id')
    mismatches={}
    for sheet in ['Registration History','Check-ins']:
        d=a[sheet].dropna(subset=['registration_id']).merge(reg[['person_id','campaign_id']],left_on='registration_id',right_index=True,suffixes=('','_reg'))
        mismatches[sheet]={'person_mismatches':int((d.person_id!=d.person_id_reg).sum()),'campaign_mismatches':int((d.campaign_id!=d.campaign_id_reg).sum())}
    temporal={}
    for name,sheets in tables.items():
        for sheet,d in sheets.items():
            for col in d:
                if pd.api.types.is_datetime64_any_dtype(d[col]): temporal[f'{name}/{sheet}/{col}']={'earliest':str(d[col].min()),'latest':str(d[col].max()),'missing':int(d[col].isna().sum())}
    (OUT/'temporal_audit.json').write_text(json.dumps(temporal,indent=2))
    rr=a['Registrations'].merge(a['People'][['person_id','first_seen_at']],on='person_id')
    hh=a['Registration History'].merge(a['Registrations'][['registration_id','registered_at']],on='registration_id')
    mismatches['temporal']={'registrations_before_identity':int((rr.registered_at<rr.first_seen_at).sum()),'history_before_registration':int((hh.effective_at<hh.registered_at).sum())}
    report+=['## Interpretation and consistency',json.dumps(mismatches), 'Attendee duplicate source IDs: 2 activity_id, 4 history_id, 20 admission event_id. Sponsor duplicates: 3 interaction_id, 1 qualification history_id, 2 opportunity history_id. All identical payloads. Remove import copies only.','Three repeated display names identify different people; never merge them. People include 3,625 external, 40 internal, 10 staff and 10 test identities. There are 2,840 total registrations but only 2,800 external registrations.','145 people lack first-campaign attribution; 170 raw check-in rows lack registration/campaign attribution. Missing IDs here are documented walk-in/access paths, not automatic data corruption. Sponsor root touches legitimately omit origin_interaction_id (373 rows).','Negative marketing entries total INR -6,500 and represent vendor credits. Net spend is INR 274,000. No conflicting stable-key payloads were found.','Campaign budgets, venue capacity, student ages/college membership, unique cross-platform reach, ticket revenue, experimental holdouts and bank receipts are missing. Do not fill these with invented facts.','## Baseline, 20 April 2025 IST']
    s=analytics.snapshot(); report += [json.dumps(s['metrics'],indent=2),s['campaigns'].to_markdown(index=False),'## Bottlenecks','2,800 registered people produced 1,925 verified registered visitors: 68.75%. This loses 875 people between registration and admission. There are 825 external identities without a registration, including 125 admitted walk-ins. Latest confirmation-to-admission and all-registration conversion use different denominators.','Creator Partners has CPA INR 337.14 and registration-to-attendance 50%; Paid Social also converts 50% of registrants to attendance. Referrals CPA is INR 69.09, College Partnerships INR 80.52. These observational differences suggest hypotheses, not causal spend-response estimates.','## Original file SHA-256',json.dumps(hashes,indent=2)]
    (OUT/'data_audit.md').write_text('\n\n'.join(report),encoding='utf8'); (OUT/'data_audit.json').write_text(json.dumps(schemas,indent=2),encoding='utf8'); (OUT/'source_hashes.json').write_text(json.dumps(hashes,indent=2))
    (OUT/'baseline.json').write_text(json.dumps(s['metrics'],indent=2)); s['campaigns'].to_csv(OUT/'campaign_baseline.csv',index=False)
    with db.connect() as c: schema=';\n\n'.join(x[0] for x in c.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"))+';\n'
    (ROOT/'schema.sql').write_text(schema,encoding='utf8')

STRATEGIES=[
 dict(name='College club partnerships',campaign='C04',gross=320,net=256,budget=70000,ice='8 x 8 x 7 = 448',audience='Club and competition participants',resource='1 partnerships lead + 10 club captains',timing='T-6 to T-1 weeks',dependency='College permission and group itinerary',risk='Group overlap, transport no-shows',test='Randomize 20 matched clubs to itinerary + group RSVP or standard outreach',scale='>=12.8 incremental registrations/club and CPA <= INR 120',stop='<6 incremental registrations/club or CPA > INR 180',fix='Replace inactive clubs; stagger transport and reminders',leading='Active clubs, RSVP-to-confirmed rate'),
 dict(name='Student referral programme',campaign='C05',gross=240,net=192,budget=45000,ice='8 x 8 x 6 = 384',audience='Friends of consented registrants',resource='1 growth operator + developer',timing='T-5 to T-1 weeks',dependency='Unique referral codes and admission validation',risk='Self-referral fraud and existing-user overlap',test='50/50 person-level invitation incentive holdout; reward verified admission only',scale='>=0.20 new registrations/inviter and CPA <= INR 100',stop='<0.08 registrations/inviter or fraud >5%',fix='Cap rewards; block self-referrals; shorten invitation steps',leading='Unique eligible invites, new-identity share'),
 dict(name='Campus ambassador expansion',campaign='C01',gross=180,net=144,budget=80000,ice='7 x 7 x 6 = 294',audience='Students at nearby campuses',resource='1 lead + 20 ambassadors',timing='T-6 to T-1 weeks',dependency='Campus access and weekly reporting',risk='Uneven activation and unsupported signups',test='Randomize 20 campus clusters to ambassador kit vs usual communication',scale='>=7.2 incremental registrations/ambassador and CPA <= INR 120',stop='<3 registrations/ambassador or CPA > INR 180',fix='Coach or replace inactive reps; focus nearby campuses',leading='Active ambassadors, verified signups per rep'),
 dict(name='Performance + retargeting',campaign='C02',gross=160,net=128,budget=65000,ice='6 x 6 x 5 = 180',audience='Consented form abandoners; exclude confirmed people',resource='1 marketer + shared analyst',timing='T-4 to T-1 weeks',dependency='Consent, suppression list and conversion events',risk='Cannibalization, saturation and weak form completion',test='Randomized user holdout with equal creative exposure rules',scale='>=5 pp form-completion lift and incremental CPA <= INR 140',stop='<=0 pp lift or incremental CPA > INR 210',fix='Pause audience; repair form; cap frequency at 3/week',leading='Unique form starts, completion, frequency'),
 dict(name='Creator micro-pilots',campaign='C03',gross=100,net=80,budget=20000,ice='5 x 4 x 4 = 80',audience='Local niche student communities',resource='1 creator manager + 2 creators',timing='T-4 to T-2 weeks',dependency='Verified audience geography and trackable links',risk='Vanity reach and poor attendance intent',test='Two matched audience cells, creator content vs event information',scale='>=40 incremental registrations/creator and CPA <= INR 160',stop='<15 registrations/creator or CPA > INR 240',fix='Change programme hook once, then stop broad creator buys',leading='Qualified click-to-start and verified new identities')]
def strategy():
    text='''# Growth strategy and assumptions

Choose Bengaluru for a proposed next edition. The historical dataset has no city field, so this is a planning choice, not a claim about where CampusFest 2025 occurred. Ministry of Education AISHE 2020-21 reported 1,058 colleges in Bangalore Urban. This dated evidence establishes a substantial college base, not current enrollment or reachable audience. Source: https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1894517&lang=2&reg=48

## Audience model
Assume 40 accessible colleges x 1,500 eligible students = 60,000 potential students. Prioritize 20,000 club/competition participants, 25,000 general campus students and 15,000 friend/interest communities as mutually exclusive planning buckets. These sizes are unverified assumptions, not inferred from People names. Confirm campus permissions, geography and deduplicated audience before spending.

Assumed reachable audience 30,000 of 60,000. Base identified-interest pool 4,800 (16% reach-to-interest assumption), registrations 3,600 (75%), confirmed 3,240 (90%), registered attendees 2,700 (83.33% of confirmed; 75% of all registered), plus 100 walk-ins = 2,800 visitors. Forecast cohorts are nested by construction, unlike observed final historical status groups. Reach-to-interest cannot be calibrated from anonymous source reach.

Stretch: 35,000 reachable, 5,500 identified interest (15.71%), 4,000 registrations (72.73%), 3,600 confirmed (90%), 3,200 registered attendees (88.89% of confirmed, 80% of registered), plus 100 walk-ins = 3,300 unconstrained. Cap at assumed 3,200 distinct visitor capacity and reserve 100 walk-in places, reducing admitted registered visitors to 3,100. Final visitor target 3,200. Validate total-event unique capacity and peak concurrent capacity separately with venue operations. No source venue-capacity figure exists.

Historical: 3,625 external people, 2,800 registrations, 2,500 confirmed, 1,925 registered verified visitors + 125 unregistered visitors = 2,050. Identified-interest actions are calculated separately in baseline.json. Historical registration conversion 77.24%, confirmation 89.29%, registered show rate 68.75%. INR 274,000 / 2,800 = INR 97.86 per registration; / 1,925 = INR 142.34 per attributed attendee; / 2,050 = INR 133.66 per total visitor. The latter allocates spend to otherwise unattributed walk-ins and is labelled an event-wide ratio.

## Budget and target bridge
Assume next-edition authorization of the source's final INR 300,000 ceiling. The source limit is historical, not a future approval. Allocate INR 280,000 across five all-in initiatives plus INR 20,000 reserve. This is the entire next-edition budget, not INR 300,000 added to historical INR 274,000. Existing organic/community communication is folded into campus and club delivery. Volunteer time is constrained, not priced as cash. Team: three operators, one shared analyst/developer, 20 ambassadors and 10 club captains; roles overlap and require workload validation.

Anchor the repeatable registration base at 2,800 as an explicit assumption. Gross incremental initiative registrations 320+240+180+160+100=1,000. Apply 20% overlap/cannibalization haircut once: 800 net, producing 3,600. Deduplicate person IDs and assign each prospect to one experiment. Observed first-touch attribution alone does not justify adding all channel lifts.

Base visitor bridge: 2,050 + (800 x 75%) + [2,800 x (75%-68.75%)] + (100-125) = 2,800. Acquisition adds 600, improved attendance adds 175, lower walk-ins subtract 25. Forecast acquisition cost at full ceiling: 300,000 / 3,600 = INR 83.33 per registration and / 2,800 = INR 107.14 per total visitor. This requires a 14.8% improvement in CPR and a 6.25 percentage-point increase in registered show rate. Capacity, distribution and improved channel mix are unproven dependencies.

Stretch assumes gross increments 1,500, same 20% haircut = 1,200 net. 2,800+1,200=4,000 registrations. At 80% show rate plus 100 walk-ins: 3,300 before capacity, 3,200 after capacity. Same cash ceiling requires INR 75 CPR and INR 93.75 per admitted visitor, and 11.25 percentage-point show-rate improvement. Release reserve only after pilots demonstrate better unit economics. Downside: 3,200 registrations x 68.75% +100 =2,300 visitors. The range is a scenario analysis, not a fitted confidence interval.

## Prioritization
ICE = Impact x Confidence x Ease, each scored 1–10. Scores are explicit judgment informed by historical CPA, delivery feasibility and available volunteer resources. College clubs and referrals lead; ambassadors remain a core channel; paid retargeting is conditional; broad creator sponsorships are rejected in favor of two capped micro-tests. Organic search's low CPA is useful supporting infrastructure, not evidence it can absorb arbitrary spend.
'''
    for i,s in enumerate(STRATEGIES,1):
        text+=f'\n### {i}. {s["name"]}\n'+ '\n'.join(f'- {k}: {v}' for k,v in s.items() if k!='name')+f'\n- Expected base incremental attendees: {s["net"]} net registrations x 75% = {s["net"]*.75:.0f}. This acquisition contribution excludes the shared 175-person attendance improvement.\n'
    text+='''
## Monitoring and experiment discipline
Incremental CPA means (treatment cost minus comparable control cost) / incremental verified visitors, not the whole initiative allocation divided by incremental visitors. Pilot cash caps within the all-in initiative budgets are INR 15,000 for clubs, 10,000 for referrals, 10,000 for ambassadors, 10,000 for paid retargeting and 5,000 for creators (INR 50,000 total). The remaining INR 230,000 of allocated budget sustains baseline delivery and subsequent gated scaling. These are proposed allocations; record actual treatment/control cost before judging the thresholds. Pilot effects are extrapolated to full deployment only after valid evidence and capacity checks.

Review daily cohort counts, net spend, completed registrations, cancellations and explicit opt-outs. Review matched cluster outcomes weekly. Acquisition KPI thresholds are operating gates, not proof of significance. CPA gates refer to incremental attendees measured against a randomized holdout; pre-event proxies use registrations x a labelled 75% show assumption. Do not replace missing causal lift with attributed historical CPA.

Scale only after two consecutive review windows pass the strategy-specific volume and cost gates, with positive lower 95% confidence bound on incremental outcome and a valid pre-registered analysis. For initial directional review require at least 200 eligible people per arm for individual tests, or 10 clusters per arm for club/campus tests. These small pilot floors do NOT establish adequate statistical power. At baseline 68.75% attendance, detecting +6.25 percentage points with two-sided 5% alpha/80% power needs roughly 850–900 people per arm before cluster/design effects. Do not claim significance at 200/arm. Defer scale if underpowered; pool comparable waves or treat results as directional.

For binary outcomes use a two-proportion interval/test; for clubs/campuses use cluster-level randomization inference or cluster-robust uncertainty. Freeze a 14-day window, primary metric and exclusion rules before launch. Avoid repeatedly testing each day. Adjust multiple comparisons across five tests (Holm) before claiming portfolio causal lift. Stop immediately for consent failures or >5% invalid referral identities. Otherwise stop after two failed review windows or the pilot budget cap. Between success and failure gates, iterate one variable and rerun with a new locked cohort. Missing exposure or identity logs means fix instrumentation before a decision.

The thresholds reflect a base overall visitor cost of INR 107 and a proposed ceiling of INR 120 for scalable grassroots pilots. Paid/creator gates allow discovery premiums of INR 140/160, with lower budget caps. Failure cost bands are 1.5x the scale gate (180/210/240). Referral fraud caps and per-rep volumes are proposed operational guardrails. Trial cost is part of each initiative allocation. Reserve INR 20,000, never exceed total INR 300,000 without explicit new approval.

Dashboard: monitor registrations and first admissions by IST date, registered-cohort attendance, target vintage, attributed campaign CPA and actual spend vs current operational allocation. AI reads the latest database, cites fields/IDs, proposes a diagnosis and prepares an action. User confirmation is required to save. It does not infer causality or automatically scale spend. Persist experiment actuals, decision and evidence notes manually; no random-assignment or significance engine is claimed in this version.
'''
    (OUT/'growth_strategy.md').write_text(text,encoding='utf8')

def slides():
    # User explicitly requests a PDF. Use ReportLab PDF authoring; no extra cover slide.
    fonts=Path('C:/Windows/Fonts')
    for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]: pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
    W,H=1600,900; c=canvas.Canvas(str(ROOT.parent/'RISA_Growth_Strategy.pdf'),pagesize=(W,H)); navy='#14263D'; green='#177F72'; muted='#53677E'
    def para(text,x,y,w,size=22,color=navy,bold=False):
        style=ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.3,textColor=HexColor(color))
        p=Paragraph(text,style); ww,hh=p.wrap(w,H); p.drawOn(c,x,H-y-hh); return hh
    def header(n,title,sub):
        c.setFillColor(HexColor('#F7F9FC')); c.rect(0,0,W,H,fill=1,stroke=0)
        para('RISA LABS  /  ATTENDEE GROWTH',60,35,1400,17,green,True); para(title,60,78,1480,42,navy,True); para(sub,60,141,1480,20,muted)
        para(f'{n:02d} / 03',1450,842,100,16,muted)
    def table(rows,widths,x,y,size=19,rowheights=None):
        style=ParagraphStyle('cell',fontName='Body',fontSize=size,leading=size*1.24,textColor=HexColor(navy))
        cells=[[Paragraph(str(v),style) for v in row] for row in rows]
        t=Table(cells,colWidths=widths,rowHeights=rowheights,hAlign='LEFT'); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#DFEBE8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.6,HexColor('#CDD8DF'))])); tw,th=t.wrap(W,H); t.drawOn(c,x,H-y-th); return th
    header(1,'How high can we aim?','Bengaluru • Proposed next edition • Sarthak Dwivedi • Historical comparison: 20 April 2025 IST')
    para('2,800 base',60,202,500,54,green,True); para('3,200 stretch',570,202,500,54,green,True); para('INR 300,000',1100,202,440,46,navy,True)
    para('3,600 registrations × 75% + 100 walk-ins',60,279,490,22); para('min(3,200 capacity, 4,000 × 80% + 100)',570,279,500,22); para('Assumed total budget ceiling<br/>INR 280k allocation + 20k reserve',1100,273,440,22)
    rows=[['Measure','Historical synthetic records','Proposed base case'],['Reach','666,297 summed daily reach observations.<br/>Unique reach and reach conversion unavailable.','30,000 unique prospects assumed'],['Identified interest / people','3,500 people with interest actions<br/>3,625 external identities overall','4,800 interested (16% of reach assumed)'],['Registrations','2,800 / 3,500 interested = 80%<br/>2,800 / 3,625 identities = 77.24%','3,600 / 4,800 = 75%'],['Confirmed registrations','2,500 / 2,800 = 89.29%','3,240 / 3,600 = 90%'],['Actual attendance','1,925 registered / 2,800 = 68.75%<br/>+ 125 walk-ins = 2,050 unique visitors','2,700 / 3,240 = 83.33%<br/>+ 100 walk-ins = 2,800 forecast visitors']]
    table(rows,[320,600,560],60,345,20)
    para('Audience and constraints',60,725,480,23,navy,True)
    para('Assume 40 colleges × 1,500 students = 60,000 potential. Prioritize clubs, nearby campuses and friends. Bengaluru Urban had 1,058 colleges in AISHE 2020–21 [1]. Venue capacity of 3,200 requires validation.',60,765,700,18)
    para('Target bridge and economics',820,725,720,23,navy,True)
    para('2,050 + 600 acquisition + 175 better show rate − 25 walk-ins = 2,800. Historical spend INR 274k; CPR 97.86; attributed CPA 142.34. Base CPR 83.33 and total-visitor cost 107.14. No campaign effect is causal.',820,765,720,18)
    c.showPage()
    header(2,'Where will we place our bets?','Five proposed initiatives • ICE = impact × confidence × ease (1–10) • Budget includes delivery and testing')
    rows=[['Rank / strategy / ICE','Audience and contribution','Budget / people / timing','Test, dependency and risk']]
    for i,s in enumerate(STRATEGIES,1):
        rows.append([f'<b>{i}. {s["name"]}</b><br/>{s["ice"]}',f'{s["audience"]}<br/><b>+{s["net"]} net registrations / +{s["net"]*.75:.0f} attendees</b>',f'INR {s["budget"]:,}<br/>{s["resource"]}<br/>{s["timing"]}',f'{s["test"]}.<br/>Needs: {s["dependency"]}.<br/>Risk: {s["risk"]}.'])
    table(rows,[300,320,300,560],60,195,18)
    para('Scale clubs and referrals after gates pass. Maintain ambassadors. Test retargeting cautiously. Reject broad creator buys; cap two micro-pilots.',60,742,1480,23,green,True)
    para('Impact math: 1,000 gross registrations × 80% after overlap = 800 net; × 75% show = 600 incremental attendees. Repeat-base assumption: 2,800 registrations. Person-ID deduplication and mutually exclusive test cohorts prevent adding the same person twice.',60,800,1370,19)
    c.showPage()
    header(3,"How will we know what’s working?",'Proposed operating gates • Outcomes use randomized holdouts • Attributed historical CPA guides hypotheses only')
    rows=[['Strategy / critical variable','Scale gate / leading signals','Stop gate / corrective action']]
    for s in STRATEGIES:
        rows.append([f'<b>{s["name"]}</b><br/>{s["risk"]}',f'{s["scale"]}.<br/>Watch: {s["leading"]}.',f'{s["stop"]}.<br/>Action: {s["fix"]}.'])
    table(rows,[360,560,560],60,205,18)
    para('Decision discipline',60,667,720,24,navy,True)
    para('Two review windows + positive 95% lower lift bound before scale. Pilot floor: 200 people/arm or 10 clusters/arm; directional only. Detecting +6.25 pp show rate needs roughly 850–900/arm before cluster effects. Iterate one variable between gates. Stop at budget cap or consent failure.',60,707,720,20)
    para('Dashboard → analyst → confirmed action',850,667,690,24,navy,True)
    para('Track cohort conversions, spend, target vintage, opt-outs and admissions. AI cites fresh database facts, diagnoses C03, proposes a budget/task/test and waits for confirmation. Save in SQLite; refresh dashboard and follow-up answer. INR 120 grassroots CPA gate supports INR 107 base visitor economics.',850,707,690,20)
    para('[1] Ministry of Education, AISHE 2020–21, PIB release 29 Jan 2023: pib.gov.in/Pressreleaseshare.aspx?PRID=1894517. Full assumptions, test designs and source definitions: reports/growth_strategy.md and data_audit.md.',60,841,1350,14,muted)
    c.showPage(); c.save()

if __name__=='__main__':
    db.initialize(); audit(); strategy(); slides()
    print(json.dumps(analytics.snapshot()['metrics'],indent=2))

# RISA Growth Center

A working Streamlit analytics and execution application for **Challenge A: Attendee Growth**, with an embedded, database-grounded analyst. The supplied CampusFest event is fictional and historical (12–13 April 2025). Every future strategy is a proposal. The presentation contains exactly three slides and names Sarthak Dwivedi on slide one.

## Start here

Use standard CPython 3.11 or 3.12. From this folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS/Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Open the localhost URL printed by Streamlit (normally http://localhost:8501). No API key or paid subscription is required. A populated SQLite database is included. If it is missing, the app imports the original attendee workbook on first launch. SQLite changes persist across local app restarts. Run tests against disposable databases with `python -m pytest tests -q`. Run `python build_reports.py` to reproduce the audit and PDF (PDF builder uses Windows Arial fonts; change the font paths on another OS).

The delivered database also contains five explicitly proposed experiments and five planning tasks. Their January/February 2027 dates are illustrative placeholders, not agreed festival dates, and actual results are blank. Run `python seed_proposals.py` to recreate these idempotently in a fresh database. Campaign budgets remain unavailable until you enter an operational allocation.

## Deliverables and interpretation

- `app.py`: all eight requested pages and operational forms.
- `analytics.py`: historical snapshots, matched-cohort rates, attribution, trends and explicit forecasts.
- `db.py`: source import, unique-ID indexes, parameterized writes, validation, audit log and operational storage.
- `analyst.py`: intent routing to fresh analytics, evidence, context-aware follow-ups, confirmed writes and optional model narration.
- `data/risa.db` and `schema.sql`: working database and reproducible table/index definitions.
- `source/`: unchanged copies of both workbooks and the assignment PDF.
- `reports/data_audit.md`, `data_audit.json`, `source_hashes.json`: every sheet, field, type, missing-value count, duplicate check, relationship and source checksum.
- `reports/growth_strategy.md`: full quantitative model, five ICE-ranked initiatives, resources, risks, experiment design and numeric decision gates.
- `reports/baseline.json`, `campaign_baseline.csv`: reproducible historical outputs.
- `reports/chatbot_tests.md`, `test_results.xml`, `test_summary.md`: expected/actual answers and executed checks.
- `../RISA_Growth_Strategy.pdf`: exactly three presentation slides.

The PDF's references to “training” the chatbot are interpreted as access to chosen-track evidence, not fine-tuning a model on a static snapshot. The user's explicit dynamic-data requirement takes priority. The original source remains available for testing.

## Why Attendee Growth and Bengaluru

The attendee file supports a complete measurable outcome: identified people, registered people, dated status changes and verified admissions. The sponsor file has 180 brands, 270 contacts and 58 opportunities, but **no bank receipts**. Its latest 24 confirmed partnerships are not proof of collected cash, the actual Challenge B objective.

Bengaluru is a proposed location; the synthetic event file does not identify a city. The [Ministry of Education's AISHE 2020–21 release](https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1894517&lang=2&reg=48) reports 1,058 colleges in Bangalore Urban. This dated source supports a large college base. It does not substantiate present enrollment or reach. The model explicitly assumes 40 accessible colleges × 1,500 students = 60,000 potential students. College permissions, student numbers, a 3,200-visitor venue ceiling and future budget approval require validation.

Base forecast: 3,600 registrations × 75% show rate + 100 walk-ins = **2,800 visitors**. Stretch: min(3,200 capacity, 4,000 × 80% + 100) = **3,200**. Forecast cash ceiling: INR 300,000, including INR 20,000 reserve. Five initiatives contribute 1,000 gross registrations, reduced once by 20% overlap to 800 net. The repeat base of 2,800 registrations is an assumption, not a guarantee. Full arithmetic, downside and capacity handling appear in the strategy report.

## Audited baseline (20 April 2025, end of day IST)

|Metric|Value|Definition|
|---|---:|---|
|Identified external identities|3,625|Distinct external person IDs existing by cutoff|
|Identified interest|3,500|Distinct external people with page visit, brochure download, form start or event question|
|Completed registrations|2,800|Unique external registration IDs, including subsequently cancelled records|
|Confirmed registrations|2,500|Latest eligible history status confirmed|
|Cancelled registrations|183|Latest eligible history status cancelled|
|Verified external attendees|2,050|Distinct external person IDs with admitted AND verified events|
|Registered attendees|1,925|Verified attendees matched to an eligible created registration|
|Unregistered attendees|125|Verified attendees without a registration as of cutoff|
|Net marketing spend|INR 274,000|Posted activity ledger after ID deduplication and credits|
|Registration conversion|77.24%|2,800 / 3,625|
|Interest-to-registration|80.00%|2,800 matched interested registrants / 3,500 interested people|
|Confirmation rate|89.29%|2,500 / 2,800|
|Confirmed-cohort attendance|77.00%|1,925 admitted confirmed people / 2,500 confirmed people|
|All-registrant attendance|68.75%|1,925 / 2,800|
|Cost per registration|INR 97.86|274,000 / 2,800|
|Cost per attributed attendee|INR 142.34|274,000 / 1,925|
|Event-wide spend per visitor|INR 133.66|274,000 / 2,050; includes unattributed walk-ins|
|Visitor target attainment|93.18%|2,050 / 2,200 revised target|
|Budget utilization|91.33%|274,000 / 300,000 revised budget|

Referrals have the lowest attributed CPA (INR 69.09), followed by Organic Search (71.79) and College Partnerships (80.52). Creator Partners have the highest (337.14), then Paid Social (273.53). Paid Social has the most registrations (680). These are descriptive rankings, not causal spending elasticities. Channels can differ in intent and selection.

## Cleaning and temporal rules

1. Preserve source workbook bytes and record SHA-256 checksums. Read every worksheet; retain source field guides.
2. Deduplicate exact repeated stable IDs: attendee daily activity 2, status history 4, admission events 20; sponsor interactions 3, qualification history 1, opportunity history 2. Conflicting-ID payloads cause an import failure rather than an arbitrary choice. Unique indexes reject repeated IDs in working tables.
3. Use person IDs, registration IDs and campaign IDs for joins. Three repeated display names remain separate people. The 40 internal, 10 staff and 10 test identities never enter external visitor metrics.
4. Excel's typed dates lose timezone suffix metadata. Source guidance identifies them as Asia/Kolkata, so ingestion explicitly adds +05:30. End-of-day filters use the next midnight as an exclusive cutoff. No later history state leaks backward.
5. Select the latest full-state history for each registration, ordered by effective timestamp and stable history ID. Registration history rows are never registrations. Missing historical state is `unknown`, never implicitly confirmed.
6. Admission requires `result=admitted` and `verification=verified`; deduplicate by event ID, then person ID for attendance. Reentries/manual scans do not create more visitors. Earliest eligible admission owns the first-admission trend.
7. Attribute registrations to their registration campaign. Attribute attendees through that registration, not check-in campaign or engagement campaign. If new data supplies multiple registrations for a person, earliest created eligible registration owns their campaign attribution. Person-level attendance remains unique.
8. Use the target version effective at cutoff: INR 240,000 / 1,800 visitors before 15 March 2025; INR 300,000 / 2,200 from 15 March. Planned dates are never completed events.
9. Net credits (INR -6,500) remain negative spend. Summed reach (666,297) is **daily platform observations**, never unique people. Anonymous click/session/start ratios are not individual user conversion probabilities.

## Filters and formulas

`snapshot(day, campaign_ids, channel, path, start)` is the reusable entry point. All dashboard views and chatbot answers invoke it afresh. No static KPI cache exists.

- Date: historical state as of selected IST day. Tasks, owners and user-entered allocation budgets represent current operational state, clearly labelled independently of the historical date.
- Campaign/channel: registrations use acquisition attribution; identified people use fixed first-touch attribution. Campaign conversion uses the intersection of those groups. The global registration-conversion card is unavailable under campaign filters to avoid incompatible denominators. Engagement campaign IDs remain separately inspectable.
- Optional start date: an acquisition cohort whose identities AND registrations started since that date, followed to the as-of date. Spend is from the same interval; it is an observational allocation, not proof all spend acquired those people. Event-wide target comparisons are unavailable for subsets.
- Completed-registration conversion: distinct registered people / external identified people. In this source each external person has one registration, so it equals completed registrations / identified people. For new repeated registrations, person conversion remains bounded while the separate registration count counts registration IDs.
- Confirmation: confirmed registration IDs / all registration IDs.
- Eligible attendance: admitted people in the currently confirmed cohort / distinct people in that cohort. This is a selected-date cohort metric, not status-at-gate reconstruction. Admission evidence remains counted even if a later status cancels a registration.
- CPR: net spend / attributed unique registration IDs. CPA: net spend / attributed unique verified people. Global event-wide visitor cost is separately named.
- CTR: clicks / impressions. Landing conversion: registrations / anonymous landing sessions. Start conversion: registrations / anonymous start events. These latter two are aggregate efficiency ratios with identity limitations.
- Cancellation: latest-cancelled registration IDs / registrations. Budget utilization: spend / approved event budget, or campaign spend / current operational campaign allocation where supplied.
- Daily trends count creations and first admissions by IST date. Weekly trends use Sunday week-end sums. Growth uses `(current - previous) / previous`; zero previous totals return unavailable.
- Forecast: `min(capacity, registrations × assumed show rate + assumed walk-ins)`. Never labelled observed or statistically fitted. Target comparison is against the selected historical target for context only.
- All ratios return unavailable for a zero or missing denominator. No campaign budget is inferred from historical spend.

## Application and database architecture

Streamlit provides navigation, forms, status messages, downloads and the conversation UI. Plotly renders interactive charts. Pandas/NumPy compute fresh snapshots from SQLite. SQLite uses unique indexes on source identity columns, foreign keys on operational campaign links, validated parameterized writes and an append-only operational audit log. Source analytical tables are deliberately close to source schema for traceability; source foreign-key integrity is audited rather than enforced across every imported table. `schema.sql` includes every table and index.

```text
Unchanged workbooks -> validated import -> SQLite source tables
                                         |          |
                              analytics.snapshot    operational tables
                                         |          |
                                   dashboard    campaign/task/experiment forms
                                         \          /
                                    analyst tools
                                         |
                               proposed action -> confirmation -> saved write
```

Source tables: `event`, `targets`, `campaigns`, `daily`, `people`, `interactions`, `registrations`, `registration_history`, `checkins`. Operational tables: `campaign_plan`, `tasks`, `experiments`, `audit_log`, `metadata`.

Campaign deletion archives the operational item and preserves historical facts and linked entities. Existing source workbook bytes never change. Editing names, channel, audience or planned dates changes the working campaign table and produces an audit entry; it does not reconstruct a historical campaign-plan version. Budget and owner edits live in `campaign_plan`. Registration corrections append a dated full state, preserving earlier snapshots. Database backups use SQLite's consistent backup API.

## Analyst architecture and configuration

The default is a deterministic analytics assistant, not a trained language model. It recognizes supported intents, resolves campaign IDs/names, remembers the last campaign for follow-ups, queries current data and assembles answers from calculations. It declines unsupported questions. It does not execute model-generated SQL. Database writes accept only validated budget/task/experiment actions and require the visible confirmation button. A changed budget invalidates an old proposal to prevent stale overwrites.

Optional provider narration supplements the deterministic result. Configure environment variables (the `.env.example` file documents them; it is **not automatically loaded**):

```powershell
$env:AI_PROVIDER = 'gemini'
$env:GEMINI_MODEL = '<available model name>'
$env:GEMINI_API_KEY = '<your key>'
```

Or use `AI_PROVIDER=openai_compatible`, `AI_BASE_URL`, `AI_MODEL`, `AI_API_KEY`. `RISA_DB` selects a database path. Keys stay in server environment variables. Only aggregate tool facts are sent to the model; source person records are not sent. No external provider is required, and **live provider integration was not tested without credentials**. Provider failures retain the deterministic answer. Model narration is explicitly labelled and can make errors; deterministic evidence remains visible. Provider availability/free-tier quotas must be checked in the account; the basic app makes no paid calls.

Provider reference: [Gemini generateContent API](https://ai.google.dev/api/generate-content). UI tests use [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing).

## Demonstrate the complete workflow

1. Overview, as-of 20 April 2025: examine campaign performance. C03 has INR 337.14 CPA versus portfolio INR 142.34.
2. AI Growth Analyst: enter `Investigate C03`. It retrieves 350 registrations, 175 attributed attendees and INR 59,000 spend and proposes a controlled next-cycle test.
3. Ask `What is its budget?`. It reports the current allocation, initially unavailable unless entered.
4. Enter `Set C03 budget to INR 40000`. The assistant prepares an action; it has not saved anything.
5. Click **Confirm and save**. The operational budget persists in SQLite with an audit record. Historical spend remains INR 59,000.
6. Ask `What is its budget?`. The new answer reports INR 40,000 from a fresh database read.
7. Overview/Campaign Management now show that allocation and 147.5% spend/allocation utilization. This comparison is an operational diagnostic, not a claim that INR 40,000 was the historical allocation.
8. Enter `Create a task for C03` or `Propose an experiment for C03`, review the payload and confirm. The task/experiment appears in the relevant management page.
9. Change task status through the edit form to move it between Kanban columns. Record experiment actuals and a Scale/Iterate/Stop decision when evidence is available.

Automated tests perform this workflow on disposable databases and test changed registration data, historical snapshots, unfamiliar questions and unsupported causal/unique-reach questions. The packaged production demo database is not contaminated by test mutations.

## Deployment

A local demonstration is available by running the app. No externally hosted URL is claimed in this package. Sites hosting supports static/Worker applications, not a Python Streamlit server. This project keeps the requested Python stack.

For a shareable demo, follow the [official Community Cloud deployment instructions](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy): put this project in a GitHub repository you control, choose `app.py`, install `requirements.txt` and set optional secrets server-side. Do not publish API keys. The supplied records are synthetic. Include `source/Attendee Dataset.xlsx` so the database can initialize.

**Persistence limitation:** [Streamlit documents that local files on Community Cloud are not guaranteed to persist](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data). Use the included backup download for a temporary demo. For reliable shared deployment, run on a host with a persistent mounted volume (`RISA_DB=/persistent/risa.db`), or implement a managed database adapter. Authentication and durable cloud storage are future deployment work, not included capabilities. Free-tier availability is provider-dependent.

## Testing and limitations

See `reports/test_summary.md` for the executed result and `reports/chatbot_tests.md` for expected/actual responses. Tests cover baseline metrics, independent SQL historical-state checks, duplicate rejection, credits, attribution, campaign CRUD, task/experiment persistence, new records, stale budget proposals, confirmation gates, eight page loads and chat confirmation through Streamlit AppTest.

Known limits: no authentication, no native drag-and-drop Kanban (status edits move cards), no live ad-platform integration, no randomized exposure logger, no automated causal significance engine, no cash-receipt or ticket-revenue model, no historical campaign-plan versioning, and no unrestricted natural-language query generation in deterministic mode. New raw entities can be inserted through the documented Python/database layer; UI data corrections currently append registration statuses rather than offering a general-purpose import wizard. Experiment results are manually entered and labelled; blank means unobserved, not zero. Daily source reporting ends 20 April 2025. Selecting a later date does not turn the synthetic data into live activity.

Future work: authentication, durable hosted storage, consent and exposure logging, cohort assignment, cluster-aware experiment analysis, observed college segments, attribution sensitivity and snapshot-versioned operational plans. All original Python code was authored for this assignment. Third-party libraries provide UI, charts, tabular computation and PDF generation; no paid services were used for the core app.

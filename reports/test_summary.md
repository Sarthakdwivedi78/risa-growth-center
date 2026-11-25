# Test and verification summary

Executed on 25 November 2026. Final result: **51 tests passed, 0 failed, 0 errors** in 83.58 seconds. Machine-readable evidence: `test_results.xml`.

## Coverage
- Independent SQL historical-state comparisons at eight dates, including pre-event and target-change boundaries.
- Exact baseline: 3,625 external people; 2,800 registrations; 2,500 confirmed; 2,050 unique admitted/verified external visitors; INR 274,000 net spend.
- Duplicate ID rejection, vendor credits, zero denominators, first-touch versus registration attribution, no future outcomes and acquisition cohorts.
- Campaign create/read/update/archive, invalid negative budgets, task completion and experiment result persistence.
- Status corrections preserve earlier historical snapshots. New person/registration/status rows update both dashboard and chatbot.
- Analyst comparisons, arithmetic, allocation scenarios, evidence citations, unsupported questions, campaign-context follow-ups and stale proposal rejection.
- Confirmed budget change, task creation and experiment creation. Unconfirmed actions cannot write.
- All eight Streamlit pages, pre-history/empty date views and an AppTest chat confirmation workflow.

`chatbot_tests.md` records expected and actual answers for 20 distinct baseline questions plus diagnosis/proposal/confirmation/follow-up, modified registration data and explicit historical-date questions. No external provider key was supplied, so live Gemini or compatible-provider calls are not claimed as tested.

## Artifact and runtime checks
- Exactly three PDF pages; all final slide renders visually inspected for clipping and overlap.
- All four assignment PDF pages inspected.
- Source workbook and PDF copies match the SHA-256 hashes of the user's originals.
- Local Streamlit health endpoint returned HTTP 200. Browser inspection verified the populated dashboard and campaign filter response. Eight pages and write workflows were tested through Streamlit AppTest; no claim of exhaustive browser interaction testing.
- Database packaging uses SQLite's backup API for a consistent snapshot.
- Installed package versions are recorded in `requirements-lock.txt`.

## Non-blocking warnings and limits
The tested pandas/NumPy combination emits 69 datetime-unit deprecation warnings. All assertions pass; the lock file records this exact tested environment. Update the data-library pair and rerun historical tests before a dependency upgrade. There is no public deployment, authentication, or durable cloud database in this deliverable. Local SQLite persists across restarts. Proposed experiment outcomes are blank; dates are explicitly illustrative. No real campaign activity, statistical lift or paid API usage is fabricated.

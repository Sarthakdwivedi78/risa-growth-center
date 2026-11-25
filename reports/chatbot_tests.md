# Chatbot acceptance evidence

All answers use fresh SQLite queries. External provider narration is optional and was not tested without credentials. Tests below run against a disposable source-baseline copy.

## 1. How many registrations?

Expected: answer contains `2800`. Result: **PASS**.

Actual:

Historical snapshot 2025-04-20 (Asia/Kolkata): 3625 external people; 2800 registrations; 2500 confirmed; 183 cancelled; 2050 unique verified attendees. Confirmed-cohort attendance = 1925/2500 = 77.0%; registered-person attendance = 1925/2800 = 68.8%. 125 attendees have no registration and are excluded from those rates. Registration conversion = 77.2%; confirmation = 89.3%. Net spend INR 274,000.00; CPR INR 97.86; attributed CPA INR 142.34. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 2. How many confirmed registrations?

Expected: answer contains `2500`. Result: **PASS**.

Actual:

Historical snapshot 2025-04-20 (Asia/Kolkata): 3625 external people; 2800 registrations; 2500 confirmed; 183 cancelled; 2050 unique verified attendees. Confirmed-cohort attendance = 1925/2500 = 77.0%; registered-person attendance = 1925/2800 = 68.8%. 125 attendees have no registration and are excluded from those rates. Registration conversion = 77.2%; confirmation = 89.3%. Net spend INR 274,000.00; CPR INR 97.86; attributed CPA INR 142.34. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 3. What is actual attendance?

Expected: answer contains `2050`. Result: **PASS**.

Actual:

Historical snapshot 2025-04-20 (Asia/Kolkata): 3625 external people; 2800 registrations; 2500 confirmed; 183 cancelled; 2050 unique verified attendees. Confirmed-cohort attendance = 1925/2500 = 77.0%; registered-person attendance = 1925/2800 = 68.8%. 125 attendees have no registration and are excluded from those rates. Registration conversion = 77.2%; confirmation = 89.3%. Net spend INR 274,000.00; CPR INR 97.86; attributed CPA INR 142.34. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 4. What is our marketing expenditure?

Expected: answer contains `274,000`. Result: **PASS**.

Actual:

Historical snapshot 2025-04-20 (Asia/Kolkata): 3625 external people; 2800 registrations; 2500 confirmed; 183 cancelled; 2050 unique verified attendees. Confirmed-cohort attendance = 1925/2500 = 77.0%; registered-person attendance = 1925/2800 = 68.8%. 125 attendees have no registration and are excluded from those rates. Registration conversion = 77.2%; confirmation = 89.3%. Net spend INR 274,000.00; CPR INR 97.86; attributed CPA INR 142.34. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 5. Which campaign generated the most registrations?

Expected: answer contains `C02`. Result: **PASS**.

Actual:

Paid Social (C02): registrations = 680.00. 680 registrations, 340 attributed attendees, INR 93,000.00 net spend. Rates use matching observed cohorts and do not establish causal lift.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 6. Which campaign has the lowest cost per registration?

Expected: answer contains `C05`. Result: **PASS**.

Actual:

Student Referrals (C05): cpr = 54.29. 350 registrations, 275 attributed attendees, INR 19,000.00 net spend. Rates use matching observed cohorts and do not establish causal lift.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 7. Which campaign has the lowest cost per attendee?

Expected: answer contains `C05`. Result: **PASS**.

Actual:

Student Referrals (C05): cpa = 69.09. 350 registrations, 275 attributed attendees, INR 19,000.00 net spend. Rates use matching observed cohorts and do not establish causal lift.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 8. Which campaign has the worst conversion rate?

Expected: answer contains `C02`. Result: **PASS**.

Actual:

Paid Social (C02): conversion = 70.8%. 680 registrations, 340 attributed attendees, INR 93,000.00 net spend. Rates use matching observed cohorts and do not establish causal lift.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 9. Are we achieving targets?

Expected: answer contains `93.2%`. Result: **PASS**.

Actual:

As of 2025-04-20: 2050 / 2200 distinct external visitors = 93.2%. Registrations 2800 / 3200. Target version: Attendee revised plan. Approved budget INR 300,000.00. Net spend INR 274,000.00.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits); Targets.effective_at and target_version

## 10. Where is the biggest funnel bottleneck?

Expected: answer contains `C03`. Result: **PASS**.

Actual:

Largest measured person-count gap: registered people to admitted registered people, 875 people. Reach-to-interest is unavailable because reach is not deduplicated. Creator Partners (C03) generated 350 registrations and 175 attributed verified attendees from INR 59,000.00: CPA INR 337.14, registration-to-attendance 50.0%. Portfolio CPA is INR 142.34. Student Referrals (C05) is the lowest-CPA observed option: INR 19,000.00 / 275 = INR 69.09. Propose a capped INR 10,000 next-cycle pilot there, implying 144.74 attendees only if historical average cost repeats. This is a scenario, not incremental causal evidence. Deprioritize expansion of Creator Partners; diagnose creative-to-form and reminder drop-off first. Use randomized mutually exclusive cohorts, minimum 200 per arm for directional review, and scale only if incremental CPA <= INR 120 with a positive confidence interval. Ask to create a task or propose an experiment for C03.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 11. Where should we allocate additional budget?

Expected: answer contains `C05`. Result: **PASS**.

Actual:

Creator Partners (C03) generated 350 registrations and 175 attributed verified attendees from INR 59,000.00: CPA INR 337.14, registration-to-attendance 50.0%. Portfolio CPA is INR 142.34. Student Referrals (C05) is the lowest-CPA observed option: INR 19,000.00 / 275 = INR 69.09. Propose a capped INR 10,000 next-cycle pilot there, implying 144.74 attendees only if historical average cost repeats. This is a scenario, not incremental causal evidence. Deprioritize expansion of Creator Partners; diagnose creative-to-form and reminder drop-off first. Use randomized mutually exclusive cohorts, minimum 200 per arm for directional review, and scale only if incremental CPA <= INR 120 with a positive confidence interval. Ask to create a task or propose an experiment for C03.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 12. Who owns C01?

Expected: answer contains `Meera`. Result: **PASS**.

Actual:

Campus Ambassadors (C01): 520 registrations, 480 confirmed, 390 attributed attendees, net spend INR 42,000.00, CPR INR 80.77, CPA INR 107.69. First-touch cohort conversion 86.7%. Owner: Meera Iyer. Current operational budget: INR unavailable. Operational status: Historical. Budget is not a source fact unless supplied by the user.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits); campaign_plan.budget, owner, status (current, not historical)

## 13. Show weekly trends

Expected: answer contains `weekly`. Result: **PASS**.

Actual:

Last four observed weekly totals (week ends Sunday, Asia/Kolkata):
| date                |   Registrations |   First admission |   Identified people |   Spend |
|:--------------------|----------------:|------------------:|--------------------:|--------:|
| 2025-03-30 00:00:00 |             354 |                 0 |                 410 |   20050 |
| 2025-04-06 00:00:00 |             346 |                 0 |                 203 |   12800 |
| 2025-04-13 00:00:00 |             170 |              2050 |                 146 |   23600 |
| 2025-04-20 00:00:00 |               0 |                 0 |                   0 |   -2500 |
Registration creation and first verified admission are separate event dates. Post-event flat counts do not imply live campaign failure.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 14. What is the unique reach?

Expected: answer contains `cannot answer`. Result: **PASS**.

Actual:

The dataset cannot answer this. It has no weather, ticket revenue, bank receipts, demographic ages/genders, cross-platform reach identities, or randomized causal outcomes. Campaign association does not establish incremental impact.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 15. How much bank receipt cash collected?

Expected: answer contains `cannot answer`. Result: **PASS**.

Actual:

The dataset cannot answer this. It has no weather, ticket revenue, bank receipts, demographic ages/genders, cross-platform reach identities, or randomized causal outcomes. Campaign association does not establish incremental impact.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 16. What was the weather?

Expected: answer contains `cannot answer`. Result: **PASS**.

Actual:

The dataset cannot answer this. It has no weather, ticket revenue, bank receipts, demographic ages/genders, cross-platform reach identities, or randomized causal outcomes. Campaign association does not establish incremental impact.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 17. Tell me about quantum bananas

Expected: answer contains `cannot map`. Result: **PASS**.

Actual:

I cannot map that question reliably to the available analytics. Ask about a campaign ID, registrations, attendance, spend, targets, trends, tasks or experiments. Unavailable fields and causal effects will not be invented.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits)

## 18. What is C04 attendance?

Expected: answer contains `385`. Result: **PASS**.

Actual:

College Partnerships (C04): 450 registrations, 420 confirmed, 385 attributed attendees, net spend INR 31,000.00, CPR INR 68.89, CPA INR 80.52. First-touch cohort conversion 90.0%. Owner: Meera Iyer. Current operational budget: INR unavailable. Operational status: Historical. Budget is not a source fact unless supplied by the user.

Sources: Registrations.registration_id, person_id, campaign_id; Registration History: latest effective_at <= selected IST day; Check-ins: event_id, admitted + verified, distinct external person_id; Daily Marketing.activity_id, marketing_spend_inr (net credits); campaign_plan.budget, owner, status (current, not historical)

## 19. What tasks exist?

Expected: answer contains `tasks`. Result: **PASS**.

Actual:

5 tasks in the current database. | title                                | owner      | status   | deadline   |
|:-------------------------------------|:-----------|:---------|:-----------|
| Validate College club partnerships   | Unassigned | To Do    | 2027-01-25 |
| Validate Student referral programme  | Unassigned | To Do    | 2027-01-25 |
| Validate Campus ambassador expansion | Unassigned | To Do    | 2027-01-25 |
| Validate Performance + retargeting   | Unassigned | To Do    | 2027-01-25 |
| Validate Creator micro-pilots        | Unassigned | To Do    | 2027-01-25 |

Sources: tasks: current operational records

## 20. What experiments exist?

Expected: answer contains `experiments`. Result: **PASS**.

Actual:

5 experiments in the current database. | name                                   | metric                    |   expected | actual   | decision   |
|:---------------------------------------|:--------------------------|-----------:|:---------|:-----------|
| College club partnerships (proposed)   | Incremental registrations |        256 |          | Pending    |
| Student referral programme (proposed)  | Incremental registrations |        192 |          | Pending    |
| Campus ambassador expansion (proposed) | Incremental registrations |        144 |          | Pending    |
| Performance + retargeting (proposed)   | Incremental registrations |        128 |          | Pending    |
| Creator micro-pilots (proposed)        | Incremental registrations |         80 |          | Pending    |

Sources: experiments: current operational records

## 21–24. Full diagnosis, proposal, confirmation and follow-up workflow

Expected: C03 diagnosis uses 350 registrations, 175 attendees, INR 59,000 spend and INR 337.14 CPA; unconfirmed write rejected; confirmed budget becomes INR 40,000; follow-up and dashboard both read it. **PASS**.

Diagnosis: Creator Partners (C03) generated 350 registrations and 175 attributed verified attendees from INR 59,000.00: CPA INR 337.14, registration-to-attendance 50.0%. Portfolio CPA is INR 142.34. Student Referrals (C05) is the lowest-CPA observed option: INR 19,000.00 / 275 = INR 69.09. Propose a capped INR 10,000 next-cycle pilot there, implying 144.74 attendees only if historical average cost repeats. This is a scenario, not incremental causal evidence. Deprioritize expansion of Creator Partners; diagnose creative-to-form and reminder drop-off first. Use randomized mutually exclusive cohorts, minimum 200 per arm for directional review, and scale only if incremental CPA <= INR 120 with a positive confidence interval. Ask to create a task or propose an experiment for C03.

Proposal: Proposed operational budget for Creator Partners (C03): INR 40,000.00. Previous budget: unavailable. This does not change historical spend of INR 59,000.00. Confirm to save.

Follow-up: Creator Partners (C03): 350 registrations, 290 confirmed, 175 attributed attendees, net spend INR 59,000.00, CPR INR 168.57, CPA INR 337.14. First-touch cohort conversion 71.4%. Owner: Nisha Rao. Current operational budget: INR 40,000.00. Operational status: Historical. Budget is not a source fact unless supplied by the user.

Dashboard after save: budget INR 40,000; spend INR 59,000; utilization 147.5%. Historical source spend unchanged.

## 25. Modified registration data

Expected: 2,499 confirmed after appending one cancellation. **PASS**. Actual:

Historical snapshot 2025-04-20 (Asia/Kolkata): 3625 external people; 2800 registrations; 2499 confirmed; 184 cancelled; 2050 unique verified attendees. Confirmed-cohort attendance = 1924/2499 = 77.0%; registered-person attendance = 1925/2800 = 68.8%. 125 attendees have no registration and are excluded from those rates. Registration conversion = 77.2%; confirmation = 89.2%. Net spend INR 274,000.00; CPR INR 97.86; attributed CPA INR 142.34. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.

## 26. Date specified in natural-language question

Expected: zero actual admission before the event, no hindsight. **PASS**. Actual:

Historical snapshot 2025-04-11 (Asia/Kolkata): 3500 external people; 2800 registrations; 2500 confirmed; 183 cancelled; 0 unique verified attendees. Confirmed-cohort attendance = 0/2500 = 0.0%; registered-person attendance = 0/2800 = 0.0%. 0 attendees have no registration and are excluded from those rates. Registration conversion = 80.0%; confirmation = 89.3%. Net spend INR 276,500.00; CPR INR 98.75; attributed CPA INR unavailable. Anonymous CTR 3.1%; registrations/session 11.4%; registrations/form-start event 50.5%. Ask about a campaign ID for its owner and operational budget.
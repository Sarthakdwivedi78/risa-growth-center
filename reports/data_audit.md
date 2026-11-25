# Data audit

All 23 sheets and all populated rows were scanned. Source files remain unchanged. Timestamps imported from timezone-naive Excel cells are localized to Asia/Kolkata as specified in the source guide.

## Selection

Challenge A measures actual attendance through verified admission events. Sponsor data has 180 brands, 270 contacts, 58 opportunities, 60 latest-qualified brands and 24 latest-confirmed opportunities. It contains no receipt ledger, so confirmed cash-type partnership value cannot establish pre-festival cash collected.

## Sheet inventory and quality

### Attendee: Read me

8 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|topic|object|0|2|

|description|object|0|8|

### Attendee: Field guide

86 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|source_table|object|0|9|

|field|object|0|52|

|data_type|object|0|5|

|meaning|object|0|53|

### Attendee: Event

1 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|event_name|object|0|1|

|history_start|datetime64[ns]|0|1|

|history_end|datetime64[ns]|0|1|

|event_starts_at|datetime64[ns]|0|1|

|event_ends_at|datetime64[ns]|0|1|

|timezone|object|0|1|

|currency|object|0|1|

|fictional|bool|0|1|

### Attendee: Targets

2 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|effective_at|datetime64[ns]|0|2|

|identified_external_people_goal|int64|0|2|

|registration_goal|int64|0|2|

|unique_external_visitors_goal|int64|0|2|

|marketing_budget_inr|int64|0|2|

|target_version|object|0|2|

### Attendee: Campaigns

7 rows. Stable key: campaign_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|campaign_name|object|0|7|

|channel|object|0|7|

|target_audience|object|0|7|

|objective|object|0|7|

|owner_name|object|0|4|

|created_at|datetime64[ns]|0|1|

|planned_start_at|datetime64[ns]|0|7|

|planned_end_at|datetime64[ns]|0|1|

|campaign_id|object|0|7|

|owner_id|object|0|4|

### Attendee: Daily Marketing

483 rows. Stable key: activity_id. Duplicate keys/rows: 2. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|campaign_name|object|0|7|

|owner_name|object|0|4|

|activity_date|datetime64[ns]|0|84|

|impressions|int64|0|452|

|clicks|int64|0|121|

|reported_reach|int64|0|424|

|landing_page_sessions|int64|0|103|

|registration_starts|int64|0|32|

|marketing_spend_inr|int64|0|20|

|platform|object|0|3|

|activity_id|object|0|481|

|campaign_id|object|0|7|

|owner_id|object|0|4|

### Attendee: People

3,685 rows. Stable key: person_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|person_name|object|0|3682|

|person_type|object|0|4|

|first_seen_at|datetime64[ns]|0|108|

|first_touch_source|object|0|4|

|first_campaign_name|object|145|7|

|owner_name|object|0|4|

|person_id|object|0|3685|

|first_campaign_id|object|145|7|

|owner_id|object|0|4|

### Attendee: Interest and Engagement

11,650 rows. Stable key: interaction_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|person_name|object|0|3497|

|campaign_name|object|0|7|

|owner_name|object|0|4|

|occurred_at|datetime64[ns]|0|3149|

|event_type|object|0|8|

|detail|object|0|16|

|interaction_id|object|0|11650|

|person_id|object|0|3500|

|campaign_id|object|0|7|

|owner_id|object|0|4|

### Attendee: Registrations

2,840 rows. Stable key: registration_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|person_name|object|0|2839|

|campaign_name|object|0|7|

|owner_name|object|0|4|

|registered_at|datetime64[ns]|0|81|

|registration_id|object|0|2840|

|person_id|object|0|2840|

|campaign_id|object|0|7|

|owner_id|object|0|4|

### Attendee: Registration History

5,911 rows. Stable key: history_id. Duplicate keys/rows: 4. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|person_name|object|0|2839|

|campaign_name|object|0|7|

|owner_name|object|0|4|

|effective_at|datetime64[ns]|0|368|

|status|object|0|4|

|history_id|object|0|5907|

|registration_id|object|0|2840|

|person_id|object|0|2840|

|campaign_id|object|0|7|

|owner_id|object|0|4|

### Attendee: Check-ins

3,390 rows. Stable key: event_id. Duplicate keys/rows: 20. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|person_name|object|0|2149|

|campaign_name|object|170|7|

|owner_name|object|0|4|

|occurred_at|datetime64[ns]|0|3125|

|result|object|0|3|

|verification|object|0|2|

|source|object|0|2|

|event_id|object|0|3370|

|person_id|object|0|2150|

|registration_id|object|170|2005|

|campaign_id|object|170|7|

|owner_id|object|0|4|

### Sponsor: Read me

8 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|topic|object|0|2|

|description|object|0|8|

### Sponsor: Field guide

87 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|source_table|object|0|10|

|field|object|0|53|

|data_type|object|0|5|

|meaning|object|0|54|

### Sponsor: Event

1 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|event_name|object|0|1|

|history_start|datetime64[ns]|0|1|

|history_end|datetime64[ns]|0|1|

|event_starts_at|datetime64[ns]|0|1|

|event_ends_at|datetime64[ns]|0|1|

|timezone|object|0|1|

|currency|object|0|1|

|fictional|bool|0|1|

### Sponsor: Targets

2 rows. Stable key: metadata / effective_at for targets. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|effective_at|datetime64[ns]|0|2|

|qualified_brands_goal|int64|0|2|

|confirmed_partnerships_goal|int64|0|2|

|target_version|object|0|2|

### Sponsor: Brands

180 rows. Stable key: brand_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|brand_name|object|0|180|

|industry|object|0|6|

|owner_name|object|0|3|

|created_at|datetime64[ns]|0|75|

|brand_id|object|0|180|

|owner_id|object|0|3|

### Sponsor: Sponsor contacts

270 rows. Stable key: contact_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|contact_name|object|0|268|

|job_title|object|0|2|

|brand_name|object|0|180|

|created_at|datetime64[ns]|0|137|

|contact_id|object|0|270|

|brand_id|object|0|180|

### Sponsor: Sponsor campaigns

6 rows. Stable key: sponsor_campaign_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|campaign_name|object|0|6|

|channel|object|0|4|

|objective|object|0|6|

|audience|object|0|6|

|owner_name|object|0|3|

|planned_start_at|datetime64[ns]|0|1|

|planned_end_at|datetime64[ns]|0|1|

|created_at|datetime64[ns]|0|1|

|sponsor_campaign_id|object|0|6|

|owner_id|object|0|3|

### Sponsor: Sponsor interactions

953 rows. Stable key: interaction_id. Duplicate keys/rows: 3. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|brand_name|object|0|180|

|contact_name|object|0|200|

|campaign_name|object|0|6|

|channel|object|0|4|

|event_type|object|0|8|

|outcome|object|0|11|

|summary|object|0|11|

|occurred_at|datetime64[ns]|0|280|

|interaction_id|object|0|950|

|attempt_id|object|0|370|

|origin_interaction_id|object|373|370|

|brand_id|object|0|180|

|contact_id|object|0|202|

|sponsor_campaign_id|object|0|6|

|owner_id|object|0|3|

### Sponsor: Brand qualification

434 rows. Stable key: history_id. Duplicate keys/rows: 1. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|brand_name|object|0|180|

|qualification_status|object|0|5|

|reason|object|0|9|

|source_campaign_name|object|0|6|

|effective_at|datetime64[ns]|0|234|

|history_id|object|0|433|

|brand_id|object|0|180|

|sponsor_campaign_id|object|0|6|

### Sponsor: Partner opportunities

58 rows. Stable key: opportunity_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|opportunity_name|object|0|58|

|brand_name|object|0|57|

|primary_contact_name|object|0|57|

|originating_campaign_name|object|0|6|

|support_type|object|0|2|

|created_at|datetime64[ns]|0|41|

|opportunity_id|object|0|58|

|brand_id|object|0|57|

|primary_contact_id|object|0|57|

|sponsor_campaign_id|object|0|6|

### Sponsor: Opportunity history

230 rows. Stable key: history_id. Duplicate keys/rows: 2. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|opportunity_name|object|0|58|

|brand_name|object|0|57|

|stage|object|0|7|

|proposed_value_inr|int64|0|21|

|confirmed_value_inr|int64|0|16|

|owner_name|object|0|3|

|effective_at|datetime64[ns]|0|67|

|history_id|object|0|228|

|opportunity_id|object|0|58|

|brand_id|object|0|57|

|owner_id|object|0|3|

### Sponsor: Sponsor activations

3 rows. Stable key: activation_id. Duplicate keys/rows: 0. Conflicting key payloads: 0.

|Column|Observed type|Missing|Distinct|

|---|---|---:|---:|

|brand_name|object|0|3|

|opportunity_name|object|0|3|

|attendee_campaign_name|object|0|3|

|activation_note|object|0|1|

|linked_at|datetime64[ns]|0|3|

|activation_id|object|0|3|

|brand_id|object|0|3|

|opportunity_id|object|0|3|

|attendee_campaign_id|object|0|3|

## Relationships

Campaigns 1:N Daily Marketing / Registrations / Interactions. People 1:N Registrations / Interactions / Check-ins. Registrations 1:N full-state history. Check-ins.event_id is an admission-event key, not a festival identity. Sponsor brands 1:N contacts and opportunities; opportunities 1:N history. Activations link opportunities to attendee campaigns. Owner IDs are labels shared across sources; no separate owner table is supplied.

|Reference|Orphan nonblank IDs|

|---|---:|

|Attendee: Registrations.person_id to People.person_id|0|

|Attendee: Registrations.campaign_id to Campaigns.campaign_id|0|

|Attendee: Registration History.registration_id to Registrations.registration_id|0|

|Attendee: Check-ins.registration_id to Registrations.registration_id|0|

|Attendee: Check-ins.person_id to People.person_id|0|

|Attendee: Interest and Engagement.person_id to People.person_id|0|

|Attendee: Interest and Engagement.campaign_id to Campaigns.campaign_id|0|

|Attendee: People.first_campaign_id to Campaigns.campaign_id|0|

|Attendee: Daily Marketing.campaign_id to Campaigns.campaign_id|0|

|Sponsor: Sponsor contacts.brand_id to Brands.brand_id|0|

|Sponsor: Sponsor interactions.brand_id to Brands.brand_id|0|

|Sponsor: Sponsor interactions.contact_id to Sponsor contacts.contact_id|0|

|Sponsor: Sponsor interactions.sponsor_campaign_id to Sponsor campaigns.sponsor_campaign_id|0|

|Sponsor: Brand qualification.brand_id to Brands.brand_id|0|

|Sponsor: Partner opportunities.brand_id to Brands.brand_id|0|

|Sponsor: Partner opportunities.primary_contact_id to Sponsor contacts.contact_id|0|

|Sponsor: Opportunity history.opportunity_id to Partner opportunities.opportunity_id|0|

|Sponsor: Sponsor activations.opportunity_id to Partner opportunities.opportunity_id|0|

|Sponsor activations.attendee_campaign_id to Attendee Campaigns|0|

## Interpretation and consistency

{"Registration History": {"person_mismatches": 0, "campaign_mismatches": 0}, "Check-ins": {"person_mismatches": 0, "campaign_mismatches": 0}, "temporal": {"registrations_before_identity": 0, "history_before_registration": 0}}

Attendee duplicate source IDs: 2 activity_id, 4 history_id, 20 admission event_id. Sponsor duplicates: 3 interaction_id, 1 qualification history_id, 2 opportunity history_id. All identical payloads. Remove import copies only.

Three repeated display names identify different people; never merge them. People include 3,625 external, 40 internal, 10 staff and 10 test identities. There are 2,840 total registrations but only 2,800 external registrations.

145 people lack first-campaign attribution; 170 raw check-in rows lack registration/campaign attribution. Missing IDs here are documented walk-in/access paths, not automatic data corruption. Sponsor root touches legitimately omit origin_interaction_id (373 rows).

Negative marketing entries total INR -6,500 and represent vendor credits. Net spend is INR 274,000. No conflicting stable-key payloads were found.

Campaign budgets, venue capacity, student ages/college membership, unique cross-platform reach, ticket revenue, experimental holdouts and bank receipts are missing. Do not fill these with invented facts.

## Baseline, 20 April 2025 IST

{
  "identified_external_people": 3625,
  "registrations": 2800,
  "confirmed": 2500,
  "cancelled": 183,
  "waitlisted": 88,
  "unknown_status": 0,
  "attendees": 2050,
  "registered_attendees": 1925,
  "eligible_attendees": 1925,
  "walk_ins": 125,
  "spend": 274000.0,
  "registration_conversion": 0.7724137931034483,
  "confirmation_rate": 0.8928571428571429,
  "attendance_rate": 0.77,
  "registration_to_attendance": 0.6875,
  "cancellation_rate": 0.06535714285714286,
  "cpr": 97.85714285714286,
  "cpa": 142.33766233766235,
  "all_visitor_cost": 133.65853658536585,
  "ctr": 0.03116572644713634,
  "landing_conversion": 0.11361330898762427,
  "start_conversion": 0.5046863734679163,
  "target_achievement": 0.9318181818181818,
  "budget_utilization": 0.9133333333333333,
  "identified_interest": 3500,
  "interest_to_registration": 0.8
}

| campaign_id   | campaign             | channel          | owner        | budget   | status     |   people |   registrations |   confirmed |   attendees |   spend |      cpr |      cpa |   conversion |   reg_attendance | budget_utilization   |   deleted | performance   |
|:--------------|:---------------------|:-----------------|:-------------|:---------|:-----------|---------:|----------------:|------------:|------------:|--------:|---------:|---------:|-------------:|-----------------:|:---------------------|----------:|:--------------|
| C01           | Campus Ambassadors   | ambassadors      | Meera Iyer   |          | Historical |      600 |             520 |         480 |         390 |   42000 |  80.7692 | 107.692  |     0.866667 |         0.75     |                      |         0 | Efficient     |
| C02           | Paid Social          | paid_social      | Arjun Verma  |          | Historical |      960 |             680 |         580 |         340 |   93000 | 136.765  | 273.529  |     0.708333 |         0.5      |                      |         0 | Review        |
| C03           | Creator Partners     | creators         | Nisha Rao    |          | Historical |      490 |             350 |         290 |         175 |   59000 | 168.571  | 337.143  |     0.714286 |         0.5      |                      |         0 | Review        |
| C04           | College Partnerships | college_partners | Meera Iyer   |          | Historical |      500 |             450 |         420 |         385 |   31000 |  68.8889 |  80.5195 |     0.9      |         0.855556 |                      |         0 | Efficient     |
| C05           | Student Referrals    | referrals        | Dev Malhotra |          | Historical |      410 |             350 |         320 |         275 |   19000 |  54.2857 |  69.0909 |     0.853659 |         0.785714 |                      |         0 | Efficient     |
| C06           | Organic Search       | organic          | Arjun Verma  |          | Historical |      290 |             250 |         225 |         195 |   14000 |  56      |  71.7949 |     0.862069 |         0.78     |                      |         0 | Efficient     |
| C07           | Community Groups     | community        | Nisha Rao    |          | Historical |      250 |             200 |         185 |         165 |   16000 |  80      |  96.9697 |     0.8      |         0.825    |                      |         0 | Efficient     |

## Bottlenecks

2,800 registered people produced 1,925 verified registered visitors: 68.75%. This loses 875 people between registration and admission. There are 825 external identities without a registration, including 125 admitted walk-ins. Latest confirmation-to-admission and all-registration conversion use different denominators.

Creator Partners has CPA INR 337.14 and registration-to-attendance 50%; Paid Social also converts 50% of registrants to attendance. Referrals CPA is INR 69.09, College Partnerships INR 80.52. These observational differences suggest hypotheses, not causal spend-response estimates.

## Original file SHA-256

{
  "Attendee Dataset.xlsx": "d63f3e013e9a823e28ab0a0587703b2ed4344e443ade185606c2ce3427203469",
  "Sponsor Dataset.xlsx": "12e3db14a56dacb3741b2bc67eeff3e74aff7c9fac0fcf7194800d195608b080"
}
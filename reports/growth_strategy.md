# Growth strategy and assumptions

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

### 1. College club partnerships
- campaign: C04
- gross: 320
- net: 256
- budget: 70000
- ice: 8 x 8 x 7 = 448
- audience: Club and competition participants
- resource: 1 partnerships lead + 10 club captains
- timing: T-6 to T-1 weeks
- dependency: College permission and group itinerary
- risk: Group overlap, transport no-shows
- test: Randomize 20 matched clubs to itinerary + group RSVP or standard outreach
- scale: >=12.8 incremental registrations/club and CPA <= INR 120
- stop: <6 incremental registrations/club or CPA > INR 180
- fix: Replace inactive clubs; stagger transport and reminders
- leading: Active clubs, RSVP-to-confirmed rate
- Expected base incremental attendees: 256 net registrations x 75% = 192. This acquisition contribution excludes the shared 175-person attendance improvement.

### 2. Student referral programme
- campaign: C05
- gross: 240
- net: 192
- budget: 45000
- ice: 8 x 8 x 6 = 384
- audience: Friends of consented registrants
- resource: 1 growth operator + developer
- timing: T-5 to T-1 weeks
- dependency: Unique referral codes and admission validation
- risk: Self-referral fraud and existing-user overlap
- test: 50/50 person-level invitation incentive holdout; reward verified admission only
- scale: >=0.20 new registrations/inviter and CPA <= INR 100
- stop: <0.08 registrations/inviter or fraud >5%
- fix: Cap rewards; block self-referrals; shorten invitation steps
- leading: Unique eligible invites, new-identity share
- Expected base incremental attendees: 192 net registrations x 75% = 144. This acquisition contribution excludes the shared 175-person attendance improvement.

### 3. Campus ambassador expansion
- campaign: C01
- gross: 180
- net: 144
- budget: 80000
- ice: 7 x 7 x 6 = 294
- audience: Students at nearby campuses
- resource: 1 lead + 20 ambassadors
- timing: T-6 to T-1 weeks
- dependency: Campus access and weekly reporting
- risk: Uneven activation and unsupported signups
- test: Randomize 20 campus clusters to ambassador kit vs usual communication
- scale: >=7.2 incremental registrations/ambassador and CPA <= INR 120
- stop: <3 registrations/ambassador or CPA > INR 180
- fix: Coach or replace inactive reps; focus nearby campuses
- leading: Active ambassadors, verified signups per rep
- Expected base incremental attendees: 144 net registrations x 75% = 108. This acquisition contribution excludes the shared 175-person attendance improvement.

### 4. Performance + retargeting
- campaign: C02
- gross: 160
- net: 128
- budget: 65000
- ice: 6 x 6 x 5 = 180
- audience: Consented form abandoners; exclude confirmed people
- resource: 1 marketer + shared analyst
- timing: T-4 to T-1 weeks
- dependency: Consent, suppression list and conversion events
- risk: Cannibalization, saturation and weak form completion
- test: Randomized user holdout with equal creative exposure rules
- scale: >=5 pp form-completion lift and incremental CPA <= INR 140
- stop: <=0 pp lift or incremental CPA > INR 210
- fix: Pause audience; repair form; cap frequency at 3/week
- leading: Unique form starts, completion, frequency
- Expected base incremental attendees: 128 net registrations x 75% = 96. This acquisition contribution excludes the shared 175-person attendance improvement.

### 5. Creator micro-pilots
- campaign: C03
- gross: 100
- net: 80
- budget: 20000
- ice: 5 x 4 x 4 = 80
- audience: Local niche student communities
- resource: 1 creator manager + 2 creators
- timing: T-4 to T-2 weeks
- dependency: Verified audience geography and trackable links
- risk: Vanity reach and poor attendance intent
- test: Two matched audience cells, creator content vs event information
- scale: >=40 incremental registrations/creator and CPA <= INR 160
- stop: <15 registrations/creator or CPA > INR 240
- fix: Change programme hook once, then stop broad creator buys
- leading: Qualified click-to-start and verified new identities
- Expected base incremental attendees: 80 net registrations x 75% = 60. This acquisition contribution excludes the shared 175-person attendance improvement.

## Monitoring and experiment discipline
Incremental CPA means (treatment cost minus comparable control cost) / incremental verified visitors, not the whole initiative allocation divided by incremental visitors. Pilot cash caps within the all-in initiative budgets are INR 15,000 for clubs, 10,000 for referrals, 10,000 for ambassadors, 10,000 for paid retargeting and 5,000 for creators (INR 50,000 total). The remaining INR 230,000 of allocated budget sustains baseline delivery and subsequent gated scaling. These are proposed allocations; record actual treatment/control cost before judging the thresholds. Pilot effects are extrapolated to full deployment only after valid evidence and capacity checks.

Review daily cohort counts, net spend, completed registrations, cancellations and explicit opt-outs. Review matched cluster outcomes weekly. Acquisition KPI thresholds are operating gates, not proof of significance. CPA gates refer to incremental attendees measured against a randomized holdout; pre-event proxies use registrations x a labelled 75% show assumption. Do not replace missing causal lift with attributed historical CPA.

Scale only after two consecutive review windows pass the strategy-specific volume and cost gates, with positive lower 95% confidence bound on incremental outcome and a valid pre-registered analysis. For initial directional review require at least 200 eligible people per arm for individual tests, or 10 clusters per arm for club/campus tests. These small pilot floors do NOT establish adequate statistical power. At baseline 68.75% attendance, detecting +6.25 percentage points with two-sided 5% alpha/80% power needs roughly 850–900 people per arm before cluster/design effects. Do not claim significance at 200/arm. Defer scale if underpowered; pool comparable waves or treat results as directional.

For binary outcomes use a two-proportion interval/test; for clubs/campuses use cluster-level randomization inference or cluster-robust uncertainty. Freeze a 14-day window, primary metric and exclusion rules before launch. Avoid repeatedly testing each day. Adjust multiple comparisons across five tests (Holm) before claiming portfolio causal lift. Stop immediately for consent failures or >5% invalid referral identities. Otherwise stop after two failed review windows or the pilot budget cap. Between success and failure gates, iterate one variable and rerun with a new locked cohort. Missing exposure or identity logs means fix instrumentation before a decision.

The thresholds reflect a base overall visitor cost of INR 107 and a proposed ceiling of INR 120 for scalable grassroots pilots. Paid/creator gates allow discovery premiums of INR 140/160, with lower budget caps. Failure cost bands are 1.5x the scale gate (180/210/240). Referral fraud caps and per-rep volumes are proposed operational guardrails. Trial cost is part of each initiative allocation. Reserve INR 20,000, never exceed total INR 300,000 without explicit new approval.

Dashboard: monitor registrations and first admissions by IST date, registered-cohort attendance, target vintage, attributed campaign CPA and actual spend vs current operational allocation. AI reads the latest database, cites fields/IDs, proposes a diagnosis and prepares an action. User confirmation is required to save. It does not infer causality or automatically scale spend. Persist experiment actuals, decision and evidence notes manually; no random-assignment or significance engine is claimed in this version.

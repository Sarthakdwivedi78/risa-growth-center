CREATE TABLE "event" (
"event_name" TEXT,
  "history_start" TEXT,
  "history_end" TEXT,
  "event_starts_at" TEXT,
  "event_ends_at" TEXT,
  "timezone" TEXT,
  "currency" TEXT,
  "fictional" INTEGER
);

CREATE TABLE "targets" (
"effective_at" TEXT,
  "identified_external_people_goal" INTEGER,
  "registration_goal" INTEGER,
  "unique_external_visitors_goal" INTEGER,
  "marketing_budget_inr" INTEGER,
  "target_version" TEXT
);

CREATE TABLE "campaigns" (
"campaign_name" TEXT,
  "channel" TEXT,
  "target_audience" TEXT,
  "objective" TEXT,
  "owner_name" TEXT,
  "created_at" TEXT,
  "planned_start_at" TEXT,
  "planned_end_at" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_campaigns" ON "campaigns"("campaign_id");

CREATE TABLE "daily" (
"campaign_name" TEXT,
  "owner_name" TEXT,
  "activity_date" TEXT,
  "impressions" INTEGER,
  "clicks" INTEGER,
  "reported_reach" INTEGER,
  "landing_page_sessions" INTEGER,
  "registration_starts" INTEGER,
  "marketing_spend_inr" INTEGER,
  "platform" TEXT,
  "activity_id" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_daily" ON "daily"("activity_id");

CREATE TABLE "people" (
"person_name" TEXT,
  "person_type" TEXT,
  "first_seen_at" TEXT,
  "first_touch_source" TEXT,
  "first_campaign_name" TEXT,
  "owner_name" TEXT,
  "person_id" TEXT,
  "first_campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_people" ON "people"("person_id");

CREATE TABLE "interactions" (
"person_name" TEXT,
  "campaign_name" TEXT,
  "owner_name" TEXT,
  "occurred_at" TEXT,
  "event_type" TEXT,
  "detail" TEXT,
  "interaction_id" TEXT,
  "person_id" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_interactions" ON "interactions"("interaction_id");

CREATE TABLE "registrations" (
"person_name" TEXT,
  "campaign_name" TEXT,
  "owner_name" TEXT,
  "registered_at" TEXT,
  "registration_id" TEXT,
  "person_id" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_registrations" ON "registrations"("registration_id");

CREATE TABLE "registration_history" (
"person_name" TEXT,
  "campaign_name" TEXT,
  "owner_name" TEXT,
  "effective_at" TEXT,
  "status" TEXT,
  "history_id" TEXT,
  "registration_id" TEXT,
  "person_id" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_registration_history" ON "registration_history"("history_id");

CREATE TABLE "checkins" (
"person_name" TEXT,
  "campaign_name" TEXT,
  "owner_name" TEXT,
  "occurred_at" TEXT,
  "result" TEXT,
  "verification" TEXT,
  "source" TEXT,
  "event_id" TEXT,
  "person_id" TEXT,
  "registration_id" TEXT,
  "campaign_id" TEXT,
  "owner_id" TEXT
);

CREATE UNIQUE INDEX "pk_checkins" ON "checkins"("event_id");

CREATE TABLE campaign_plan(campaign_id TEXT PRIMARY KEY REFERENCES campaigns(campaign_id), budget REAL CHECK(budget>=0), status TEXT NOT NULL DEFAULT 'Historical', owner TEXT, notes TEXT DEFAULT '', deleted INTEGER DEFAULT 0);

CREATE TABLE tasks(id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT, owner TEXT, priority TEXT, deadline TEXT, status TEXT, campaign_id TEXT REFERENCES campaigns(campaign_id));

CREATE TABLE experiments(id TEXT PRIMARY KEY, name TEXT NOT NULL, hypothesis TEXT, audience TEXT, campaign_id TEXT REFERENCES campaigns(campaign_id), metric TEXT, expected REAL, budget REAL CHECK(budget>=0), start_date TEXT, end_date TEXT, actual REAL, decision TEXT, notes TEXT);

CREATE TABLE audit_log(id INTEGER PRIMARY KEY, recorded_at TEXT, entity TEXT, entity_id TEXT, action TEXT, payload TEXT);

CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);

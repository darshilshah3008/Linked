import sqlite3

conn = sqlite3.connect("data/app.db")
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

print("=== Tables in data/app.db ===\n")
for (name,) in tables:
    count = c.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"  {name}: {count} rows")

print("\n=== Sample Leads (top 3) ===\n")
for row in c.execute("SELECT id, title, company, relevance_score, status FROM leads ORDER BY relevance_score DESC LIMIT 3"):
    print(f"  [{row[0]}] {row[1]} @ {row[2]} — score: {row[3]}, status: {row[4]}")

print("\n=== Companies ===\n")
for row in c.execute("SELECT id, name, embedded_relevance FROM companies"):
    print(f"  [{row[0]}] {row[1]} — relevance: {row[2]}")

print("\n=== Outreach Messages ===\n")
for row in c.execute("SELECT id, message_type, approval_status FROM outreach_messages"):
    print(f"  [{row[0]}] {row[1]} — {row[2]}")

print("\n=== Recent Activity Logs ===\n")
for row in c.execute("SELECT agent_name, action_type, summary FROM activity_logs ORDER BY created_at DESC LIMIT 5"):
    print(f"  {row[0]}: {row[1]} — {row[2]}")

conn.close()

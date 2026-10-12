from db import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
print("Connected! users count =", cursor.fetchone()[0])
conn.close()
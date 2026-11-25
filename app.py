import sqlite3, json, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("create table if not exists users(id int, name text, company text)")
cur.execute("create table if not exists trips(id int, user_id int, company text, cost int, status text)")
if cur.execute("select count(*) from users").fetchone()[0] == 0:
    cur.execute("insert into users values (1,'rahul','abc'),(2,'priya','xyz'),(3,'amit','abc')")
    cur.execute("insert into trips values (1,1,'abc',100,'done'),(2,2,'xyz',500,'cancelled'),(3,3,'abc',200,'done')")
    conn.commit()

def get_sql(q, comp):
    q = q.lower()
    if "user" in q or "employee" in q:
        return "select * from users"
    if "trip" in q:
        return "select * from trips"
    if "cost" in q:
        return "select cost from trips"
    if "sql:" in q:
        return q.split("sql:")[1]
    return "select * from trips where company='" + str(comp) + "'"

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = """
        <html><body bgcolor="#ffffcc">
        <marquee><h1>Transport AI Chatbot</h1></marquee>
        <form method="POST" action="/ask">
        Question: <input name="q" size="40"><br><br>
        Company: <input name="c" value="abc"><br><br>
        <button type="submit">Submit</button>
        </form>
        </body></html>
        """
        self.wfile.write(page.encode())

    def do_POST(self):
        l = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(l).decode()
        if "{" in raw:
            d = json.loads(raw)
            q = d.get("question", "")
            c = d.get("company", "abc")
        else:
            p = urllib.parse.parse_qs(raw)
            q = p.get("q", [""])[0]
            c = p.get("c", ["abc"])[0]
        s = get_sql(q, c)
        try:
            r = cur.execute(s).fetchall()
            conn.commit()
            out = {"ans": r, "query": s}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(out).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"err": str(e)}).encode())

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 5000), H).serve_forever()

from flask import Flask, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.getenv("DB_HOST")
app.config["MYSQL_USER"] = os.getenv("DB_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("DB_NAME")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def home():
    return """
    <h1>Flask DevOps Project</h1>
    <p>App is connected with AWS RDS MySQL.</p>
    <a href="/messages">View Messages</a>
    """

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO messages (name, message) VALUES (%s, %s)",
            (name, message)
        )
        mysql.connection.commit()
        cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = cur.fetchall()
    cur.close()

    html = """
    <h1>Messages</h1>
    <form method="POST">
        <input name="name" placeholder="Your name" required>
        <br><br>
        <textarea name="message" placeholder="Your message" required></textarea>
        <br><br>
        <button type="submit">Save Message</button>
    </form>
    <hr>
    """

    for msg in messages:
        html += f"<p><b>{msg['name']}</b>: {msg['message']} <small>{msg['created_at']}</small></p>"

    return html

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

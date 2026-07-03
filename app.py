from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Flask DevOps Project</h1>
    <p>Local app is running successfully.</p>
    """

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

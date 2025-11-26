from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    # Listen on all interfaces, port 5000 (inside container)
    app.run(host="0.0.0.0", port=5000, debug=True)

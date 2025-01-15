from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/terms-of-service")
def terms_of_service():
    return render_template("terms_of_service.html")


if __name__ == "__main__":
    app.run(debug=True)

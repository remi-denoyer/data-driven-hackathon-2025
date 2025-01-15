from dotenv import load_dotenv
from flask import Flask, render_template
import plotly.express as px

# Hardcoded data
data = [
    {"name": "TechCorp", "category": "Technology", "size": 500, "funding": 100},
    {"name": "BioLife", "category": "Healthcare", "size": 300, "funding": 200},
    {"name": "EcoWorld", "category": "Environment", "size": 150, "funding": 50},
    {"name": "FinSecure", "category": "Finance", "size": 400, "funding": 250},
    {"name": "MediCare", "category": "Healthcare", "size": 350, "funding": 180},
    {"name": "CleanTech", "category": "Environment", "size": 220, "funding": 120},
    {"name": "SafeInvest", "category": "Finance", "size": 270, "funding": 300},
    {"name": "GreenFuture", "category": "Environment", "size": 180, "funding": 90},
    {"name": "TechSolutions", "category": "Technology", "size": 600, "funding": 500},
    {"name": "HealthBridge", "category": "Healthcare", "size": 240, "funding": 140},
]

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/map")
def display_map():
    # Create treemap using Plotly
    fig = px.treemap(
        data,
        path=["category", "name"],  # Define hierarchy
        values="size",  # Define size of blocks
        color="funding",  # Color by funding
        title="Company Tree Map",  # Title of the tree map
        color_continuous_scale="Viridis",
    )

    # Convert Plotly graph to HTML
    map_html = fig.to_html(full_html=False)
    return render_template("map.html", map_html=map_html)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/terms-of-service")
def terms_of_service():
    return render_template("terms_of_service.html")


if __name__ == "__main__":
    app.run(debug=True)

from dotenv import load_dotenv
from flask import Flask, render_template
import plotly.express as px

# Data
data = [
    {
        "category": "Technology",
        "company": "TechCorp",
        "employees": 500,
        "growth": 0.15,
    },
    {
        "category": "Technology",
        "company": "CodeLabs",
        "employees": 300,
        "growth": -0.05,
    },
    {
        "category": "Healthcare",
        "company": "MediLife",
        "employees": 400,
        "growth": 0.25,
    },
    {
        "category": "Healthcare",
        "company": "BioHealth",
        "employees": 200,
        "growth": -0.10,
    },
    {
        "category": "Finance",
        "company": "FinTrust",
        "employees": 350,
        "growth": 0.05,
    },
    {
        "category": "Finance",
        "company": "SafeBank",
        "employees": 150,
        "growth": 0.10,
    },
    {
        "category": "Environment",
        "company": "GreenTech",
        "employees": 450,
        "growth": -0.20,
    },
    {
        "category": "Environment",
        "company": "EcoWorld",
        "employees": 250,
        "growth": 0.30,
    },
]

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/map")
def display_map():
    fig = px.treemap(
        data,
        path=["category", "company"],  # Hierarchical levels: category > company
        values="employees",  # Block size determined by headcount
        color="growth",  # Color determined by growth
        color_continuous_scale=["green", "yellow", "red"],  # Custom green-to-red scale
        title="Company Dynamism Treemap",
    )

    # Enhance layout and styling
    fig.update_layout(
        font=dict(
            family="Arial, sans-serif",  # Modern font
            size=20,  # Larger font size
            color="white",  # Font color for dark background
        ),
        title=dict(
            font=dict(size=28),  # Larger title font
            x=0.5,  # Center the title
            xanchor="center",
        ),
        paper_bgcolor="black",  # Dark background
        plot_bgcolor="black",  # Dark plot background
        margin=dict(t=50, l=25, r=25, b=25),  # Reduce margins for better space usage
    )

    # Update traces for centered text and percentages
    fig.update_traces(
        textinfo="label+text",  # Display company name and custom text
        texttemplate=("%{label}<br>" "Size: %{value}"),
        textfont=dict(size=16),  # Larger text inside rectangles
        textposition="middle center",  # Center the text in each rectangle
        marker=dict(
            line=dict(color="black", width=1),  # Subtle borders for contrast
            cornerradius=8,  # Slightly rounded corners
        ),
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

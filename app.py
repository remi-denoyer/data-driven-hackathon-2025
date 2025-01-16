from dotenv import load_dotenv
from flask import Flask, render_template
import plotly.express as px
import json
from services.get_competitors_enriched import get_competitors_enriched
from services.open_ai import generate_market_analysis

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

def field_selector(data_array: list, fields: list) -> list:
    """
    Filter JSON objects to only include specified fields.

    Args:
        data_array (list): List of dictionaries containing data
        fields (list): List of field names to keep

    Returns:
        list: List of filtered dictionaries containing only specified fields
    """
    return [{key: item[key] for key in fields if key in item} for item in data_array]

# Load data from external JSON file
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/orchestrator/<domain>")
@app.route("/orchestrator/<domain>/<fields>")
def orchestrator(domain: str, fields: str = "name,company_type,funding_total"):
    companies = get_competitors_enriched(domain)
    analysis = generate_market_analysis(field_selector(companies, ["name",
                                                                   "website",
                                                                   "customer_type",
                                                                   "description",
                                                                   "external_description",
                                                                   "funding_stage",
                                                                   "funding_total",
                                                                   "country",
                                                                   "headcount",
                                                                   "ownership_status",
                                                                   "company_type",
                                                                   "stage",
                                                                   "highlights",
                                                                   "traction_metrics"]))

    # Join companies and analysis based on domain key
    enriched_companies = []
    companies_dict = {company["website"]: company for company in companies}
    analysis_dict = {company["website"]: company for company in analysis["companies"] if not company["outlier"]}

    # Merge data for matching domains
    for website in set(companies_dict.keys()) | set(analysis_dict.keys()):
        company_data = companies_dict.get(website, {})
        analysis_data = analysis_dict.get(website, {})
        merged = {**company_data, **analysis_data}
        enriched_companies.append(merged)

    # Split fields string into list
    fields_list = fields.split(",")
    return field_selector(enriched_companies, fields_list)

@app.route("/map")
def display_map():
    data = load_data()

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
        ),
        title=dict(
            font=dict(size=28),  # Larger title font
            x=0.5,  # Center the title
            xanchor="center",
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        margin=dict(t=50, l=25, r=25, b=25),  # Reduce margins for better space usage
    )

    # Update traces for centered text and percentages
    fig.update_traces(
        textinfo="label+text",  # Display company name and custom text
        texttemplate=("%{label}<br>" "Size: %{value}"),
        textfont=dict(size=16),  # Larger text inside rectangles
        textposition="middle center",  # Center the text in each rectangle
        marker=dict(line=dict(color="black", width=1)),  # Subtle borders for contrast
    )

    # Convert Plotly graph to HTML
    map_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
    return render_template("map.html", map_html=map_html)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/terms-of-service")
def terms_of_service():
    return render_template("terms_of_service.html")


if __name__ == "__main__":
    app.run(debug=True)

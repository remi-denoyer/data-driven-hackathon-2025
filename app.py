from dotenv import load_dotenv
from flask import Flask, render_template
import plotly.express as px
from services.get_competitors_enriched import get_competitors_enriched
from services.open_ai import generate_market_analysis

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

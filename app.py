from dotenv import load_dotenv
from flask import Flask, render_template, request, session
import json
import os

# Your service imports
from services.companies import list_companies
from services.figures import create_tree_map

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flask session management


# Load data from external JSON file
def load_data_example():
    with open("data.example.json", "r") as file:
        return json.load(file)


def load_data(domain="perplexity.ai"):
    # Returns a list of companies from your external service
    return list_companies(domain)


@app.route("/")
def display_map():
    """
    Main route for displaying the treemap and side panel data.

    This function loads company data from an external service or uses example data,
    generates a Plotly tree map figure, and renders the template with the map and
    company details in the side panel.

    The function takes the following parameters from the URL query string:

    - metric (str): The metric to display in the treemap, e.g. headcount or funding_total
    - search (str): The search term to search for a company or domain
    - selected_company (str): The name of the company selected in the treemap

    The function returns an HTML page with a treemap and side panel with company details.
    """
    # Get the metric, search term, and selected company from the URL
    metric = request.args.get("metric", "headcount")
    search_term = request.args.get("search", None)
    selected_company = request.args.get("selected_company", None)

    # initialize session
    if "data" not in session.keys() or "search_term" not in session.keys():
        session["data"] = []
        session["search_term"] = ""

    # If a search term is provided and it's different from the previous one, load data from your services
    if search_term is not None and search_term != session.get("search_term", ""):
        # Load data from your services
        data = load_data(domain=search_term)
    else:
        # Load data from session storage
        data = session["data"]

    session["data"] = data
    session["search_term"] = search_term

    # If a company is selected, find its details in the data
    selected_company_data = None
    print(selected_company)
    if selected_company and len(data) > 0:
        selected_company_data = next(
            (
                entry
                for entry in data
                if entry["name"].lower() == selected_company.lower()
            ),
            None,
        )
        print(selected_company_data)

    # Generate the Plotly tree map figure based on the selected metric
    if len(data) > 0:
        fig = create_tree_map(data, search_term, metric)
        map_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
    else:
        map_html = None

    # Render the template
    return render_template(
        "index.html",
        map_html=map_html,
        current_metric=metric,
        search_term=search_term,
        selected_company_data=selected_company_data,
        # Pass the data if you want to do client-side re-rendering, e.g.:
        # all_companies=data
    )

if __name__ == "__main__":
    # Run in debug mode for development
    if os.environ.get("FLASK_ENV") == "development":
        debug = True
    else:
        debug = False
    app.run(debug=debug, port=os.environ.get("PORT", 5000))

from dotenv import load_dotenv
from flask import Flask, render_template, request
import json

# Your service imports
from services.companies import list_companies
from services.figures import create_tree_map

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)


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
    """
    # Get the metric, search term, and selected company from the URL
    metric = request.args.get("metric", "headcount")
    search_term = request.args.get("search", None)
    selected_company = request.args.get("selected_company", None)

    # If a search term is provided, load data from your services
    # otherwise, use your example JSON data
    if search_term:
        data = load_data(domain=search_term)
        display_name = search_term
    else:
        data = load_data_example()
        display_name = "alan.com"

    # If a company is selected, find its details in the data
    selected_company_data = None
    if selected_company:
        selected_company_data = next(
            (
                entry
                for entry in data
                if entry["name"].lower() == selected_company.lower()
            ),
            None,
        )

    # Generate the Plotly tree map figure based on the selected metric
    fig = create_tree_map(data, display_name, metric)
    map_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

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


# Optional: If you want an endpoint for updating company data (used in plot clicks)
# you can define it here. This is just an example of how it might look.
@app.route("/update_data")
def update_data():
    company = request.args.get("company", None)
    if not company:
        return {"error": "No company specified"}, 400
    # Do whatever logic needed to return updated info
    # For now, just return a placeholder
    return {"success": True, "company": company}


if __name__ == "__main__":
    # Run in debug mode for development
    app.run(debug=True)

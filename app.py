from dotenv import load_dotenv
from flask import Flask, render_template, request

import json
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
    return list_companies(domain)


@app.route("/")
def display_map():
    # Get the metric, search term, and selected company from the URL
    metric = request.args.get("metric", "headcount")
    search_term = request.args.get("search", None)
    selected_company = request.args.get("selected_company", None)

    # Load data based on the search term or use example data
    if search_term:
        data = load_data(domain=search_term)
        display_name = search_term
    else:
        display_name = "alan.com"
        data = load_data_example()

    # If a company is selected, find its details in the data
    selected_company_data = None
    if selected_company:
        selected_company_data = next(
            (entry for entry in data if entry["name"].lower() == selected_company.lower()), None
        )

    # Generate the tree map based on the selected metric
    fig = create_tree_map(data, display_name, metric)
    map_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    # Pass data to the template, including the selected company details (if any)
    return render_template(
        "index.html",
        map_html=map_html,
        current_metric=metric,
        search_term=search_term,
        selected_company_data=selected_company_data,
    )


if __name__ == "__main__":
    app.run(debug=True)

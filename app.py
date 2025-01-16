from dotenv import load_dotenv
from flask import Flask, render_template

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
    data = load_data_example()
    fig = create_tree_map(data)
    map_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
    return render_template("index.html", map_html=map_html)


if __name__ == "__main__":
    app.run(debug=True)

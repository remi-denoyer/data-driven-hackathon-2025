from flask import Flask, request, jsonify
import requests
import os
from typing import List

app = Flask(__name__)

class HarmonicAPI:
    BASE_URL = "https://api.harmonic.ai"
    def __init__(self, api_key: str):
        self.headers = {
            "apikey": api_key,
            "accept": "application/json"
        }

    def get_company_urn(self, website_url: str) -> str:
        """
        Get company URN from website URL using Harmonic API
        """
        endpoint = f"{self.BASE_URL}/companies"
        params = {"website_url": website_url}

        response = requests.post(endpoint, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        return data["entity_urn"]

    def get_similar_companies(self, entity_urn: str, size: int = 10) -> List[str]:
        """
        Get similar companies based on entity URN
        Args:
            entity_urn: The URN of the company
            size: Number of similar companies to return (default: 10)
        Returns:
            List of company URNs
        """
        endpoint = f"{self.BASE_URL}/search/similar_companies/{entity_urn}"
        params = {"size": size}

        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        print(data)
        return data["results"]

    def get_companies_batch(self, urns: List[str]) -> List[dict]:
        """
        Get detailed information for multiple companies using their URNs
        Args:
            urns: List of company URNs
        Returns:
            List of company detail objects
        """
        endpoint = f"{self.BASE_URL}/companies/batchGet"
        payload = {"urns": urns}

        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

# Initialize HarmonicAPI with your API key
api_key = os.getenv('HARMONIC_API_KEY')
if not api_key:
    raise ValueError("HARMONIC_API_KEY environment variable is not set")
harmonic = HarmonicAPI(api_key)

@app.route('/')
def home():
    try:
        return jsonify({
            "message": "Welcome to the Harmonic API wrapper",
            "endpoints": {
                "/get_urn": "GET - Get company URN from website URL",
                "/get_similar": "GET - Get similar companies from URN",
                "/process": "GET - Complete pipeline to get similar companies from website URL"
            }
        })
    except Exception as e:
        app.logger.error(f"Error in home route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_urn')
def get_urn():
    website_url = request.args.get('website_url')
    if not website_url:
        return jsonify({"error": "website_url parameter is required"}), 400

    try:
        urn = harmonic.get_company_urn(website_url)
        return jsonify({"company_urn": urn})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_similar')
def get_similar():
    entity_urn = request.args.get('entity_urn')
    size = request.args.get('size', default=10, type=int)
    if not entity_urn:
        return jsonify({"error": "entity_urn parameter is required"}), 400

    try:
        similar = harmonic.get_similar_companies(entity_urn, size)
        return jsonify({"similar_companies": similar})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process')
def process():
    website_url = request.args.get('website_url')
    size = request.args.get('size', default=10, type=int)
    if not website_url:
        return jsonify({"error": "website_url parameter is required"}), 400

    try:
        # Get company URN
        company_urn = harmonic.get_company_urn(website_url)

        # Get similar companies (now returns just the URN list)
        similar_companies = harmonic.get_similar_companies(company_urn, size)

        # Get detailed information for similar companies
        company_details = harmonic.get_companies_batch(similar_companies)

        # Extract only required fields for each company
        formatted_companies = []
        for company in company_details:

            simplified_traction_metrics = {}
            for metric_name, metric_data in company["traction_metrics"].items():
                if "latest_metric_value" in metric_data:
                    simplified_traction_metrics[metric_name] = metric_data["latest_metric_value"]

            formatted_companies.append({
                "entity_urn": company["entity_urn"],
                "id": company["id"],
                "initialized_date": company["initialized_date"],
                "website": company["website"]["domain"],
                "customer_type": company["customer_type"],
                "name": company["name"],
                "description": company["description"],
                "external_description": company["external_description"],
                "founding_date": company["founding_date"]["date"],
                "headcount": company["headcount"],
                "ownership_status": company["ownership_status"],
                "company_type": company["company_type"],
                "stage": company["stage"],
                "country": company["location"]["country"],
                "funding": {
                    "funding_stage": company["funding"]["funding_stage"],
                    "funding_total": company["funding"]["funding_total"],
                    "last_funding_at": company["funding"]["last_funding_at"],
                    "last_funding_total": company["funding"]["last_funding_total"],
                    "last_funding_type": company["funding"]["last_funding_type"],
                    "num_funding_rounds": company["funding"]["num_funding_rounds"]
                },
                "highlights": company["highlights"],
                "funding_attribute_null_status": company["funding_attribute_null_status"],
                "traction_metrics": simplified_traction_metrics
            })

        # Return list of companies as separate objects
        return jsonify(formatted_companies)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
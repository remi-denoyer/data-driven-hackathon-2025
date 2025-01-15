import requests
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()


BASE_URL = "https://api.harmonic.ai"

HEADERS = {"apikey": os.environ["HARMONIC_API_KEY"], "accept": "application/json"}


def get_company_urn(website_url: str) -> str:
    """
    Get company URN from website URL using Harmonic API
    """
    endpoint = f"{BASE_URL}/companies"
    params = {"website_url": website_url}

    response = requests.post(endpoint, headers=HEADERS, params=params)
    response.raise_for_status()

    data = response.json()
    return data["entity_urn"]


def get_similar_companies(entity_urn: str, size: int = 10) -> List[str]:
    """
    Get similar companies based on entity URN
    Args:
        entity_urn: The URN of the company
        size: Number of similar companies to return (default: 10)
    Returns:
        List of company URNs
    """
    endpoint = f"{BASE_URL}/search/similar_companies/{entity_urn}"
    params = {"size": size}

    response = requests.get(endpoint, headers=HEADERS, params=params)
    response.raise_for_status()

    data = response.json()
    return data["results"]


def get_companies_batch(urns: List[str]) -> List[dict]:
    """
    Get detailed information for multiple companies using their URNs
    Args:
        urns: List of company URNs
    Returns:
        List of company detail objects
    """
    endpoint = f"{BASE_URL}/companies/batchGet"
    payload = {"urns": urns}

    response = requests.post(endpoint, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def list_enrich_similar_companies_from_domain(website_url: str, size: int = 10):

    # Get company URN
    company_urn = get_company_urn(website_url)

    # Get similar companies (now returns just the URN list)
    similar_companies = get_similar_companies(company_urn, size)

    # Get detailed information for similar companies
    company_details = get_companies_batch(similar_companies)

    # Extract only required fields for each company
    formatted_companies = []
    for company in company_details:

        simplified_traction_metrics = {}
        for metric_name, metric_data in company["traction_metrics"].items():
            if "latest_metric_value" in metric_data:
                simplified_traction_metrics[metric_name] = metric_data[
                    "latest_metric_value"
                ]

        formatted_companies.append(
            {
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
                    "num_funding_rounds": company["funding"]["num_funding_rounds"],
                },
                "highlights": company["highlights"],
                "funding_attribute_null_status": company[
                    "funding_attribute_null_status"
                ],
                "traction_metrics": simplified_traction_metrics,
            }
        )

        return formatted_companies

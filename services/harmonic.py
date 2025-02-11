import requests
import os
from dotenv import load_dotenv
from typing import List
import json
from data_harmonic import fake_companies
load_dotenv()


BASE_URL = "https://api.harmonic.ai"

HEADERS = {"apikey": os.environ.get("HARMONIC_API_KEY", ""), "accept": "application/json"}


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


def get_similar_companies(entity_urn: str, size: int = 5) -> List[str]:
    """
    Get similar companies based on entity URN
    Args:
        entity_urn: The URN of the company
        size: Number of similar companies to return (default: 30)
    Returns:
        List of unique company URNs, including the input URN
    """
    endpoint = f"{BASE_URL}/search/similar_companies/{entity_urn}"
    params = {"size": size}

    response = requests.get(endpoint, headers=HEADERS, params=params)
    response.raise_for_status()

    data = response.json()
    # Create a set with the input URN and similar companies to ensure uniqueness
    unique_urns = {entity_urn} | set(data["results"])
    return list(unique_urns)


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


def list_enrich_similar_companies_from_domain(website_url: str, size: int = 15):

    # Without API access to harmonic, lets use example data
    if os.environ.get("HARMONIC_API_KEY", "") == "":
        return fake_companies

    # Get company URN
    company_urn = get_company_urn(website_url)

    # Get similar companies (now returns just the URN list)
    similar_companies = get_similar_companies(company_urn, size)

    # Get detailed information for similar companies
    company_details = get_companies_batch(similar_companies)

    # Extract only required fields for each company
    formatted_companies = []
    for company in company_details:
        # Initialize simplified_traction_metrics
        simplified_traction_metrics = {}
        if company.get("traction_metrics"):  # Check if traction_metrics exists
            for metric_name, metric_data in company["traction_metrics"].items():
                if metric_data and "latest_metric_value" in metric_data:
                    simplified_traction_metrics[metric_name] = metric_data[
                        "latest_metric_value"
                    ]

        # Get headcount growth from traction metrics
        headcount_growth = None
        if company.get("traction_metrics", {}).get("headcount", {}).get("365d_ago", {}).get("percent_change"):
            headcount_growth = company["traction_metrics"]["external_headcount"]["365d_ago"]["percent_change"]

        formatted_companies.append(
            {
                "entity_urn": company.get("entity_urn"),
                "id": company.get("id"),
                "website": company.get("website", {}).get("domain"),
                "customer_type": company.get("customer_type"),
                "name": company.get("name"),
                "description": company.get("description"),
                "external_description": company.get("external_description"),
                "founding_date": (company.get("founding_date") or {}).get("date"),
                "headcount": company.get("headcount"),
                "ownership_status": company.get("ownership_status"),
                "company_type": company.get("company_type"),
                "stage": company.get("stage"),
                "country": (
                    company.get("location", {}).get("country")
                    if company.get("location")
                    else None
                ),
                "funding_stage": company.get("funding", {}).get("funding_stage"),
                "funding_total": company.get("funding", {}).get("funding_total"),
                "last_funding_at": company.get("funding", {}).get("last_funding_at"),
                "last_funding_total": company.get("funding", {}).get(
                    "last_funding_total"
                ),
                "last_funding_type": company.get("funding", {}).get(
                    "last_funding_type"
                ),
                "num_funding_rounds": company.get("funding", {}).get(
                    "num_funding_rounds"
                ),
                "highlights": company.get("highlights"),
                "funding_attribute_null_status": company.get(
                    "funding_attribute_null_status"
                ),
                "traction_metrics": simplified_traction_metrics,
                "headcount_growth": headcount_growth/100 if headcount_growth is not None else None,
            }
        )

    return formatted_companies

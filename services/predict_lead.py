import requests
import os
from similar_web import extract_domain
from dotenv import load_dotenv

load_dotenv()


def get_company_data(domain):
    """
    Fetch company data for a given domain using PredictLeads API.

    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        api_key (str): Your PredictLeads API key.
        api_token (str): Your PredictLeads API token.

    Returns:
        dict or str: JSON data returned by the API or an error message.
    """
    url = f"https://predictleads.com/api/v3/companies/{extract_domain(domain)}"
    headers = {
        "X-Api-Key": os.environ["PREDICT_LEAD_AUTH_KEY"],
        "X-Api-Token": os.environ["PREDICT_LEAD_AUTH_TOKEN"],
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Parse and return JSON data
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


def get_job_openings(domain):
    """
    Fetch company data for a given domain using PredictLeads API.

    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        api_key (str): Your PredictLeads API key.
        api_token (str): Your PredictLeads API token.

    Returns:
        dict or str: JSON data returned by the API or an error message.
    """
    url = f"https://predictleads.com/api/v3/companies/{extract_domain(domain)}/job_openings"
    headers = {
        "X-Api-Key": os.environ["PREDICT_LEAD_AUTH_KEY"],
        "X-Api-Token": os.environ["PREDICT_LEAD_AUTH_TOKEN"],
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Parse and return JSON data
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


def get_financing_events(domain):
    """
    Fetch company data for a given domain using PredictLeads API.

    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        api_key (str): Your PredictLeads API key.
        api_token (str): Your PredictLeads API token.

    Returns:
        dict or str: JSON data returned by the API or an error message.
    """
    url = f"https://predictleads.com/api/v3/companies/{extract_domain(domain)}/financing_events"
    headers = {
        "X-Api-Key": os.environ["PREDICT_LEAD_AUTH_KEY"],
        "X-Api-Token": os.environ["PREDICT_LEAD_AUTH_TOKEN"],
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Parse and return JSON data
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


def get_connections(domain):
    """
    Fetch company data for a given domain using PredictLeads API.

    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        api_key (str): Your PredictLeads API key.
        api_token (str): Your PredictLeads API token.

    Returns:
        dict or str: JSON data returned by the API or an error message.
    """
    url = f"https://predictleads.com/api/v3/companies/{extract_domain(domain)}/connections"
    headers = {
        "X-Api-Key": os.environ["PREDICT_LEAD_AUTH_KEY"],
        "X-Api-Token": os.environ["PREDICT_LEAD_AUTH_TOKEN"],
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Parse and return JSON data
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

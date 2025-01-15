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
        if len(response.json()["data"]) > 0:
            return response.json()["data"][0]  # Parse and return JSON data
        else:
            return {}
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
    params = {"limit": 1000, "active_only": True}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()["data"]
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
        return response.json()["data"]  # Parse and return JSON data
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
        return response.json()["data"]
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


def get_predict_lead_data(domain):
    # company_data = get_company_data(domain)
    job_openings = get_job_openings(domain)
    # financing_events = get_financing_events(domain)
    connections = get_connections(domain)

    # simple_connections = []
    # for connection in connections:
    #     # print(connection)
    #     if connection["attributes"]["source_url"] is None:
    #         continue
    #     simple_connections.append(
    #         {
    #             "category": connection["attributes"]["category"],
    #             "website": extract_domain(connection["attributes"]["source_url"]),
    #         }
    #     )

    nb_job_openings = len(job_openings)

    data = {
        "nb_job_openings": nb_job_openings,
        # "connections": simple_connections,
    }

    return data

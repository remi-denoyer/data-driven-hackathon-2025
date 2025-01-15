import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime

load_dotenv()

BASE_URL = "https://api.similarweb.com/v1"
BASE_URL_V4 = "https://api.similarweb.com/v4"


def extract_domain(url):
    """
    Extracts the domain from a given URL.

    Args:
        url (str): The URL to process.

    Returns:
        str: The extracted domain (e.g., "example.com").
    """
    parsed_url = urlparse(url)
    domain = parsed_url.path
    if domain.startswith("www."):
        domain = domain[4:]  # Remove "www." prefix if present
    return domain


def get_website_data(domain):
    """
    Fonction pour récupérer des données sur un domaine via l'API SimilarWeb.

    Args:
        domain (str): Le domaine à analyser (ex: "example.com").
        api_key (str): Votre clé API SimilarWeb.

    Returns:
        dict: Les données JSON renvoyées par l'API ou un message d'erreur.
    """
    # Construire l'URL complète avec le point de terminaison et les paramètres
    endpoint = f"{BASE_URL}/website/{domain}/general-data/all"
    params = {"api_key": os.environ["SIMILAR_WEB_REST_API_KEY"]}

    try:
        # Envoyer la requête GET
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Retourner les données au format JSON
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}


def get_keywords(domain):
    """
    Fonction pour récupérer les keywords sur un domaine via l'API SimilarWeb.

    Args:
        domain (str): Le domaine à analyser (ex: "example.com").
        api_key (str): Votre clé API SimilarWeb.

    Returns:
        dict: Les données JSON renvoyées par l'API ou un message d'erreur.
    """
    # Construire l'URL complète avec le point de terminaison et les paramètres
    endpoint = f"{BASE_URL_V4}/website-analysis/keywords/"
    start_date = "2024-12"
    end_date = "2024-12"
    params = {
        "URL": extract_domain(domain),
        "country": "world",
        "start_date": start_date,
        "end_date": end_date,
        "api_key": os.environ["SIMILAR_WEB_REST_API_KEY"],
    }

    try:
        # Envoyer la requête GET
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Retourner les données au format JSON
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}


def get_traffic_sources_overview(domain):
    """
    Fetch traffic sources overview share for a given domain using SimilarWeb API.

    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        api_key (str): Your SimilarWeb API key.

    Returns:
        dict: JSON data returned by the API or an error message.
    """
    endpoint = (
        f"{BASE_URL}/website/{extract_domain(domain)}/traffic-sources/overview-share"
    )
    params = {"api_key": os.environ["SIMILAR_WEB_REST_API_KEY"]}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}

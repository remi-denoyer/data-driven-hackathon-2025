import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

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
    domain = parsed_url.netloc
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
    params = {
        "url": extract_domain(domain),
        "country": "world",
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


# Exemple d'utilisation
def main(domain: str = "google.com"):
    data = get_website_data(domain)

    if "error" in data:
        print("Erreur :", data["error"])
    else:
        print("Données obtenues :")
        print(data)


if __name__ == "__main__":
    main()

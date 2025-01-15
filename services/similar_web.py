import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.similarweb.com/v1"


def get_website_data(domain, api_key):
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
    params = {"api_key": api_key}

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
    data = get_website_data(domain, os.environ["SIMILAR_WEB_REST_API_KEY"])

    if "error" in data:
        print("Erreur :", data["error"])
    else:
        print("Données obtenues :")
        print(data)


if __name__ == "__main__":
    main()

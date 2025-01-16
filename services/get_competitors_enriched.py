from services.harmonic import list_enrich_similar_companies_from_domain
from services.similar_web import get_similar_web_data
from services.predict_lead import get_predict_lead_data
from dotenv import load_dotenv

load_dotenv()

def get_competitors_enriched(domain: str):
    """
    Enriches the data of competitors for a given domain with additional information.

    Args:
        domain (str): The domain to analyze.

    Returns:
        list: A list of enriched competitor data.
    """
    data = list_enrich_similar_companies_from_domain(domain)

    for element in data:
        domain_element = element["website"]

        # Get data from external sources
        similar_web_data = get_similar_web_data(domain_element)
        predict_lead_data = get_predict_lead_data(domain_element)

        # Unpack similar_web_data fields into the element
        if similar_web_data:
            for key, value in similar_web_data.items():
                element[f"similar_web_{key}"] = value

        # Unpack predict_lead_data fields into the element
        if predict_lead_data:
            for key, value in predict_lead_data.items():
                element[f"predict_lead_{key}"] = value

    return data

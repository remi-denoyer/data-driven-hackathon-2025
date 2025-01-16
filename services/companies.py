from services.harmonic import list_enrich_similar_companies_from_domain
from services.similar_web import get_similar_web_data
from services.predict_lead import get_predict_lead_data
from dotenv import load_dotenv

from services.open_ai import generate_market_analysis
from services.utils import field_selector


load_dotenv()

FIELDS = [
    "name",
    "website",
    "headcount",
    "headcount_growth",
    "segment",
    "funding_total",
    "positive_analysis",
    "negative_analysis",
    "company_question",
]


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


def list_companies(domain: str):
    companies = get_competitors_enriched(domain)
    analysis = generate_market_analysis(
        field_selector(
            companies,
            [
                "name",
                "website",
                "customer_type",
                "description",
                "external_description",
                "funding_stage",
                "funding_total",
                "country",
                "headcount",
                "ownership_status",
                "company_type",
                "stage",
                "highlights",
                "traction_metrics",
            ],
        )
    )

    # Join companies and analysis based on domain key
    enriched_companies = []
    companies_dict = {company["website"]: company for company in companies}
    analysis_dict = {
        company["website"]: company
        for company in analysis["companies"]
        if not company["outlier"]
    }

    # Merge data for matching domains
    for website in set(companies_dict.keys()) | set(analysis_dict.keys()):
        company_data = companies_dict.get(website, {})
        analysis_data = analysis_dict.get(website, {})
        merged = {**company_data, **analysis_data}
        enriched_companies.append(merged)

    return field_selector(enriched_companies, FIELDS)

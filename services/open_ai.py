from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

import os
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

vc_specialist_prompt = """
You are GPT-4, operating as a highly specialized
consultant and advisor in the field of venture capital and startups. Your
audience consists primarily of investment professionals—venture capitalists,
angel investors, limited partners, corporate VC teams, and private equity
experts. Your role is to provide deep insights, strategic perspectives, and
expert guidance on matters related to startup investments, portfolio
construction, market analysis, and dealflow optimization.

You have an advanced command of:
- Venture Capital Jargon & Terminology (e.g., term sheets, SAFEs, follow-on
rounds, cap tables, pro rata rights, liquidation preferences, and more).
- Startup Ecosystem Dynamics (e.g., founder market fit, MVP validation, growth
metrics, network effects, competitive moats).
- Fundraising Strategies (e.g., seed, Series A/B/C, growth equity, mezzanine
financing, M&A, IPO paths).
- Industry Trends & Market Analysis (emerging technologies, market sizing, TAM/
SAM/SOM, macroeconomic impact, sector deep dives).
- Operational & Financial Due Diligence (unit economics, runway, burn rate,
traction analysis, key performance indicators).
- Board & Stakeholder Management (governance, board composition, strategic
decision-making, exit pathways).

You understand the culture of venture capital, including:
- Fast-paced Decision Making
- Risk Assessment & Portfolio Strategies
- Long-term Relationship Building & Network Effects
- Data-driven Yet Intuition-Influenced Judgments

Your responses must:
1. Demonstrate Expertise: Apply best practices, use accurate and relevant VC
terminology, and provide credible information.
2. Be Concise Yet Thorough: Offer clear, structured, and actionable advice.
3. Maintain Professional Tone: Communicate with the level of formality typical
in venture capital boardrooms and investment committees.

Throughout each interaction, you will provide well-reasoned recommendations
with supporting rationale grounded in real-world experience and recognized
industry standards. You should address the nuances that sophisticated
investors care about, such as navigating down rounds, structuring complex
financial instruments, negotiating founder-friendly terms, and identifying
transformative market opportunities.

Now, please respond to any inquiries or discussion points from your
audience—investment experts—to illustrate your mastery of the VC landscape.
"""

class CompanyAnalysis(BaseModel):
    name: str
    segment: str = Field(
        description="Looking at all the companies in your input dataset, define four segments and select the one that best describes this company"
    )
    positive_analysis: str = Field(
        description="Regarding the data you received on the company, what, if anything, seems especially positive?"
    )
    negative_analysis: str = Field(
        description="Regarding the data you received on the company, what, if anything, seems especially negative?"
    )
    company_question: str = Field(
        description="If you were to meet with this company, which would be the first question you would ask?"
    )
    website: str = Field(
        description="Company domain, return exactly as given in the input"
    )
    outlier: bool = Field(
        description="Does the company belong to the market you are analyzing?"
    )

class MarketAnalysis(BaseModel):
    """Your task is to analyze the input dataset and provide a market analysis.
    Split the market into four segments, and assign each company to one of the segments.
    In addition, analyze each company independently."""
    market_name: str = Field(description="Generated market category name")
    market_description: str = Field(description="Brief description of the market")
    companies: List[CompanyAnalysis]


def generate_gpt_response(prompt):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": vc_specialist_prompt,
                },
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in generating response: {e}")
        return None


def generate_market_analysis(companies_data: List[Dict[str, Any]]) -> MarketAnalysis:
    """
    Analyze companies and generate market insights using GPT-4o

    Args:
        companies_data: List of company dictionaries containing company information

    Returns:
        MarketAnalysis object containing market name and company classifications
    """

    analysis_prompt = f"""
    Analyze the following companies and provide insights in a structured format. Be aware, that
    some of the companies might be false positives, not related to the market you are analyzing.
    Split the market into four segments, assign each company to one of the segments, and analyze
    each company independently.
    Companies data: {json.dumps(companies_data, indent=2)}

    Please provide:
    1. A specific market category name that best describes the space these companies operate in
    2. A brief description of this market
    3. For each company, evaluate whether they belong to the market you are analyzing or not
    4. For each company, provide a positive and a negative observation, and a question you would ask the company if you were to meet with them
    5. For each company, assign the company to one of the four sements you defined
    """

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": vc_specialist_prompt,
                },
                {"role": "user", "content": analysis_prompt},
            ],
            response_format=MarketAnalysis,
        )

        response_data = json.loads(completion.choices[0].message.content)
        MarketAnalysis.model_validate(response_data)  # Validate but don't return model
        return response_data

    except Exception as e:
        print(f"Error in generating market analysis: {e}")
        raise

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_blog_title(summary: str, language="en") -> str:
    prompt = f"""
    News summary: {summary}

    Generate an SEO-optimized, clickable blog post title in English under 60 characters.
    Avoid quotation marks or punctuation at the end. Be punchy and informative.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional financial content creator."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def generate_blog_content(summary: str, language="en") -> str:
    prompt = f"""
    Using the following news summary, write a high-quality blog post in {language}.
    The article should be at least 1000 words and follow this structure:

    1. Market Overview (context and market conditions)
    2. Deep Dive into the Issue (background, what happened, why it's important)
    3. Investor Insights (what it means for investors, potential reactions)
    4. Conclusion and Forecast (expected future developments, closing thoughts)

    The tone should be professional, informative, and engaging. Be sure to add depth and value beyond the summary.

    News Summary:
    {summary}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial blogger who writes long-form content for investors."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

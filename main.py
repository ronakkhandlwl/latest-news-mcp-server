# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

# Create an MCP server
mcp = FastMCP("Latest-News")


def fetch_latest_headlines(category: str = None, country: str = 'us',
                           page_size: int = 10) -> List[Dict]:
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        raise ValueError("NEWS_API_KEY not found in environment variables")

    # Base URL for NewsAPI
    base_url = "https://newsapi.org/v2/top-headlines"

    # Prepare parameters
    params = {
        'country': country,
        'pageSize': page_size,
        'apiKey': api_key
    }

    # Add category if specified
    if category:
        params['category'] = category

    try:
        # Make the API request
        response = requests.get(base_url, params=params)

        # Raise exception for bad status codes
        response.raise_for_status()

        # Parse response
        data = response.json()

        # Extract relevant information from each article
        articles = []
        for article in data['articles']:
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'source': article['source']['name'],
                'url': article['url'],
                'published_at': article['publishedAt']
            })

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


@mcp.tool()
def latest_news_headlines(category: str, country: str,
                          page_size: int) -> List[Dict]:
    """
    Fetch latest news headlines using NewsAPI.

    Args:
        - category (str, optional): News category
          (e.g., 'business', 'technology', 'sports')
        - country (str, optional): 2-letter ISO 3166-1
          country code. Defaults to 'us'
        - page_size (int, optional): Number of headlines
          to return. Defaults to 10

    Returns:
        List[Dict]: List of news articles with title,
        description, source, and URL
    """
    return fetch_latest_headlines(category, country, page_size)


if __name__ == "__main__":
    mcp.run(transport='stdio')

import os
import requests
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Tool to retrieve news articles for a specified ticker symbol
def get_ticker_news(ticker: str) -> dict:
    """Retrieves the latest news articles for a specified ticker symbol.

    Args:
        ticker (str): The stock ticker symbol for which to retrieve the latest news articles. This is to be retrieved using 'identify_ticker_agent' sub-agent.

    Returns:
        dict: status with list of news articles or error message.
    """
    
    response = requests.get(f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_VANTAGE_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        if "feed" in data and len(data["feed"]) > 0:
            news = {"ticker": ticker,
                "sentiment_score_definition": data.get("sentiment_score_definition", "N/A"),
                "feed": []}
            
            # Limit to the first 15 news articles and extract relevant fields
            for i in range(15):
                news["feed"].append({
                    "title": data["feed"][i].get("title", "N/A"),
                    "time_published": data["feed"][i].get("time_published", "N/A"),
                    "source": data["feed"][i].get("source", "N/A"),
                    "summary": data["feed"][i].get("summary", "N/A"),
                    "overall_sentiment_score": data["feed"][i].get("overall_sentiment_score", "N/A"),
                    "overall_sentiment_label": data["feed"][i].get("overall_sentiment_label", "N/A"),
                })
            return {
                "status": "success",
                "news": news
            }
        else:
            return {
                "status": "error",
                "error_message": f"No news found for ticker '{ticker}'."
            }
    else:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve news information for '{ticker}'."
        }

# Create the agent that retrieves the latest news articles for a specified ticker symbol using the get_ticker_news tool
ticker_news = None
try:
    ticker_news = LlmAgent(
        name="ticker_news_agent",
        model=MODEL_GEMINI_1_5_FLASH,
        description=(
            "This agent retrieves the latest news articles for a specified ticker symbol using the 'get_ticker_news' tool."
        ),
        instruction="You are an agent that retrieves the latest news articles for a specified ticker symbol using the 'get_ticker_news' tool."
        "You will be provided with a ticker symbol, and you should use the 'get_ticker_news' tool to return the latest news articles."
        "Analyze the news articles to provide insights on the stock's performance."
        "Use this information to provide a comprehensive overview of the stock ticker symbol and answer questions like 'What is the latest news about the stock?' and 'How is the stock performing based on recent news?'."
        "If no news is found, return an error message."
        "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
        tools=[get_ticker_news],
    )
    print(f"Agent '{ticker_news.name}' created successfully.")
except Exception as e:
    print(f"Failed to create agent: {e}")
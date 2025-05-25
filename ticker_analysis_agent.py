import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from .ticker_news_agent import get_ticker_news
from .ticker_price_change_agent import get_ticker_price_change

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Tool to retrieve the latest news articles and price change for a specified ticker symbol
def get_ticker_analysis(ticker: str, days: int = 7) -> dict:
    """Retrieves the latest news articles and price change for a specified ticker symbol.

    Args:
        ticker (str): The stock ticker symbol for which to retrieve the latest news articles and price change. This is to be retrieved using 'identify_ticker_agent' sub-agent.
        days (int): The number of days over which to calculate the price change. Example: 1 for today, 7 for a week, 30 for a month, etc. Default is 7 days.

    Returns:
        dict: status with news articles and price change or error message.
    """
    
    news = get_ticker_news(ticker)
    price_change = get_ticker_price_change(ticker, days)

    if news["status"] == "success" and price_change["status"] == "success":
        news["news"].pop("ticker")
        price_change.pop("ticker")
        price_change.pop("status")
        
        # Amalgamate the results into a single response
        return {
            "status": "success",
            "ticker": ticker,
            "news": news["news"],
            "price_change": price_change
        }
    else:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve complete analysis for '{ticker}'."
        }

# Create the agent that analyzes stock ticker symbols using the get_ticker_analysis tool
ticker_analysis = None
try:
    ticker_analysis = LlmAgent(
        name="ticker_analysis_agent",
        model=MODEL_GEMINI_1_5_FLASH,
        description=(
            "This agent analyzes stock ticker symbols by retrieving the latest news articles and price changes for a specified ticker symbol."
        ),
        instruction="You are an agent that analyzes stock ticker symbols by retrieving the latest news articles and price changes for a specified ticker symbol using the 'get_ticker_analysis' tool."
        "You will be provided with a ticker symbol, and you should use the 'get_ticker_analysis' tool to return the latest news articles and price change over a specified number of days. Example: 1 for today, 7 for a week, 30 for a month, etc."
        "Analyze the news articles and price change to provide insights on the stock's performance."
        "Use this information to provide a comprehensive analysis of the stock ticker symbol and answer questions like 'What is the current status of the stock?' and 'Why has the stock price changed over the last 7 days?'."
        "If the analysis is not found, return an error message."
        "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
        tools=[get_ticker_analysis],
    )
    print(f"Agent '{ticker_analysis.name}' created successfully.")
except Exception as e:
    print(f"Failed to create agent: {e}")
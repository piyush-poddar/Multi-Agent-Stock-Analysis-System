import os
from dotenv import load_dotenv
import requests
from google.adk.agents import LlmAgent

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Tool to retrieve the current stock price for a specified ticker symbol
def get_ticker_price(ticker: str) -> dict:
    """Retrieves the current stock price for a specified ticker symbol.

    Args:
        ticker (str): The stock ticker symbol for which to retrieve the current price. This is to be retrieved using 'identify_ticker_agent' sub-agent.

    Returns:
        dict: status with current price or error message.
    """
    
    response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return {
                "status": "success",
                "ticker": ticker,
                "price": data["Global Quote"]["05. price"],
            }
        else:
            return {
                "status": "error",
                "error_message": f"No price found for ticker '{ticker}'."
            }
    else:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve price information for '{ticker}'."
        }
    
# Create the agent that retrieves the current stock price for a specified ticker symbol using the get_ticker_price tool
ticker_price = None
try:
    ticker_price = LlmAgent(
        name="ticker_price_agent",
        model=MODEL_GEMINI_1_5_FLASH,
        description=(
            "This agent retrieves the current stock price for a specified ticker symbol using the 'get_ticker_price' tool."
        ),
        instruction="You are an agent that retrieves the current stock price for a specified ticker symbol using the 'get_ticker_price' tool."
        "You will be provided with a ticker symbol, and you should use the 'get_ticker_price' tool to return the current price."
        "If the price is not found, return an error message."
        "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
        tools=[get_ticker_price],
    )
    print(f"Agent '{ticker_price.name}' created successfully.")
except Exception as e:
    print(f"Failed to create agent: {e}")
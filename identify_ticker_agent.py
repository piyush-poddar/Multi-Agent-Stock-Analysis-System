import os
import requests
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Tool to retrieve stock ticker symbol for a specified company
def get_ticker(keyword: str) -> dict:
    """Retrieves the stock ticker symbol for a specified company.

    Args:
        keyword (str): The name of the company or keyword for which to retrieve the ticker symbol. This is to be retrieved from the user query.

    Returns:
        dict: status with ticker symbol, company name and currency or error message.
    """

    ticker = requests.get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={ALPHA_VANTAGE_API_KEY}")

    if ticker.status_code == 200:
        data = ticker.json()
        if "bestMatches" in data and len(data["bestMatches"]) > 0:
            best_match = data["bestMatches"][0]
            return {
                "status": "success",
                "ticker": best_match["1. symbol"],
                "name": best_match["2. name"],
                "currency": best_match["8. currency"]
            }
        else:
            return {
                "status": "error",
                "error_message": f"No ticker found for '{keyword}'."
            }
    else:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve ticker information for '{keyword}'."
        }

# Create the agent that identifies stock ticker symbols using the get_ticker tool
identify_ticker = None
try:
    identify_ticker = LlmAgent(
        name="identify_ticker_agent",
        model=MODEL_GEMINI_1_5_FLASH,
        description=(
            "This agent identifies the stock ticker symbol for a specified company using the 'get_ticker' tool."
        ),
        instruction="You are an agent that identifies the stock ticker symbol for a specified company using the 'get_ticker' tool."
        "Retrieve the appropriate company name or keyword from user query, and you should use the 'get_ticker' tool to return the ticker symbol, company name and currency for further use."
        "If the ticker symbol is not found, return an error message."
        "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
        tools=[get_ticker],
    )
    print(f"Agent '{identify_ticker.name}' created successfully.")
except Exception as e:
    print(f"Failed to create agent: {e}")
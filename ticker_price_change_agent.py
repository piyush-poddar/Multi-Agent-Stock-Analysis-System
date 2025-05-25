import os
from dotenv import load_dotenv
import requests
from google.adk.agents import LlmAgent

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Tool to retrieve the stock price change for a specified ticker symbol over a given number of days
def get_ticker_price_change(ticker: str, days: int = 7) -> dict:
    """Retrieves the stock price change for a specified ticker symbol over a given number of days.

    Args:
        ticker (str): The stock ticker symbol for which to retrieve the price change. This is to be retrieved using 'identify_ticker_agent' sub-agent.
        days (int): The number of days over which to calculate the price change. Example: 1 for today, 7 for a week, 30 for a month, etc. Default is 7 days.

    Returns:
        dict: status with price change or error message.
    """
    
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            dates = sorted(time_series.keys(), reverse=True)
            if len(dates) >= days:
                # Get the latest and previous dates and their corresponding prices
                latest_date = dates[0]
                previous_date = dates[days - 1]
                latest_price = float(time_series[latest_date]["4. close"])
                previous_price = float(time_series[previous_date]["4. close"])
                price_change = latest_price - previous_price
                return {
                    "status": "success",
                    "ticker": ticker,
                    "price_change": price_change,
                    "latest_date": latest_date,
                    "latest_price": latest_price,
                    "previous_date": previous_date,
                    "previous_price": previous_price,
                }
            else:
                return {
                    "status": "error",
                    "error_message": f"Not enough data available for '{ticker}' over {days} days."
                }
        else:
            return {
                "status": "error",
                "error_message": f"No data found for ticker '{ticker}'."
            }
    else:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve price change information for '{ticker}'."
        }

# Create the agent that retrieves the stock price change for a specified ticker symbol using the get_ticker_price_change tool  
ticker_price_change = None
try:
    ticker_price_change = LlmAgent(
        name="ticker_price_change_agent",
        model=MODEL_GEMINI_1_5_FLASH,
        description=(
            "This agent retrieves the stock price change for a specified ticker symbol over a given number of days using the 'get_ticker_price_change' tool."
        ),
        instruction="You are an agent that retrieves the stock price change for a specified ticker symbol over a given number of days using the 'get_ticker_price_change' tool."
        "You will be provided with a ticker symbol and the number of days, and you should use the 'get_ticker_price_change' tool to return the price change."
        "If the price change is not found, return an error message."
        "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
        tools=[get_ticker_price_change],
    )
    print(f"Agent '{ticker_price_change.name}' created successfully.")
except Exception as e:
    print(f"Failed to create agent: {e}")
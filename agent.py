from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from .identify_ticker_agent import identify_ticker
from .ticker_price_agent import ticker_price
from .ticker_price_change_agent import ticker_price_change
from .ticker_news_agent import ticker_news
from .ticker_analysis_agent import ticker_analysis

MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"

# NOTE:
# Instead of registering sub-agents using the `sub_agents` parameter, each specialized agent
# is wrapped as a tool using `AgentTool` and passed to the root agent via the `tools` parameter.
#
# Reason:
# Using sub-agents directly caused the root agent to lose control after delegation.
# Once a sub-agent was invoked, the conversation flow would remain inside it, and
# the root agent could not regain control to continue orchestrating or summarizing.
#
# Solution:
# Wrapping sub-agents as tools allows the root agent to invoke them like function calls,
# retain control of the conversation, and coordinate multiple tools in a single interaction.
#
# This design enables proper multi-agent collaboration while preserving modularity.

identify_ticker_tool = agent_tool.AgentTool(agent=identify_ticker)
ticker_price_tool = agent_tool.AgentTool(agent=ticker_price)
ticker_price_change_tool = agent_tool.AgentTool(agent=ticker_price_change)
ticker_news_tool = agent_tool.AgentTool(agent=ticker_news)
ticker_analysis_tool = agent_tool.AgentTool(agent=ticker_analysis)

# Create the root agent that coordinates the specialized sub-agents
root_agent = LlmAgent(
    name="stock_analysis_agent",
    model=MODEL_GEMINI_1_5_FLASH,
    description=(
        "Main Stock Analysis Agent that coordinates a team of specialized sub-agents to provide stock information. "
    ),
    instruction="You are the main Stock Analysis Agent coordinating a team of sub-agents. Your primary responsibility is to provide Stock information. "
                "You have specialized sub-agents: "
                "1. 'identify_ticker_agent': Handles identifying stock ticker symbols for companies. Delegate to it for any query related to identifying a ticker symbol, and use it for further tasks."
                "2. 'ticker_price_agent': Retrieves the current stock price for a specified ticker symbol. Delegate to it for any query related to retrieving stock prices."
                "3. 'ticker_price_change_agent': Retrieves the stock price change for a specified ticker symbol over a given number of days. Delegate to it for any query related to retrieving stock price changes."
                "4. 'ticker_news_agent': Retrieves the latest news articles for a specified ticker symbol. Delegate to it for any query related to retrieving stock news."
                "5. 'ticker_analysis_agent': Analyzes stock ticker symbols by retrieving the latest news articles and price changes for a specified ticker symbol. Delegate to it for any query related to analyzing stock tickers. Use it to provide comprehensive insights on stock performance, including news and price changes and answer questions like 'What is the current status of the stock?' and 'Why has the stock price changed over the last 7 days?'."
                "You will receive user queries that may require the use of multiple sub-agents to gather the necessary information."
                "Based on the user's request, make a step by step plan to gather the required information using these sub-agents."
                "Then carefully delegate tasks to the appropriate sub-agents based on the user's request."
                "You may have to use multiple sub-agents to complete a task, so ensure you manage the flow of information effectively."
                "Remember to provide clear instructions to the sub-agents and handle their responses appropriately, for further delegation to the next sub-agent or to the user."
                "For example, if a user asks 'what is the current price of tesla stock?'"
                "The following steps should be taken:"
                "1. First identify the company name or keyword from the user query, which in this case is 'tesla'."
                "2. Identify the ticker symbol for 'tesla' using the 'identify_ticker_agent'."
                "3. Once the ticker symbol is identified, retrieve the current stock price using the 'ticker_price_agent'."
                "If a sub-agent fails to provide the required information, handle the error gracefully and inform the user."
                "Ensure that you provide only the final comprehensive response to the user based on the information gathered from the sub-agents. No need for internal conversation or task management details in the final response."
                "Remember that you can only use these sub-agents for the stock related user queries, do not use any other information or tools outside of these sub-agents."
                "For anything else, respond appropriately or state you cannot handle it."
                "NOTE: ALWAYS RETURN BACK TO THE ROOT AGENT AFTER FINALLY COMPLETING THE TASK, SO THAT IT CAN PROVIDE THE FINAL RESPONSE TO THE USER.",
    # sub_agents=[identify_ticker, ticker_price, ticker_price_change],
    tools=[identify_ticker_tool, ticker_price_tool, ticker_price_change_tool, ticker_news_tool, ticker_analysis_tool],
)
print(f"Agent '{root_agent.name}' created successfully.")
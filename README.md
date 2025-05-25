# 📊 Multi-Agent Stock Analysis System (Google ADK)

This project is a modular, multi-agent system built using **Google Agent Developer Kit (ADK)** that can handle complex stock-related queries using a team of coordinated sub-agents. It provides real-time price, news, and performance insights for publicly traded companies using the Alpha Vantage API.

---

## 🚀 Features

- 🔎 **Ticker Identification:** Recognizes and maps company names to stock ticker symbols.
- 💵 **Current Price Fetching:** Retrieves the latest stock price.
- 📈 **Price Change Analysis:** Calculates how the price has changed over a specified period.
- 📰 **News Aggregation:** Collects and summarizes the most recent news related to the stock.
- 🧠 **Comprehensive Analysis:** Uses both price and news data to explain recent stock performance.
- ⚡ **Powered by Gemini 1.5 Flash** (via Vertex AI) and fully orchestrated using Google ADK.

---

## 🧠 System Architecture

- **Root Agent:** `stock_analysis_agent`
- **Coordinates five sub-agents:**
  - `identify_ticker_agent`
  - `ticker_price_agent`
  - `ticker_price_change_agent`
  - `ticker_news_agent`
  - `ticker_analysis_agent`

Each sub-agent performs a specific task and returns control to the root agent, which generates the final response.

---

---
## 🧠 Agent Design Insight

### Why are sub-agents wrapped as tools instead of traditional ADK sub-agents?

During development, a challenge was encountered:

> When sub-agents were used via the `sub_agents=[...]` parameter in the root agent,  
> the root agent would delegate tasks to a sub-agent,  
> **but control never returned back to the root agent after the sub-agent responded.**

### 🚀 Solution: Wrap Sub-Agents as Tools

Each sub-agent is wrapped as a tool using `AgentTool`, which:

- 🕹️ **Ensures the root agent always retains control**
- 🔗 **Allows chaining multiple sub-agent tools in a single user query**
- 🧩 **Enables complex reasoning and orchestration within the root agent**

This approach preserves modularity while enabling smooth multi-agent collaboration through tool calls—effectively turning each specialized agent into a callable function.

#### 🛠️ Example

```python
from google.adk.tools import agent_tool

identify_ticker_tool = agent_tool.AgentTool(agent=identify_ticker)
```

These tools are then used in the root agent like this:

```python
tools = [identify_ticker_tool, ticker_price_tool, ...]
```

**✅ Result:**  
Seamless multi-step query resolution while maintaining agent-level modularity!

---

## 🛠️ Sub-Agents Overview

| Agent                    | Description                                                         |
|--------------------------|---------------------------------------------------------------------|
| `identify_ticker_agent`  | Uses Alpha Vantage SYMBOL_SEARCH to identify ticker symbols.         |
| `ticker_price_agent`     | Uses GLOBAL_QUOTE to fetch the latest stock price.                   |
| `ticker_price_change_agent` | Uses TIME_SERIES_DAILY to compute price change over a given period.|
| `ticker_news_agent`      | Uses NEWS_SENTIMENT to retrieve and summarize the latest news.       |
| `ticker_analysis_agent`  | Combines price change and news data for high-level analysis.         |

---

## 🧪 Example User Queries

- “Why did Tesla stock drop today?”
- “What’s happening with Palantir stock recently?”
- “How has Nvidia stock changed in the last 7 days?”

The root agent handles each query by calling relevant sub-agents step-by-step and returns a cohesive response.

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/stock-analysis-agent.git
cd stock-analysis-agent
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file with the following contents:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
```

> 💡 You can get an Alpha Vantage key at: [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

### 4. Run Locally with ADK Web UI

```bash
adk web
```

Then visit: [http://localhost:8080](http://localhost:8080) to start chatting with your multi-agent system.

---

## 📁 Project Structure

```
.
├── .env
├── __init__.py
├── agent.py                     # Root agent definition
├── identify_ticker_agent.py     # Sub-agent: company → ticker
├── ticker_price_agent.py        # Sub-agent: fetch current stock price
├── ticker_price_change_agent.py # Sub-agent: fetch price change
├── ticker_news_agent.py         # Sub-agent: fetch latest news
├── ticker_analysis_agent.py     # Sub-agent: news + price analysis
```

---

## 📹 Demo Video

🎥 [*A short demo video showing sample user queries and system behavior.*](https://drive.google.com/file/d/1AqYQ4f2EWmKlsw8WBOazv4GGWS2e0fQb/view?usp=sharing)

---

## ✅ Project Highlights

- ✅ Functional multi-agent pipeline using Google ADK
- ✅ Modular, reusable agents
- ✅ Handles both direct and complex stock-related queries
- ✅ Clean, documented architecture
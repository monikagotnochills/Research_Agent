<img width="1817" height="838" alt="image" src="https://github.com/user-attachments/assets/c022d5cc-120c-4d31-9827-f3b7cac7981e" />
https://dwight-ai.streamlit.app/
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-ReAct-00A67E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GPT--4o-Azure_Inference-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<h1 align="center"> Dwight AI — Multi-Agent Research System</h1>

<p align="center">
  <strong>An autonomous multi-agent pipeline that transforms any research topic into a polished, well-sourced report — in minutes, not hours.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-contributing">Contributing</a>
</p>

---
<img width="1620" height="437" alt="image" src="https://github.com/user-attachments/assets/fc2eac1d-a82d-4496-8ef3-2f8068d4bb4a" />



## 🚀 Features

| Feature | Description |
|---------|-------------|
| **🔍 Search Agent** | Queries the web via [Tavily](https://tavily.com/) to discover the most recent and relevant sources, articles, and references for any topic. |
| **📖 Reader Agent** | Automatically selects the most promising URLs from search results and scrapes clean, structured content using BeautifulSoup. |
| **✍️ Writer Agent** | Synthesizes all gathered research into a detailed, structured report with an introduction, key findings, conclusion, and cited sources. |
| **🧐 Critic Agent** | Reviews the generated report for accuracy, depth, and consistency — producing a scored assessment with strengths and areas for improvement. |
| **🎨 Liquid Glass UI** | A premium Streamlit interface with glassmorphism design, animated 3D cube loaders, drifting cloud parallax, and a custom liquid-glass cursor. |
| **⚡ Real-time Pipeline** | Watch each agent activate, process, and complete in real-time with live status updates, notification toasts, and animated pipeline cards. |
| **📥 Downloadable Reports** | Export the final research report as a `.md` Markdown file with a single click. |
| **📱 Fully Responsive** | Optimized layouts for desktop, tablet, and mobile with media query breakpoints. |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT (Topic)                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │     🔍 SEARCH AGENT          │
         │   (LangGraph ReAct Agent)     │
         │   Tool: Tavily Web Search     │
         │   → Discovers 5 top sources   │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │     📖 READER AGENT          │
         │   (LangGraph ReAct Agent)     │
         │   Tool: URL Scraper           │
         │   → Extracts deep content     │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │     ✍️ WRITER CHAIN           │
         │   (LangChain Prompt Chain)    │
         │   → Structured research       │
         │     report with citations     │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │     🧐 CRITIC CHAIN          │
         │   (LangChain Prompt Chain)    │
         │   → Score /10, strengths,     │
         │     improvements, verdict     │
         └───────────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              📄 FINAL REPORT + ASSESSMENT               │
│           (Downloadable Markdown + Critic Score)        │
└─────────────────────────────────────────────────────────┘
```

### Agent Design

| Agent | Type | Framework | Purpose |
|-------|------|-----------|---------|
| **Search Agent** | ReAct Agent | LangGraph `create_react_agent` | Autonomous reasoning + tool use for web search |
| **Reader Agent** | ReAct Agent | LangGraph `create_react_agent` | Autonomous reasoning + tool use for URL scraping |
| **Writer** | Prompt Chain | LangChain `ChatPromptTemplate → LLM → StrOutputParser` | Deterministic report generation from research |
| **Critic** | Prompt Chain | LangChain `ChatPromptTemplate → LLM → StrOutputParser` | Deterministic evaluation and scoring |

> **Why ReAct for Search/Reader?** These agents need to *reason* about which queries to run or which URLs to scrape — they decide autonomously. The Writer and Critic follow a fixed structure, so a simple prompt chain is more efficient.

---

## 🛠 Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **LLM** | GPT-4o via [GitHub Models](https://github.com/marketplace/models) (Azure Inference) | Core reasoning engine for all agents |
| **Agent Framework** | [LangGraph](https://github.com/langchain-ai/langgraph) | ReAct agent orchestration with tool binding |
| **Chain Framework** | [LangChain](https://github.com/langchain-ai/langchain) | Prompt templates, output parsing, chain composition |
| **Web Search** | [Tavily API](https://tavily.com/) | Real-time web search optimized for AI agents |
| **Web Scraping** | BeautifulSoup4 + Requests | Clean text extraction from HTML pages |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI with custom HTML/CSS/JS components |
| **Styling** | Custom CSS (Glassmorphism) | Liquid glass effects, animations, responsive design |
| **Environment** | python-dotenv | Secure API key management |

---

## ⚡ Quickstart

### Prerequisites

- **Python 3.10+** installed
- A **GitHub Personal Access Token** (with Models access) — [Generate here](https://github.com/settings/tokens)
- A **Tavily API Key** — [Get free key](https://app.tavily.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/monikagotnochills/Research_Agent.git
cd Research_Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the **parent directory** of the project (one level above the code files):

```
Research_Agent/          ← your cloned repo
├── .env                 ← create this file HERE
├── agents.py
├── tools.py
├── pipeline.py
├── app.py
├── assets/
└── ...
```

Add your API keys:

```env
TAVILY_API_KEY=tvly-your-tavily-api-key-here
GITHUB_TOKEN=github_pat_your-github-token-here
```

> ⚠️ **Important:** The `.env` file is loaded from one directory above the source files (`parent.parent` of the script). If you place it in the wrong directory, the agents won't authenticate.

### 5. Run the Application

**Option A — Streamlit Web UI (Recommended)**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` with the full interactive pipeline UI.

**Option B — Terminal/CLI Mode**

```bash
python pipeline.py
```

Enter a research topic when prompted and watch the agents work in your terminal.

---

##  Deployment

### Deploy on Streamlit Community Cloud

1. **Push your code** to a GitHub repository (ensure `.env` is in `.gitignore`).

2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub repo.

3. Set your **secrets** in Streamlit Cloud:
   - Navigate to **App Settings → Secrets**
   - Add your keys:
     ```toml
     TAVILY_API_KEY = "tvly-your-key-here"
     GITHUB_TOKEN = "github_pat_your-token-here"
     ```

4. Set the **main file path** to `app.py` and deploy.

> **Note:** The `.streamlit/config.toml` is included for local theming. On Streamlit Cloud, secrets are managed through the dashboard, not `.env` files.

---

## 📁 Project Structure

```
Research_Agent/
│
├── app.py                  # Streamlit web application (UI + pipeline execution)
│                           #   → 3-page flow: Home → Pipeline (live) → Results
│                           #   → Custom CSS design system (glassmorphism)
│                           #   → JS components (cursor, clouds, autocomplete)
│
├── agents.py               # Agent and chain definitions
│                           #   → Search Agent (ReAct + Tavily web_search tool)
│                           #   → Reader Agent (ReAct + scrape_url tool)
│                           #   → Writer Chain (prompt → GPT-4o → parser)
│                           #   → Critic Chain (prompt → GPT-4o → parser)
│
├── tools.py                # LangChain tool definitions
│                           #   → web_search: Tavily API wrapper (5 results)
│                           #   → scrape_url: BeautifulSoup scraper (3000 chars)
│
├── pipeline.py             # CLI pipeline runner (terminal mode)
│                           #   → Sequential: Search → Read → Write → Critique
│                           #   → Standalone entry point with `__main__`
│
├── requirements.txt        # Python dependencies with minimum versions
│
├── .gitignore              # Excludes .env, __pycache__, .venv, IDE files
│
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration (light mode)
│
└── assets/
    ├── bg.jpg              # Home page background image
    ├── bg_pipeline.jpg     # Pipeline/workspace background image
    └── blue_capsule.png    # Decorative UI element
```

---

## 🔬 How It Works

### Step-by-Step Pipeline

#### 1. 🔍 Search Agent
The Search Agent uses LangGraph's `create_react_agent` with the Tavily `web_search` tool. Given a topic, it autonomously decides what queries to run and returns the **top 5 results** with titles, URLs, and content snippets.

```python
search_agent = build_search_agent()
result = search_agent.invoke({
    "messages": [("user", f"Find recent, reliable information about: {topic}")]
})
```

#### 2. 📖 Reader Agent
The Reader Agent receives the search results and intelligently selects the most relevant URL to scrape. It uses BeautifulSoup to extract clean text (up to 3,000 characters), stripping scripts, styles, navigation, and footer elements.

```python
reader_agent = build_reader_agent()
result = reader_agent.invoke({
    "messages": [("user", f"Pick the most relevant URL and scrape it...\n{search_results}")]
})
```

#### 3. ✍️ Writer Chain
The Writer Chain combines all research (search results + scraped content) and generates a structured report with:
- **Introduction** — Context and significance
- **Key Findings** — Minimum 3 well-explained points
- **Conclusion** — Summary and implications
- **Sources** — All referenced URLs

#### 4. 🧐 Critic Chain
The Critic Chain evaluates the report and produces:
- **Score:** X/10
- **Strengths:** What the report does well
- **Areas to Improve:** Specific suggestions
- **One-line Verdict:** Final assessment

### LLM Configuration

All agents use **GPT-4o** via GitHub Models (Azure AI Inference):

```python
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)
```

This leverages the **free** GitHub Models inference tier — no OpenAI API key or Azure subscription required. Just a GitHub Personal Access Token with Models access.

---

## UI Design

The Streamlit frontend features a custom-built design system:

- **Glassmorphism** — Frosted glass panels with `backdrop-filter: blur()` and subtle gradients
- **3D Cube Loader** — Animated loading indicator during pipeline execution
- **Drifting Clouds** — Parallax cloud animation layer using JavaScript `requestAnimationFrame`
- **Liquid Glass Cursor** — Custom cursor that follows mouse movement with glass refraction effect
- **Notification Toasts** — Real-time activity feed showing agent start/completion events
- **Pipeline Cards** — Animated status cards (Waiting → Running → Done) with pulse effects
- **Typography** — Plus Jakarta Sans (UI), Playfair Display (headings), Source Serif 4 (body), JetBrains Mono (code)
- **Responsive** — Full breakpoint support for desktop (1024px+), tablet, and mobile (640px)

---

## 🔑 API Keys Reference

| Key | Source | Free Tier | Purpose |
|-----|--------|-----------|---------|
| `GITHUB_TOKEN` | [GitHub Settings → Tokens](https://github.com/settings/tokens) | ✅ Yes (with Models) | Authenticates GPT-4o via GitHub Models |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com/) | ✅ Yes (1,000 searches/month) | Powers the Search Agent's web queries |

> **GitHub Token Setup:** When creating your token, ensure you enable the **"Models"** permission under the Fine-grained permissions to access GitHub's AI inference endpoint.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

### Ideas for Contribution

- [ ] Add a **PDF export** option for research reports
- [ ] Implement **multi-topic** batch research
- [ ] Add **citation formatting** (APA, MLA, Chicago)
- [ ] Support **additional LLMs** (Claude, Gemini, Llama)
- [ ] Add a **research history** panel with past reports
- [ ] Implement **streaming responses** for real-time report generation

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/monikagotnochills">monikagotnochills</a></strong>
  <br>
  <sub>Dwight AI — Autonomous multi-agent research assistant</sub>
</p>


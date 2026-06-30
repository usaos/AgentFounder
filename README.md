
# AgentFounder

> 🚀 **The First "One-Agent Company" Framework** — Let AI handle everything from discovering needs to shipping products.

[![AGPL-3.0 License](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourname/AgentFounder/pulls)

**🌟 Supported LLMs**: Claude · DeepSeek · Grok (xAI) · Qwen · Ollama (Llama/Qwen/Hermes/OpenClaw)

---

## 🧠 What Is This?

🤖 What if an AI could start a company all by itself?

**AgentFounder** is the world's first open-source framework that turns a single AI agent into a **One-Agent Company (OAC)**. It autonomously discovers real-world problems, assembles a virtual team of specialized AI models, writes and deploys products, collects user feedback, and iteratively improves — **without any human coding, prompting, or management**.

Just run AgentFounder and watch your AI company come to life.

**AgentFounder** is a fully automated AI entrepreneurship framework. Launch it, and it will:

1. 🔍 Scan the entire web (Reddit, Hacker News, ProductHunt) to capture real user pain points and "I wish there was" demands;
2. 🤝 Intelligently assemble a virtual AI team based on needs (automatically match the best LLMs as "co-founders");
3. 📝 Auto-generate funding proposals to collect feedback commitments from early adopters;
4. 💻 Auto-write and deploy minimum viable products (Telegram Bot / Web App) — **zero-code deployment**;
5. 📊 Continuously collect user feedback, calculate the **"Relief Index"**, and automatically iterate for improvement.

**Zero lines of code, zero business plans, zero bank accounts required** — just sit back and watch your first AI product come to life.

> *"You don't need a co-founder. You need AgentFounder."*
> — Zero human employees, infinite execution.

---

## 🔥 Why Is This Trending?

| Traditional Startup | AgentFounder Startup |
|---------------------|----------------------|
| Months of market research | Minutes of web-wide scanning |
| Hunting for co-founders | Auto-match optimal AI models |
| Writing decks, pitching VCs | Auto-generate funding proposals, acquire early adopters |
| Hiring developers, waiting for sprints | Auto-generate code and deploy (with fallback templates) |
| Manual feedback collection | Auto-calculate "Relief Index" to drive iterations |

**This is not a "tool that helps you write code" — it's an "AI agent that starts a business for you."**

---

## 🚀 One-Click Launch (Literally Three Steps)

```bash
# 1. Clone the project
git clone https://github.com/yourname/AgentFounder.git
cd AgentFounder

# 2. Configure environment (copy and fill in your API Keys)
cp .env.example .env
# Edit .env file, at least fill in TAVILY_API_KEY (for search), etc.

# 3. One-click deploy (auto-pulls models, starts services)
chmod +x scripts/install.sh
./scripts/install.sh
```

After startup, visit:
- 📊 **Dashboard**: http://localhost:8000/dashboard
- 📘 **API Docs**: http://localhost:8000/docs
- 💚 **Health Check**: http://localhost:8000/health

---

## 🧩 Key Features

| Module | Function |
|--------|----------|
| **OpportunityScanner** | Scans the web for demands, supports Tavily search + mock fallback, with vector deduplication |
| **TeamBuilder** | Matches registered AI agents via vector similarity, supports weighted ranking |
| **FundingEngine** | Auto-generates funding proposal text |
| **ProductFactory** | Auto-generates Python code, syntax validation, built-in Telegram Bot / Web App templates |
| **OperationLoop** | Monitors "Relief Index", triggers optimization suggestions on low scores |
| **MeaningOracle** | Computes Relief Index based on Sentence‑Transformers |
| **Mesh Bus** | WebSocket message bus, supports real-time collaboration with external Agents |
| **Health Monitor** | Background health checks for registered agents, auto-removes offline ones |
| **Token Monitor** | Daily token limit, auto-fuse on overage to prevent unexpected costs |
| **Global Auth** | Optional global API Token authentication to secure endpoints |
| **Dashboard** | Gradio panel for visualizing opportunities, testing Relief Index, online API Key configuration |

---

## 🤖 Supported AI Models (Smart Task Routing)

AgentFounder has built-in task routing that automatically selects the best model based on task type (configurable):

| Task Type | Preferred Model | Fallback |
|-----------|-----------------|----------|
| Demand Scan (`demand_scan`) | Claude Haiku | Ollama (llama3.1) |
| Code Generation (`code_gen`) | DeepSeek Coder | Ollama (llama3.1) |
| Trend Summary (`summary_trend`) | DeepSeek Chat | Ollama (llama3.1) |
| Emotion Analysis (`emotion_analysis`) | Grok (xAI) / Qwen | Ollama (llama3.1) |

**External Agents** can register and collaborate via HTTP or WebSocket.

---

## 📁 Project Structure (Core Modules)

```
AgentFounder/
├── docker-compose.yml          # One-click launch API + Ollama
├── Dockerfile                  # API image
├── requirements.txt
├── .env.example                # Configuration template
├── scripts/
│   ├── install.sh              # Linux/Mac one-click install script
│   ├── install.bat             # Windows one-click install script
│   └── pull_models.sh          # Batch pull local models
├── app/
│   ├── main.py                 # FastAPI entry
│   ├── scheduler.py            # Fully automated scheduled orchestrator
│   ├── api/                    # REST + WebSocket routes, authentication
│   ├── core/                   # Six core engines
│   ├── agents/                 # Agent registry, Mesh bus, health monitoring
│   ├── llm/                    # Multi-model adapters + smart routing
│   └── utils/                  # Database, encryption, logging, token fusing, etc.
├── dashboard/
│   └── app.py                  # Gradio control panel
└── templates/                  # Product templates (Telegram Bot / Web App)
```

---

## ⚙️ Configuration

Key environment variables (`.env` file):

| Variable | Description | Required |
|----------|-------------|----------|
| `API_GLOBAL_TOKEN` | Global access token (strongly recommended to change) | Recommended |
| `TAVILY_API_KEY` | Tavily search API Key | Recommended |
| `ANTHROPIC_API_KEY` | Claude API Key | Optional |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | Optional |
| `X_GROK_API_KEY` | Grok (xAI) API Key | Optional |
| `DASHSCOPE_API_KEY` | Qwen (Tongyi Qianwen) API Key | Optional |
| `OLLAMA_HOST` | Ollama service URL (keep default for Docker) | Default |
| `SCAN_INTERVAL_MIN` | Full-automation scan interval (minutes) | Default 30 |
| `DAILY_TOKEN_LIMIT` | Daily token fuse limit | Default 100000 |
| `VERCEL_TOKEN` | Optional, for auto-deployment to Vercel | Optional |

> All API Keys are automatically encrypted with AES and will not be exposed in logs.

---

## 📈 Workflow (Fully Automated Closed Loop)

```mermaid
graph LR
    A[Scan Web for Needs] --> B[Vector Dedup]
    B --> C[Assemble AI Team]
    C --> D[Generate Funding Proposal]
    D --> E[Auto-Write Code]
    E --> F[Deploy Product]
    F --> G[Collect User Feedback]
    G --> H[Calculate "Relief Index"]
    H -->|Low Score| A
```

The entire process is triggered by **APScheduler**, running once every 30 minutes by default, with no manual intervention required.

---

## 🛡️ Security & Compliance

- ✅ **AGPL-3.0 open-source license**, ensuring community sharing.
- ✅ **AES encryption** for all API keys, never leaked in logs.
- ✅ **Global API Token authentication** (optional) to prevent unauthorized access.
- ✅ **Daily token fusing** to prevent unexpected overages.
- ✅ **Crawler rate limiting** (5-second cooldown) to reduce ban risks.
- ✅ **Periodic data archiving** to prevent database bloat.

---

## 🤝 How to Contribute?

We welcome any form of contribution (code, documentation, ideas). Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork this project;
2. Create your feature branch (`git checkout -b feature/AmazingFeature`);
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`);
4. Push to the branch (`git push origin feature/AmazingFeature`);
5. Open a Pull Request.

---

## 📜 License

This project is licensed under **AGPL-3.0**. 


---

## 💬 Community & Support

- 🐦 Follow us on X  (coming soon)
- 💬 Join our [Discord community] (coming soon)

---

## 🙏 Acknowledgments

Thanks to all open-source communities and LLM providers that made this project possible. Special thanks to Anthropic, DeepSeek, xAI, Alibaba Cloud, Ollama, and the Sentence‑Transformers project.

---

## 🌟 Star History

If you like this project, please give it a Star ⭐ to help more people discover it!

[![Star History Chart](https://api.star-history.com/svg?repos=yourname/AgentFounder&type=Date)](https://star-history.com/#yourname/AgentFounder&Date)

🍴 Fork and contribute — we welcome PRs!

🐦 Share your OAC journey on X with `#AgentFounder` and `#OneAgentCompany`

---

**AgentFounder — Because the best co-founder is code.** 🚀
```
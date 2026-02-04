# Multi-Agent Coding Assistant 🤖💻

A professional, local-first agentic system powered by **CrewAI**, designed to automate the software development lifecycle. By orchestrating specialized AI agents, this system researches technical requirements and generates production-ready code without relying on cloud APIs.

---

## 🚀 Key Features

* **Local Intelligence**: Runs entirely on **Ollama**, utilizing **Qwen2.5-Coder (7B)** for precise programming and **Llama 3.2** for reasoning.
* **Privacy-First**: Zero data leaves your machine; no OpenAI or Anthropic API keys are required.
* **Hardware Optimized**: Custom-tuned for **i5 processors** by disabling heavy OpenTelemetry (OTEL) tracing to maximize CPU efficiency.
* **Modular Configuration**: Agent roles, goals, and backstories are decoupled into YAML files for easy customization.
* **Traceable Results**: Automatically generates timestamped project folders in the `Results/` directory for every run.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Framework** | CrewAI |
| **Orchestration** | Ollama |
| **Models** | Qwen2.5-Coder:7b & Llama 3.2 |
| **Language** | Python 3.12+ |
| **Package Manager** | UV |
| **Environment** | Python-Dotenv |

---

## 🧠 Agent Personas

| Agent | Model | Primary Responsibility |
| :--- | :--- | :--- |
| **System Analyst** | `llama3.2` | Breaks down user prompts into technical tasks and research goals. |
| **Senior Developer** | `qwen2.5-coder:7b` | Writes clean, PEP8-compliant Python code based on analyst research. |

---

## 📦 Installation & Setup

  ### 1. Clone the Repository
  ```bash
  git clone [https://github.com/Bhavesh112004/Multi_Agent_Coding_Assitant.git](https://github.com/Bhavesh112004/Multi_Agent_Coding_Assitant.git)
  cd Multi_Agent_Coding_Assitant
  
  ### 2. Configure Environment: Initialize your local settings using the provided example:
  ```bash
  cp .env.example .env
  
  ### 3. Install Dependencies:
  ```bash
  pip install -r requirements.txt
  
  ### 4. Local Model Setup: Ensure Ollama is running, then pull the required models:
  ```bash
  ollama pull qwen2.5-coder:7b
  ollama pull llama3.2
  
  ### 5. Run the Assistant:
  ```bash
  python main.py

## 👨‍💻 Author
Bhavesh
GitHub: @Bhavesh112004
Role: Computer Engineer | Pune, Maharashtra
Focus: AI/ML, Agentic Workflows, and Local LLM Orchestration

---
title: Prompt Injection Detector
emoji: 🛡️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.36.1"
python_version: "3.10"
app_file: app.py
pinned: false
---
🛡️ Prompt Injection Detector Agent (OpenEnv)

An adaptive AI security system that detects, evaluates, and learns from prompt injection attacks in real time using a deterministic + reinforcement-style environment.

🚀 Overview

Prompt injection is one of the most critical vulnerabilities in modern LLM applications. This project provides a production-ready evaluation environment and adaptive detection agent that:

Detects direct, indirect, and adversarial prompt injections
Simulates real-world attack scenarios using mutation
Evaluates responses using deterministic grading
Improves detection over time via adaptive learning
🧠 Key Features
🔍 1. Detection Engine
Regex + pattern-based detection
Categories:
Override attacks
Role manipulation
Data exfiltration
Confidence scoring system
⚔️ 2. Adversarial Attack Generator
Dynamically mutates prompts
Simulates:
Obfuscation (ign0re, instr.)
Indirect injections
Prevents overfitting to static patterns
🧪 3. OpenEnv-Compatible Environment
Implements:
reset()
step()
state()
Task-based evaluation pipeline
Fully API-driven via FastAPI
📊 4. Deterministic Grading System
Reproducible scoring (no randomness)
Evaluates:
Detection accuracy
Attack classification
Severity estimation
🔁 5. Adaptive Learning Agent (Core Innovation)
Updates detection weights based on reward feedback
Reinforcement-style loop:
Detect → Evaluate → Learn → Improve
Enables continuous improvement against new attacks
🏗️ Architecture
User Input
   ↓
Attack Generator (Mutation)
   ↓
Detection Engine (Pattern + Weights)
   ↓
Category Mapping
   ↓
Grader (Deterministic Evaluation)
   ↓
Adaptive Agent (Weight Update)
📁 Project Structure
prompt-injection-env/
│
├── environment.py        # Main OpenEnv environment + API
├── detector.py          # Detection logic
├── attack_generator.py  # Adversarial mutation engine
├── agent.py             # Adaptive learning agent
├── graders.py           # Deterministic evaluation
├── models.py            # Data models (Pydantic)
├── tasks/               # Benchmark tasks
└── openenv.yaml         # OpenEnv config
⚙️ Installation
git clone <repo-url>
cd prompt-injection-env
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
▶️ Running the Server
python environment.py

Server runs at:

http://localhost:7860
🧪 API Usage
1. Reset Environment
POST /reset
2. Step (Run Detection)
POST /step

Body:

{}
PowerShell Example
Invoke-RestMethod -Uri "http://localhost:7860/reset" -Method POST
Invoke-RestMethod -Uri "http://localhost:7860/step" -Method POST -Body "{}" -ContentType "application/json"
📈 Example Output
{
  "reward": 0.85,
  "done": false,
  "info": {
    "task_id": "task_easy",
    "reward_breakdown": {...},
    "tasks_remaining": 3
  }
}
🧠 Learning Behavior

The system adapts based on feedback:

Correct Detection → Increase weight  
Incorrect Detection → Decrease weight

This allows:

Better handling of obfuscated attacks
Improved detection over time
🎯 Use Cases
Securing LLM chatbots
Protecting RAG pipelines
Enterprise AI safety layer
Red-teaming AI systems
🏆 Why This Matters

Unlike static filters, this system:

Learns from adversarial inputs
Provides explainable decisions
Offers deterministic evaluation
Is deployable in real-world AI pipelines
🔮 Future Improvements
Deep learning-based detection
Attack generation via LLMs
Visualization dashboard
Multi-turn conversation defense
📜 License

MIT License

👨‍💻 Author

Arshad Mahalkari
Computer Science Engineering Student
AI | ML | Systems | Open Source

⭐ Final Note

This project demonstrates how AI systems can move from static defense → adaptive security, making LLM deployments safer and more robust against evolving threats.
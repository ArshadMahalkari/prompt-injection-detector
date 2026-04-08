import gradio as gr
from inference import run_agent

def detect(prompt):
    result = run_agent(prompt)
    return result

demo = gr.Interface(
    fn=detect,
    inputs=gr.Textbox(lines=5, placeholder="Enter prompt to test injection..."),
    outputs="json",
    title="🛡️ Prompt Injection Detector",
    description="Adaptive AI agent that detects and learns from prompt injection attacks"
)

demo.launch()
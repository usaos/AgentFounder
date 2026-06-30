import gradio as gr
from app.utils.db import list_opps
from app.core.meaning import oracle
from app.core.scanner import scanner
from app.utils.crypto import get_secret, decrypt_env, encrypt_env
async def scan_btn():
    try:
        await scanner.scan_all_sources()
        return "Done"
    except Exception as e: return f"Err: {e}"
async def list_html():
    opps = await list_opps(10)
    h = "<h2>Opportunities</h2>"
    for o in opps: h += f"<div><b>{o['id']}</b>: {o['pain']}</div>"
    return h
def save_keys(c, g, q):
    env = decrypt_env()
    if c: env["ANTHROPIC_API_KEY"] = c
    if g: env["X_GROK_API_KEY"] = g
    if q: env["DASHSCOPE_API_KEY"] = q
    encrypt_env(env)
    return "Saved"
with gr.Blocks() as demo:
    with gr.Tab("Ops"):
        gr.Button("Scan").click(fn=scan_btn, outputs=gr.Textbox())
        demo.load(fn=list_html, outputs=gr.HTML())
    with gr.Tab("Config"):
        gr.Textbox("Claude Key").save(save_keys)
def mount_dashboard(app):
    gr.mount_gradio_app(app, demo, path="/dashboard")

# Entrypoint for Cloud Deployment (Streamlit Community Cloud, Hugging Face, etc.)
import os
import runpy

current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_app = os.path.join(current_dir, "dashboard", "app.py")
runpy.run_path(dashboard_app, run_name="__main__")

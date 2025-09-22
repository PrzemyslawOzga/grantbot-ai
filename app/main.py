import requests

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.api import endpoints

app = FastAPI(
    title="GrantBot.ai Backend",
    description="API for generating grant application sections using RAG",
    version="1.0.0",
)

app.include_router(endpoints.router, prefix="/api")


@app.get(path="/", response_class=HTMLResponse)
def main():
    """
    Main endpoint - returns a simple HTML form for generating a grant
    application section.
    """
    html_msg = f"""
    <h1>Welcome to GrantBot Backend API</h1>
    <p>To generate a grant application section, please fill out the form below:</p>
    <form action="/submit" method="post">
        <label><b>Company ID:</b></label>
        <input type="text" name="company_id" value="123"><br>
        
        <label><b>Section Type:</b></label>
        <input type="text" name="section_type" value="innovation_description"><br>
        
        <label><b>Text:</b></label><br>
        <textarea name="text" rows="4" cols="70">Describe GrantBot AI system.</textarea><br><br>
        
        <input type="submit" value="Generate Section">
    </form>
    """
    return html_msg


@app.post(path="/submit", response_class=HTMLResponse)
def submit_generate_section(
    company_id=Form(...), section_type=Form(...), text=Form(...)
):
    """
    Handles form submission, calls the API to generate a section, and returns
    results in HTML.
    """
    payload = {
        "company_id": company_id,
        "section_type": section_type,
        "text": text,
    }
    url = "http://127.0.0.1:8000/api/generate-section"
    response = requests.post(url=url, json=payload)

    if response.status_code == 200:
        data = response.json()
        generated_text = data.get("generated_text", "")
        sources = data.get("sources", [])

        if sources:
            sources_text = ", ".join(sources)
        else:
            sources_text = "No sources"

        html_msg = f"""
            <h2>Generated Section</h2>
            <p>{generated_text}</p>
            <h3>Sources</h3>
            <p>{sources_text}</p>
            <a href="/">Back</a>
        """
        return html_msg

    else:
        html_msg = f"""
            <h2>Error {response.status_code}</h2>
            <p>{response.json()}</p>
            <a href="/">Back</a>
        """
        return html_msg

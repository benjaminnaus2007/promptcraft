from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # Initialize result as None to prevent premature display
    error = None

    if request.method == "POST":
        about = request.form.get("about")
        role = request.form.get("role", "")
        goal = request.form.get("goal", "")
        audience = request.form.get("audience", "")
        style = request.form.get("style", "")
        focus = request.form.get("focus", "")
        twist = request.form.get("twist", "")
        hope = request.form.get("hope", "")

        if not about:
            return render_template("index.html", error="Please fill out the required field: What do you want the AI to do?")

        prompt = f"Generate a professional AI prompt based on the following inputs: The AI should {about}. Act like {role or 'a helpful assistant'}. The goal is {goal or 'to provide a clear solution'}. This is for {audience or 'a general audience'}. Use a {style or 'neutral'} tone. {focus or 'No specific focus'}. {twist or 'No additional twist'}. Address this hope or concern: {hope or 'None'}."

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://promptcraft-ruj2.onrender.com",  # Updated to match live URL
            "X-Title": "PromptCraft"
        }
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            error = f"Sorry, there was an error with the AI request: {str(e)}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
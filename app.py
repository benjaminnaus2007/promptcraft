from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "meta-llama/Llama-3.1-8b-instruct")

# System message for AI prompt crafting
system_message = (
    "You are an expert AI prompt crafter. Your job is to take the user's answers and generate a single, concise, high-quality prompt for an AI model. "
    "Never ask the user questions or request more information. Never return a list of questions. "
    "Always output a single, ready-to-use prompt that is clear, actionable, and professional. "
    "If some fields are left blank, use only the information provided. "
    "Keep the prompt a reasonable length (no more than 5 sentences unless more detail is absolutely necessary). "
    "Do not explain your reasoning, do not add commentary, and do not include instructions for the user—just return the final prompt, ready to copy and paste."
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    if request.method == "POST":
        try:
            # Collect form data
            about = request.form.get("about", "").strip()
            role = request.form.get("role", "").strip()
            goal = request.form.get("goal", "").strip()
            audience = request.form.get("audience", "").strip()
            style = request.form.get("style", "").strip()
            focus = request.form.get("focus", "").strip()
            twist = request.form.get("twist", "").strip()
            hope = request.form.get("hope", "").strip()

            if not about:
                error = "Please enter what you want the AI to do."
            else:
                # Construct user prompt
                user_prompt = (
                    f"Task: {about}\n"
                    + (f"Role: {role}\n" if role else "")
                    + (f"Goal: {goal}\n" if goal else "")
                    + (f"Audience: {audience}\n" if audience else "")
                    + (f"Style: {style}\n" if style else "")
                    + (f"Focus: {focus}\n" if focus else "")
                    + (f"Twist: {twist}\n" if twist else "")
                    + (f"Hope: {hope}" if hope else "")
                )

                # Send request to OpenRouter
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://promptcraft.onrender.com",  # Update with your Render URL later
                    "X-Title": "PromptCraft"
                }
                data = {
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_prompt}
                    ]
                }
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )
                resp.raise_for_status()
                result_json = resp.json()
                result = result_json["choices"][0]["message"]["content"].strip()
        except Exception as e:
            error = f"Sorry, there was an error with the AI request: {e}"

    return render_template("index.html", result=result, error=error, request=request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env variable
    app.run(host="0.0.0.0", port=port, debug=True)
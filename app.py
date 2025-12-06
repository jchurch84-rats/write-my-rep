from flask import Flask, request, render_template_string
import os
from groq import Groq   # ← we'll add this in a second

app = Flask(__name__)

# Put your Groq API key here (or in .env later)
GROQ_API_KEY = "gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"   # ← paste yours

client = Groq(api_key=GROQ_API_KEY)

HTML = """
<!doctype html>
<html>
<head>
    <title>Write My Rep</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        input, select, textarea { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 12px 24px; font-size: 16px; }
        .letter { background: #f8f8f8; padding: 20px; margin-top: 30px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Write My Rep</h1>
    <form method="post">
        <label>ZIP Code</label>
        <input name="zip" placeholder="90210" required>

        <label>Subject / Bill / Issue</label>
        <input name="topic" placeholder="potholes, school boards, whatever" required>

        <label>Your stance</label>
        <select name="stance" required>
            <option value="support">I support</option>
            <option value="oppose">I oppose</option>
        </select>

        <button type="submit">Generate Letter</button>
    </form>

    {% if letter %}
        <div class="letter">
            <h3>Your letter (ready to copy or send)</h3>
            <pre>{{ letter }}</pre>
            <button onclick="navigator.clipboard.writeText(`{{ letter | safe }}`)">Copy to Clipboard</button>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        zipcode = request.form["zip"]
        topic = request.form["topic"]
        stance = request.form["stance"].lower()

        prompt = f"""
        Write a short, polite, firm letter (3-4 paragraphs max) from a constituent in ZIP {zipcode} who {stance}s the following issue: {topic}.
        Tone: respectful but unmistakably angry. No insults, no threats. End with "Sincerely, A Concerned Citizen".
        """

        completion = client.chat.completions.create(
            model="llama3-70b-8192",      # or mixtral-8x7b-32768 — both are free tier
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )

        letter = completion.choices[0].message.content.strip()

        return render_template_string(HTML, letter=letter)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True) 


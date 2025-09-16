import os
import csv
from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Set GROQ_API_KEY in environment or .env file")

client = Groq(api_key=GROQ_API_KEY)

CSV_PATH = "call_analysis.csv"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")


def call_groq_for_summary_and_sentiment(transcript: str) -> dict:
    """
    Sends the transcript to Groq Chat Completions API asking for:
      - a 2-3 sentence summary
      - a sentiment: Positive / Neutral / Negative

    Returns a dict: {"summary": ..., "sentiment": ...}
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise assistant. Respond ONLY with valid JSON and no other text. "
                "The JSON must have exactly two keys: 'summary' (2-3 sentence summary) and "
                "'sentiment' (one of: Positive, Neutral, Negative). Example:\n"
                '{"summary":"Customer reported late delivery.","sentiment":"Negative"}'
            ),
        },
        {"role": "user", "content": f"Transcript:\n{transcript}"},
    ]

    resp = client.chat.completions.create(
        model="compound-beta",
        messages=messages,
        max_tokens=300,
        temperature=0.0,
    )

    text = ""
    try:
        text = resp.choices[0].message.content
    except Exception:
        text = getattr(resp.choices[0], "text", "")

    # Debug: Print what Groq actually returned
    print("Groq raw response:", text)

    import json, re

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            j = json.loads(match.group(0))
            summary = j.get("summary", "").strip()
            sentiment = j.get("sentiment", "").strip()
            return {"summary": summary, "sentiment": sentiment}
        except Exception as e:
            print("⚠️ JSON parse failed:", e)

    # Heuristic fallback
    summary = ""
    sentiment = ""
    for line in text.splitlines():
        l = line.strip()
        if l.lower().startswith("summary"):
            summary = l.split(":", 1)[1].strip() if ":" in l else summary
        if l.lower().startswith("sentiment"):
            sentiment = l.split(":", 1)[1].strip() if ":" in l else sentiment

    # Final fallback if still empty
    if not summary:
        summary = (text.strip()[:400] + ("..." if len(text.strip()) > 400 else "")).strip()

    if not sentiment:
        lowered = text.lower()
        negative_words = [
            "frustrat", "angry", "not happy", "upset", "complain",
            "bad", "unsatisfied", "failed", "poor", "terrible", "hate"
        ]
        positive_words = [
            "thank", "great", "happy", "awesome", "good", "satisfied",
            "pleased", "excellent", "love", "fantastic", "amazing"
        ]
        if any(w in lowered for w in negative_words):
            sentiment = "Negative"
        elif any(w in lowered for w in positive_words):
            sentiment = "Positive"
        else:
            sentiment = "Neutral"

    return {"summary": summary, "sentiment": sentiment}


def save_to_csv(transcript: str, summary: str, sentiment: str, path: str = CSV_PATH):
    file_exists = os.path.isfile(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Transcript", "Summary", "Sentiment"])
        writer.writerow([transcript, summary, sentiment])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        transcript = request.form.get("transcript", "").strip()
        if not transcript:
            flash("Please paste a transcript before submitting.", "error")
            return redirect(url_for("index"))

        try:
            result = call_groq_for_summary_and_sentiment(transcript)
        except Exception as e:
            flash(f"Error calling Groq API: {e}", "error")
            return redirect(url_for("index"))

        summary = result.get("summary", "")
        sentiment = result.get("sentiment", "")

        try:
            save_to_csv(transcript, summary, sentiment)
        except Exception as e:
            flash(f"Failed to save CSV: {e}", "error")

        return render_template(
            "index.html",
            transcript=transcript,
            summary=summary,
            sentiment=sentiment,
            saved=True,
        )

    preview = None
    if os.path.isfile(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            preview = df.tail(5).to_dict(orient="records")
        except Exception:
            preview = None

    return render_template("index.html", preview=preview)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

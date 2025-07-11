from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your own SERPAPI key
SERPAPI_KEY = "894807be90e816940e80a2259a46174f3dd1ff55ed27cab5bbc6665592fc0e82"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Use SerpAPI to search the web for answers
    params = {
        "q": question,
        "api_key": SERPAPI_KEY,
        "num": "5",
        "engine": "google"
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params)
        result = res.json()
        answer = ""

        if "answer_box" in result and "answer" in result["answer_box"]:
            answer = result["answer_box"]["answer"]
        elif "organic_results" in result and len(result["organic_results"]) > 0:
            snippets = [r.get("snippet", "") for r in result["organic_results"][:5] if r.get("snippet")]
            answer = "\n\n".join(snippets)
        else:
            answer = "Hmm... I couldn't find a solid answer right now, but I'm learning more every day!"

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

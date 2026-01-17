from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    matches = []
    error = None

    if request.method == "POST":
        text = request.form.get("test_string")
        pattern = request.form.get("regex")

        try:
            matches = re.findall(pattern, text)
        except re.error:
            error = "Invalid Regular Expression"

    return render_template("index.html", matches=matches, error=error)
if __name__ == "__main__":
    app.run(debug=True)            

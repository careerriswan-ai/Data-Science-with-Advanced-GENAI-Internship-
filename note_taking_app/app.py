from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory notes storage (for this small demo app).
# NOTE: This resets when the server restarts.
notes = []


@app.route('/', methods=["GET", "POST"])
def index():
    """Home route.

    - GET  : Render the page with existing notes.
    - POST : Add a new note and redirect back to GET.
    """

    if request.method == "POST":
        # Form data is sent in request.form, not request.args
        note = request.form.get("note", "").strip()

        # Avoid adding empty notes
        if note:
            notes.append(note)

        # Redirect prevents duplicate form submission on refresh
        return redirect(url_for("index"))

    return render_template("home.html", notes=notes)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, URL
import string
import random
import validators

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "rizstorm_url_shortener_key"

db.init_app(app)

with app.app_context():
    db.create_all()


def create_random_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_unique_code():

    while True:
        code = create_random_code()
        already = URL.query.filter_by(short_code=code).first()
        if not already:
            return code


@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None

    if request.method == "POST":
        long_url = request.form.get("original_url")
        custom_alias = request.form.get("custom_alias")

        
        if not long_url or not validators.url(long_url):
            flash("Invalid URL. Please enter like: https://google.com", "danger")
            return render_template("index.html", short_url=None)

        
        if custom_alias:
            custom_alias = custom_alias.strip()

            
            if not custom_alias.isalnum():
                flash("Custom alias should contain only letters and numbers (no spaces/symbols).", "warning")
                return render_template("index.html", short_url=None)

            alias_exists = URL.query.filter_by(short_code=custom_alias).first()
            if alias_exists:
                flash("This custom alias is already taken. Try another one.", "warning")
                return render_template("index.html", short_url=None)

            short_code = custom_alias
        else:
            short_code = get_unique_code()

        
        new_entry = URL(original_url=long_url, short_code=short_code)
        db.session.add(new_entry)
        db.session.commit()

        short_url = request.host_url + short_code
        flash("Short link created successfully!", "success")

    return render_template("index.html", short_url=short_url)


@app.route("/history")
def history():
    all_urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template("history.html", urls=all_urls)


@app.route("/<short_code>")
def open_short_url(short_code):
    entry = URL.query.filter_by(short_code=short_code).first()

    if entry:
        
        entry.clicks += 1
        db.session.commit()
        return redirect(entry.original_url)

    flash("Short link not found!", "danger")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

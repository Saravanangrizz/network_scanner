from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Scan
from scanner import scan_network
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://log_user:uiCHh0hvy13nx53PrzPNiLoIP2bJRllT@dpg-cvok1dq4d50c73bintn0-a/log_analysis_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("register"))
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, request.form["password"]):
            flash("Invalid credentials.")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    results = []
    if request.method == "POST":
        network = request.form["network"]
        results = scan_network(network)
        for ip, ports in results:
            record = Scan(user_id=current_user.id, ip_address=ip, open_ports=", ".join(map(str, ports)))
            db.session.add(record)
        db.session.commit()
        flash("Scan complete and saved to history.")
    history = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.timestamp.desc()).all()
    return render_template("dashboard.html", history=history, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

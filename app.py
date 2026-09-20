from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import joblib
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SECRET KEY

app.secret_key = "home_ai_house_price_secret_key"


# DATABASE

DATABASE = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create database/table when app starts
init_db()

# LOAD MACHINE LEARNING MODEL

try:

    model = joblib.load("house_price_model.pkl")

    print("House price model loaded successfully.")

except Exception as e:

    model = None

    print("Error loading model:", e)

# HOME / INDEX

@app.route("/")
def home():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        name=session.get("name")
    )

# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        terms = request.form.get("terms")


        # Required fields

        if not name or not email or not password or not confirm_password:

            return render_template(
                "register.html",
                error="Please fill all required fields."
            )


        # Terms & Conditions

        if not terms:

            return render_template(
                "register.html",
                error="Please accept the Terms & Conditions."
            )

        # Password Match

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        # Password Length

        if len(password) < 6:

            return render_template(
                "register.html",
                error="Password must be at least 6 characters."
            )


        # Check Existing Email

        conn = get_db_connection()

        existing_user = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()


        if existing_user:

            conn.close()

            return render_template(
                "register.html",
                error="An account with this email already exists."
            )

        # Hash Password

        hashed_password = generate_password_hash(password)


        # Insert User

        try:

            conn.execute(
                """
                INSERT INTO users
                (name, email, phone, password)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    phone,
                    hashed_password
                )
            )

            conn.commit()
            conn.close()


            return redirect(url_for("login"))


        except Exception as e:

            conn.close()

            print("Registration error:", e)

            return render_template(
                "register.html",
                error="Registration failed. Please try again."
            )


    return render_template("register.html")


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")



        # Validate Input


        if not email or not password:

            return render_template(
                "login.html",
                error="Please enter email and password."
            )


        # Find User

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        conn.close()


        # Check User + Password

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["email"] = user["email"]


            return redirect(url_for("home"))


        # Invalid Login

        return render_template(
            "login.html",
            error="Invalid email or password."
        )


    return render_template("login.html")


# HOUSE PRICE PREDICTION

@app.route("/predict", methods=["POST"])
def predict():

    # Login Check

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "error": "Please login first."
        }), 401


    # Check Model

    if model is None:

        return jsonify({
            "success": False,
            "error": "House price model is not loaded."
        }), 500


    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "success": False,
                "error": "No prediction data received."
            }), 400


        # CURRENT MODEL FEATURES

        house = pd.DataFrame([{

            "propertyType":
                str(data.get("propertyType", "")).strip(),

            "furnishing":
                str(data.get("furnishing", "")).strip(),

            "flrNum":
                float(data.get("flrNum", 0)),

            "facing":
                str(data.get("facing", "")).strip(),

            "totalFlrNum":
                float(data.get("totalFlrNum", 0)),

            "city":
                str(data.get("city", "")).strip(),

            "carpetArea":
                float(data.get("carpetArea", 0)),

            "bedrooms":
                float(data.get("bedrooms", 0)),

            "bathrooms":
                float(data.get("bathrooms", 0))

        }])


        # Prediction

        prediction = model.predict(house)

        price = float(prediction[0])


        # Prevent negative prediction
        if price < 0:
            price = 0


        # Price Formatting

        if price >= 10000000:

            formatted_price = (
                f"₹{price:,.0f}"
                f" ({price / 10000000:.2f} Crore)"
            )

        elif price >= 100000:

            formatted_price = (
                f"₹{price:,.0f}"
                f" ({price / 100000:.2f} Lakh)"
            )

        elif price >= 1000:

            formatted_price = (
                f"₹{price:,.0f}"
                f" ({price / 1000:.2f} Thousand)"
            )

        else:

            formatted_price = f"₹{price:,.0f}"


        # Send Response

        return jsonify({

            "success": True,

            "price": price,

            "formatted_price": formatted_price

        })


    except ValueError:

        return jsonify({

            "success": False,

            "error": "Please enter valid numeric values."

        }), 400


    except Exception as e:

        print("Prediction error:", e)

        return jsonify({

            "success": False,

            "error": "Unable to predict house price."

        }), 500


# LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# RUN APPLICATION

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
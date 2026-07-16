import re
import sqlite3
from datetime import datetime
from difflib import SequenceMatcher

import pandas as pd
import flask
from utils.database import create_table
from utils.database import get_all_users
from models.validator import validate
from models.validator import save
from utils.redundancy_checker import classify_record
DATABASE = "database.db"

app = flask.Flask(__name__)

stats = {
    "duplicates_blocked": 0,
    "false_positives": 0
}


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


initialize_database()


def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/add", methods=["POST"])
def add_record():

    data = flask.request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()

    if not name or not email or not phone:
        return flask.jsonify({
            "status": "error",
            "message": "All fields are required."
        }), 400

    if not valid_email(email):
        return flask.jsonify({
            "status": "error",
            "message": "Invalid Email."
        })

    if not valid_phone(phone):
        return flask.jsonify({
            "status": "error",
            "message": "Phone number must contain exactly 10 digits."
        })

    conn = get_connection()
    cursor = conn.cursor()

    duplicate = cursor.execute(
        "SELECT * FROM records WHERE email=? OR phone=?",
        (email, phone)
    ).fetchone()

    if duplicate:

        stats["duplicates_blocked"] += 1

        conn.close()

        return flask.jsonify({
            "status": "duplicate",
            "message": "Duplicate Record Found."
        })

    rows = cursor.execute(
        "SELECT name FROM records"
    ).fetchall()

    for row in rows:

        score = SequenceMatcher(
            None,
            name.lower(),
            row["name"].lower()
        ).ratio()

        if score >= 0.90:

            stats["false_positives"] += 1

            conn.close()

            return flask.jsonify({
                "status": "false_positive",
                "message": "Possible False Positive Detected."
            })

    cursor.execute(
        """
        INSERT INTO records
        (name,email,phone,created_at)
        VALUES(?,?,?,?)
        """,
        (
            name,
            email,
            phone,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return flask.jsonify({
        "status": "success",
        "message": "Unique Record Added Successfully."
    })


@app.route("/records")
def records():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM records ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return flask.jsonify(
        [dict(row) for row in rows]
    )


@app.route("/delete/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM records WHERE id=?",
        (record_id,)
    )

    conn.commit()
    conn.close()

    return flask.jsonify({
        "status": "success",
        "message": "Record Deleted Successfully."
    })


@app.route("/search")
def search():

    keyword = flask.request.args.get("q", "")

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM records
        WHERE
        name LIKE ?
        OR email LIKE ?
        OR phone LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    ).fetchall()

    conn.close()

    return flask.jsonify(
        [dict(row) for row in rows]
    )


@app.route("/stats")
def statistics():

    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM records"
    ).fetchone()[0]

    conn.close()

    return flask.jsonify({

        "total_records": total,

        "duplicates_blocked":
        stats["duplicates_blocked"],

        "false_positives":
        stats["false_positives"]

    })


if __name__ == "__main__":
    app.run(debug=True)
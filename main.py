from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)
DB_NAME = "online-store.db"

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount INTEGER NOT NULL
        )
    """)
    connection.commit()
    connection.close()

# GET /api/health
@app.get("/api/health")
def check_health():
    return jsonify({"status": "ok"}), 200

@app.post("/api/coupons")
def post_coupon():

    try:
        new_coupon = request.get_json()
        code = new_coupon.get("code")
        discount = new_coupon.get("discount")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO coupons (code, discount)
                VALUES (?, ?);
        """, (code, discount))
        connection.commit()
        connection.close()
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"success": False, "message": e}), 400 



init_db()

app.run(debug=True)
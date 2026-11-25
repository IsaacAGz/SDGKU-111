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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image  TEXT NOT NULL
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

        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400 
    finally:
            connection.close()

@app.get("/api/coupons")
def get_coupons():
    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory= sqlite3.Row # makes each row behave like a dictionary
        cursor = connection.cursor()
        coupons_db = cursor.execute("SELECT code, discount FROM coupons").fetchall() # fetchall retrieves all the rows fromt he result of the query

        coupons = [dict(coupon) for coupon in coupons_db]

        return jsonify({"success": True, "coupons": coupons}), 200

    except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400 
    finally:
            connection.close()

@app.get("/api/coupons/<int:coupon_id>")
def get_coupons_id(coupon_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row # makes each row behave like a dictionary
        cursor = connection.cursor()
        coupon_db = cursor.execute("SELECT code, discount FROM coupons WHERE id = ?", (coupon_id,)).fetchone() # fetchall retrieves all the rows fromt he result of the query

        coupon = dict(coupon_db)

        return jsonify({
            "success": True,
            "coupon": dict(coupon)
        }), 200

    except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400 
    finally:
            connection.close()


# ================ PRODUCTS ================================================

# POST "/api/products to add products to products TABLE
@app.post("/api/products")
def post_product():
    new_product = request.get_json()

    name = new_product.get("name")
    price = new_product.get("price")
    category = new_product.get("category")
    image = new_product.get("image")

    try:

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, category, image)
                VALUES (?, ?, ?, ?);
        """, (name, price, category, image))
        connection.commit()

        return jsonify({"success": True}), 201
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400 
    finally:
        connection.close()

# GET /api/products
@app.get("/api/products")
def get_products():
     

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
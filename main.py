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



#DELTE /api/coupons/<>
@app.delete("/api/coupons/<int:coupon_id>")
def delete_coupon(coupon_id):

    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
        coupon_db = cursor.fetchone()

        if not coupon_db:
             return({"status": False, "message": "coupon not found"}), 404

        cursor.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
        connection.commit()

        return jsonify({"status": True, "message": "coupon deleted"}), 200
    except Exception as e:
         return jsonify({"status": False, "message": str(e)}), 400
    finally:
        if not connection:
            connection.close()

# Update /api/coupons/<>
@app.put("/api/coupons/<int:coupon_id>")
def update_coupon(coupon_id):
    try:
        new_coupon = request.get_json()
        code = new_coupon.get("code")
        discount = new_coupon.get("discount")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
        coupon_db = cursor.fetchone()

        if not coupon_db:
            return jsonify({"status": False, "message": "coupon not found"}), 404

        cursor.execute("""
            UPDATE coupons 
            SET code = ?, discount = ? 
            WHERE id = ?
        """, 
        (code, discount, coupon_id))
        connection.commit()

        return jsonify({"status": True, "message": "coupon updated"}), 200
    except Exception as e:
         return jsonify({"status": False, "messge": str(e)}), 400
    finally:
        if connection:
             connection.close()

"""
    GET /api/products
        Get all products

    GET /api/products/<product_id>
          Retrieve a single product by its ID.
          Return a JSON object with all product details.
          ⁠If the product does not exist, return a 404 error with a helpful message.

    PUT /api/products/<product_id>
          ⁠Update an existing product.
          ⁠Accept a JSON body with any of the following fields: name, price, category and image.
          ⁠If the product does not exist, return a 404 error.
          ⁠Validate that the category is one of the allowed values: "electronics", "education", "food".

    DELETE /api/products/<product_id>
        Delete the specified product.
        ⁠If the product does not exist, return a 404 error.
"""

#Get /api/products
@app.get("/api/products")
def get_all_products():
    

    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        products_db = cursor.execute(" SELECT name, price, category FROM products").fetchall()
        products = [dict(product) for product in products_db]
        return jsonify({"success": True, "products": products}), 200
    except Exception as e:
         return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if connection:
            connection.close()

# GET /api/products/<products_id>
@app.get("/api/products/<int:product_id>")
def get_product(product_id):

    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        product_row = cursor.execute("SELECT name, price, category FROM products WHERE id = ?", (product_id,)).fetchone()
        

        if product_row is None:
            return jsonify({"success": False, "message": "product not found"}), 404

        product = dict(product_row)
        return jsonify({"success": True, "product": product}), 200
    except Exception as e:
         return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if connection:
            connection.close()

# PUT /api/products/<product_id>
@app.put("/api/products/<int:product_id>")
def update_product(product_id):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        product_row = cursor.execute("SELECT name, price, category FROM products WHERE id = ?", (product_id,))

        if not product_row:
             return jsonify({"status": False, "message": "product not found"}), 404

        cursor.execute("INSERT INTO")
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400
    finally:
        if connection:
            connection.close()
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

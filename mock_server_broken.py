import json
from flask import Flask, request, jsonify

app = Flask(__name__)

users_db = {}
next_user_id = 101

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    global next_user_id

    # ❌ BUG 1: dict guard yok — body null/array gelirse çöküyor
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")

    # ❌ BUG 1 devam: Tip kontrolü yok — null, false, {} kabul ediliyor
    # Schemathesis negative_data_rejection + not_a_server_error kontrolleri FAIL olur

    user_id = next_user_id
    users_db[user_id] = {"username": username, "email": email}
    next_user_id += 1

    return jsonify({"userId": user_id}), 201


@app.route('/api/v1/users/<int:user_id>/orders', methods=['POST'])
def create_order(user_id):
    data = request.get_json(silent=True) or {}

    quantity = data.get("quantity")
    if type(quantity) is not int or quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    product_id = data.get("product_id")
    if type(product_id) is not int:
        return jsonify({"error": "Invalid product_id"}), 400

    # ❌ BUG 2: use_after_free — silinen kullanıcıya sipariş verilebiliyor
    # if user_id not in users_db: satırı kasıtlı olarak kaldırıldı
    return jsonify({"orderId": 999, "status": "success!"}), 201


@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id]
        return '', 204
    return jsonify({"error": "User not found"}), 404


# ❌ BUG 3: X-Security-Protection başlığı EKSİK — custom_security_header_check FAIL olur
# @app.after_request hook kasıtlı olarak kaldırıldı


@app.errorhandler(500)
def server_error(e):
    r = jsonify({"error": "Internal Server Error"})
    r.status_code = 500
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

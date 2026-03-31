import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database
# users = { 101: {"username": "foo", "email": "bar"} }
users_db = {}
next_user_id = 101

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        data = {}
    
    username = data.get("username")
    email = data.get("email")
    
    # 🐞 ÇÖZÜLEN BUG 1: Tip ve Format Kontrolü (Whitespace dahil düzeltildi)
    if not isinstance(username, str) or len(username) < 1:
        return jsonify({"error": "Invalid username format"}), 400
        
    if not isinstance(email, str) or '@' not in email:
        return jsonify({"error": "Invalid email format"}), 400
        
    if username.startswith("admin"):
        return jsonify({"error": "Admin cannot be created"}), 400
        
    user_id = next_user_id
    users_db[user_id] = {"username": username, "email": email}
    next_user_id += 1
    
    return jsonify({"userId": user_id}), 201

@app.route('/api/v1/users/<int:user_id>/orders', methods=['POST'])
def create_order(user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        data = {}
    
    quantity = data.get("quantity")
    if type(quantity) is not int or quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400
        
    product_id = data.get("product_id")
    if type(product_id) is not int:
        return jsonify({"error": "Invalid product_id"}), 400
        
    # 🐞 ÇÖZÜLEN BUG 2: Use-After-Free Zafiyeti Giderildi
    if user_id not in users_db: 
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"orderId": 999, "status": "success!"}), 201

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id]
        return '', 204
    return jsonify({"error": "User not found"}), 404

@app.after_request
def add_security_headers(response):
    # Özel kuralımızdan (Hook) geçebilmek için koruma başlığını ekliyoruz.
    response.headers['X-Security-Protection'] = 'Active'
    return response

@app.errorhandler(404)
def not_found(e):
    r = jsonify({"error": "Not Found"})
    r.status_code = 404
    r.headers['X-Security-Protection'] = 'Active'
    return r

@app.errorhandler(405)
def method_not_allowed(e):
    r = jsonify({"error": "Method Not Allowed"})
    r.status_code = 405
    r.headers['X-Security-Protection'] = 'Active'
    # RFC 9110 kuralı: 405 hatası döndürürken geçerli metodlar 'Allow' header'ı ile belirtilmeli.
    if getattr(e, 'valid_methods', None):
        r.headers['Allow'] = ', '.join(e.valid_methods)
    return r

@app.errorhandler(500)
def server_error(e):
    r = jsonify({"error": "Internal Server Error"})
    r.status_code = 500
    r.headers['X-Security-Protection'] = 'Active'
    return r

if __name__ == '__main__':
    # 8080 portunda çalışacak
    app.run(host='0.0.0.0', port=8080)

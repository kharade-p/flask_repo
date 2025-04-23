from flask import Flask, request, jsonify
import psycopg2

from config import Config
from models import User, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/users')
def get_users():
    users = User.query.all()
    # return jsonify({'name':'Pratima'})
    return jsonify([user.to_dict() for user in users])


@app.route('/users', methods=['POST'])
def users():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415  # Ensure JSON request

    data = request.get_json()
    new_user = User(username=data.get('username'), email=data.get('email'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user =  User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['PUT','PATCH'])
def update_user(user_id):
    data = request.get_json()
    user =  User.query.get_or_404(user_id)


    if request.method == 'PUT':  # Replace entire user
        if 'username' not in data or 'email' not in data:
            return jsonify({"error": "Both 'username' and 'email' are required"}), 400
        user.username = data['username']
        user.email = data['email']

    elif request.method == 'PATCH':  # Update only provided fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']

    db.session.commit()
    return jsonify(user.to_dict())

    # user.username= data['username']
    # user.email= data['email']
    # db.session.commit()
    # return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user =  User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '',204


# @app.route('/users/<int:user_id>', methods=['PATCH'])
# def modify_user(user_id):
#     user = User.query.get_or_404(user_id)
#     data = request.get_json()

#     if 'username' in data:
#         user.username = data['username']
#     if 'email' in data:
#         user.email = data['email']
    
#     db.session.commit()
#     return jsonify(user.to_dict())

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True,port=5001)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(_name_)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    seat = db.Column(db.Integer, nullable=False)  # Changed column name from 'row' to 'seat'
    column = db.Column(db.Integer, nullable=False)

@app.route('/reserve_seat', methods=['POST'])
def reserve_seat():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    seat = data.get("seat")

    user = User(name=name, email=email, seat=seat)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Seat reserved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to reserve seat. Error: {str(e)}'}), 500

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
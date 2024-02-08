from creation import app, db, User
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class UserResource(Resource):
    # Get Data
    def get(self, email=None):
        if email:
            user = User.query.filter(User.email == email).first()
            if user:
                return {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    # 'password': user.password,
                    'mobile_number': user.mobile_number,
                    'user_type': user.user_type.name,
                    'is_active': user.is_active,
                    'is_validated': user.is_validated
                }
            else:
                return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            # users = User.filter_by(username=args['username']).all()
            return [{
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                # 'password': user.password,
                'mobile_number': user.mobile_number,
                'user_type': user.user_type.name,
                'is_active': user.is_active,
                'is_validated': user.is_validated
            } for user in users]
            
    # Adding data
    def post(self):
        try:
            data = request.get_json()

            # Check if email already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {'error': 'User with this email already exists'}, 409

            # Check if user_type is valid
            valid_user_types = ['SUPER_ADMIN', 'ADMIN', 'OWNER', 'TENANT']
            if data['user_type'] not in valid_user_types:
                return {'error': 'Invalid user type'}, 400

            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction
            print(f"Error creating user: {str(e)}")
            return {'error': 'Error creating user'}, 500

    # Editing/Updating Data
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.mobile_number = data['mobile_number']
            db.session.commit()
            return {'message': 'User updated successfully'}
        else:
            return {'message': 'User not found'}, 404

    # Delete Data
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return {'message': 'User not found'}, 404
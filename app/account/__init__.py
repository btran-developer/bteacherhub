from flask import Blueprint, jsonify, request
from app.models import User
from app import db

bp = Blueprint('account', __name__)


@bp.route('/account', methods=['POST'])
def create_account():
    """
    Create a new user
    """
    data = request.get_json()

    if 'username' not in data:
        return jsonify({'message': '"username" is required.'}), 400

    if 'password' not in data:
        return jsonify({'message': '"password" is required.'}), 400

    username = data['username']
    password = data['password']
    is_admin = True if 'is_admin' in data else False

    try:
        if User.query.filter_by(username=username).count() == 0:
            user = User(username=username, is_admin=is_admin)
            user.set_password(password=password)
            db.session.add(user)
            db.session.commit()
            message = 'User is successfully created'
        else:
            message = 'This username is taken. Please try another one.'
    except Exception as err:
        return jsonify({'message': 'Failed to create user.', 'error': str(err)}), 500

    return jsonify({'message': message}), 200


@bp.route('/account/reset-password', methods=['POST'])
def reset_account_password():
    """
    Change the account password
    """
    data = request.get_json()

    if 'username' not in data:
        return jsonify({'message': '"username" is required.'}), 400

    if 'new_password' not in data:
        return jsonify({'message': '"new_password" is required.'}), 400

    username = data['username']
    new_password = data['new_password']

    try:
        user_query = User.query.filter_by(username=username)

        if user_query.count() > 0:
            user = user_query.all()[0]
            user.set_password(password=new_password)
            db.session.add(user)
            db.session.commit()
            message = 'Password is successfully changed.'
        else:
            message = 'User does not exist.'
    except Exception as err:
        return jsonify({'message': 'Failed to reset password.', 'error': str(err)}), 500

    return jsonify({'message': message}), 200


@bp.route('/account/set-is-admin', methods=['GET'])
def set_account_to_admin():
    """
    Assign the user as admin
    """
    if 'username' not in request.args:
        return jsonify({'message': '"username" is required.'}), 400

    username = request.args['username']

    try:
        user_query = User.query.filter_by(username=username)

        if user_query.count() > 0:
            user = user_query.all()[0]
            user.is_admin = True
            db.session.add(user)
            db.session.commit()
            message = 'User is successfully set to admin.'
        else:
            message = 'User does not exist.'
    except Exception as err:
        return jsonify({'message': 'Failed to set account to admin.', 'error': str(err)}), 500

    return jsonify({'message': message}), 200


@bp.route('/account/remove-admin-privilege', methods=['GET'])
def remove_admin_privilege():
    """
    Unassign the user as admin
    """
    if 'username' not in request.args:
        return jsonify({'message': '"username" is required.'}), 400

    username = request.args['username']

    try:
        user_query = User.query.filter_by(username=username)

        if user_query.count() > 0:
            user = user_query.all()[0]
            user.is_admin = False
            db.session.add(user)
            db.session.commit()
            message = 'Admin privilege is successfully removed from the account.'
        else:
            message = 'User does not exist.'
    except:
        return jsonify({'message': 'Failed to remove admin privilege from account.'}), 500

    return jsonify({'message': message}), 200

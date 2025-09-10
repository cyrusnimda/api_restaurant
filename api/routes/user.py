from flask import Blueprint, jsonify

from api.controllers import BookingController
from api.decorators import token_required
from api.models_schemas import users_schema, user_schema, bookings_schema
from api.models import db, User


router = Blueprint("user", __name__, url_prefix="/users")


@router.route('/')
@token_required(role_needed='Admin')
def get_users(current_user):
    users = User.query.all()
    return users_schema.jsonify(users)


@router.route('/me/bookings')
@token_required()
def get_user_bookings(current_user):
    bookingManager = BookingController()
    bookings = bookingManager.get_bookings_from_user(current_user)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'bookings': bookings_json,
            'current_user': current_user.name
        }
    )


@router.route('/<int:user_id>')
@token_required(role_needed='Admin')
def get_user_id(current_user, user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)


@router.route('/<int:user_id>', methods=['DELETE'])
@token_required(role_needed='Admin')
def remove_user_id(current_user, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted.'})


@router.route('/me')
@token_required()
def get_user_me(current_user):
    return user_schema.jsonify(current_user)
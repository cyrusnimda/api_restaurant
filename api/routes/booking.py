from flask import Blueprint, app, jsonify
from flask import request
from api.controllers import BookingController
from api.decorators import token_required, check_mandatory_parameters
from api.models_schemas import bookings_schema, booking_schema
from api.models import db, Booking, Table
from api.models import DateUnknownTypeValidation, DateTimeValidation, PersonsNumberValidation

router = Blueprint("bookings", __name__, url_prefix="/bookings")



@router.route('')
@token_required()
@check_mandatory_parameters(["date"])
def get_bookings(current_user):
    try:
        dateValidator = DateUnknownTypeValidation(request.args.get('date'), app.config)
        dateValidator.validate()
        bookingDate = dateValidator.date
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    bookingManager = BookingController()
    bookings = bookingManager.get_bookings_from_date(bookingDate)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookings_json,
            'totalTables': Table.query.count(),
            'current_user': current_user.name
        }
    )


@router.route('/<int:booking_id>')
@token_required()
def get_booking_id(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return booking_schema.jsonify(booking)


@router.route('/<int:booking_id>', methods=['DELETE'])
@token_required('Admin')
def remove_booking_id(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted.'})


@router.route('', methods=['POST'])
@check_mandatory_parameters(["date", "persons", "name"])
@token_required()
def create_booking(current_user):
    req_data = request.get_json(force=True)

    # We accept datetime format only
    try:
        dateValidator = DateTimeValidation(req_data["date"], app.config)
        dateValidator.validate(validatePastRule = True)
        bookingDate = dateValidator.date

        personsValidator = PersonsNumberValidation(req_data["persons"])
        personsValidator.validate()
        persons = personsValidator.persons
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    # Create the booking object, without tables.
    booking = Booking(creator=current_user, persons=persons, booked_at=bookingDate, name=req_data["name"] )

    bookingManager = BookingController()
    try:
        bookingManager.save_booking(booking)
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    return jsonify(
        {
        'status': 'OK',
        'booking': booking_schema.dump(booking).data
        }
    )
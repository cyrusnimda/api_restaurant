from flask import Blueprint, jsonify

router = Blueprint("restaurant", __name__, url_prefix="/restaurants")

@router.route("")
def get_restaurants():
    from api.models import Restaurant
    from api.models_schemas import restaurants_schema
    restaurants = Restaurant.query.all()
    return restaurants_schema.jsonify(restaurants)


@router.route('/<int:restaurant_id>')
def get_restaurant_id(restaurant_id):
    from api.models import Restaurant
    from api.models_schemas import restaurant_schema
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return restaurant_schema.jsonify(restaurant)
from flask import Blueprint
from api.models import Table
from api.models_schemas import tables_schema, table_schema


router = Blueprint("tables", __name__, url_prefix="/tables")


@router.route('')
def get_tables():
    tables = Table.query.all()
    return tables_schema.jsonify(tables)


@router.route('/<int:table_id>')
def get_table_id(table_id):
    table = Table.query.get_or_404(table_id)
    return table_schema.jsonify(table)
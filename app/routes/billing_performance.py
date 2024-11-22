from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func
from app.models.units import Unit
from app.models.bills import Bill
from ..extensions import db

billing_performance_bp = Blueprint('billingPerformance', __name__)

@billing_performance_bp.route('/billing-performance', methods=['GET'])
def get_billing_performance():
    month = request.args.get('month')  # e.g., "10" for October
    year = request.args.get('year')  # e.g., "2000"
    status = request.args.get('status')  # Added status filter

    query = db.session.query(
        Unit.tower_number,
        Bill.bill_type,
        Bill.status,
        func.sum(Bill.total_amount).label('total_cost'),
        func.avg(Bill.total_amount).label('average_cost')
    ).join(Unit, Unit.unit_id == Bill.unit_id)  # Ensure proper join
    
    # Filtering by month and year
    if month and year:
        query = query.filter(
        extract('year', Bill.due_date) == year,
        extract('month', Bill.due_date) == month
    )
    elif year:
        query = query.filter(extract('year', Bill.due_date) == year)
    elif month:
        query = query.filter(extract('month', Bill.due_date) == month)

    # Apply filtering by status (if provided)
    if status:
        query = query.filter(Bill.status == status)

    # Group by tower_number and bill_type
    query = query.group_by(Unit.tower_number, Bill.bill_type, Bill.status)

    response = {}
    for cost in query.all():
        tower_number = cost.tower_number
        bill_type = cost.bill_type.name
        status = cost.status.name
        tower_data = response.setdefault(tower_number, {})
        if bill_type not in tower_data:
            tower_data[bill_type] = {}
        tower_data[bill_type] = {
            'total_cost': cost.total_cost or 0,
            'average_cost': cost.average_cost or 0,
        }
    return jsonify(response)

@billing_performance_bp.route('/billing-years', methods=['GET'])
def get_available_years():
    # Query to get unique years from Bill.due_date
    years_query = db.session.query(
        extract('year', Bill.due_date).label('year')
    ).distinct().order_by(extract('year', Bill.due_date).desc())

    years = [str(year.year) for year in years_query.all()]
    return jsonify(years)

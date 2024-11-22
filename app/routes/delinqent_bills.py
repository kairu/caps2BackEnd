from flask import Blueprint, jsonify
from app.models.user import User

delinquentBills_bp = Blueprint('delinquentBills', __name__)

@delinquentBills_bp.route('/delinquent-bills', methods=['GET'])
def get_delinquent_bills():
    delinquents = []

    users = User.query.all()
    for user in users:
        for unit in user.unit:
            delinquent_bills = [bill for bill in unit.bills if bill.delinquent_amount and bill.delinquent_amount > 0]
            if delinquent_bills:
                delinquents.append({
                    'user_id': user.user_id,
                    'user_name': f"{user.last_name}, {user.first_name} ",
                    'Unit': f"Tower {unit.tower_number} {unit.floor_number} - {unit.unit_id}",
                    'delinquent_bills': [{
                        'bill_type': bill.bill_type.name,
                        'due_date': bill.due_date.isoformat(),
                        'amount': bill.total_amount,
                        'delinquent_amount': bill.delinquent_amount,
                        'total_amount': bill.total_amount + bill.delinquent_amount
                    } for bill in delinquent_bills]
                })
    return jsonify(delinquents)
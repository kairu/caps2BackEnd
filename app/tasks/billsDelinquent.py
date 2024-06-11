from ..models import Bill
from .common import db, datetime, scheduler

def generate_delinquency():
    current_date = datetime.now().date()
    with scheduler.app.app_context():
        if not Bill.query.all():
            return
        bills_list = Bill.query.all()
        for bill in bills_list:
            if bill.status == 1 and (bill.due_date < current_date):
                bill.delinquent_amount = (bill.total_amount * 0.03) * ((current_date - bill.due_date).days // 30)
                # print(f'Bill {bill.bill_id} has been delinquent for {bill.delinquent_amount} since {bill.due_date} of days {(current_date - bill.due_date).days // 30}')
        db.session.commit()
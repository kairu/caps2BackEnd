from ..models import Cms
from .common import datetime, db

def check_cms_archive():
    with db.app.app_context():
        if not Cms.query.all():
            return
        current_date = datetime.now().date()
        cms_list = Cms.query.all()
        for cms in cms_list:
            if cms.archive or cms.date_to_end is None:
                continue
            if cms.date_to_end < current_date:
                cms.archive = True
        db.session.commit()
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Offence, OffenderOffence, db
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    # Query for overview of traffic offences
    total_offences = OffenderOffence.query.count()
    total_penalties = db.session.query(func.sum(Offence.penalty)).join(OffenderOffence, Offence.id == OffenderOffence.offence_id).scalar()
    
    # Query for offence trends and penalties
    offence_trends = db.session.query(
        func.strftime('%Y-%m', OffenderOffence.date_committed).label('month'),
        func.count(OffenderOffence.id).label('count'),
        func.sum(Offence.penalty).label('total_penalty')
    ).join(Offence, Offence.id == OffenderOffence.offence_id).group_by('month').all()
    
    # Query for monthly/yearly offences statistics
    monthly_offences = db.session.query(
        func.strftime('%Y-%m', OffenderOffence.date_committed).label('month'),
        func.count(OffenderOffence.id).label('count')
    ).group_by('month').all()
    
    yearly_offences = db.session.query(
        func.strftime('%Y', OffenderOffence.date_committed).label('year'),
        func.count(OffenderOffence.id).label('count')
    ).group_by('year').all()
    
    return render_template('dashboard.html', user=current_user, total_offences=total_offences, total_penalties=total_penalties, offence_trends=offence_trends, monthly_offences=monthly_offences, yearly_offences=yearly_offences)
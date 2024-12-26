from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Offender, Offence, OffenderOffence, db

offender_offences = Blueprint('offender_offences', __name__)

@offender_offences.route('/offender_offences')
@login_required
def index():
    offender_offences = OffenderOffence.query.all()
    return render_template('offender_offences/index.html', offender_offences=offender_offences)


@offender_offences.route('/offender_offences/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        offender_id = request.form.get('offender_id')
        offence_id = request.form.get('offence_id')
        status = request.form.get('status')
        date_committed = request.form.get('date_committed')
        
        if not offender_id or not offence_id or not status or not date_committed:
            flash('All fields are required!', 'red')
            return redirect(url_for('offender_offences.create'))
        
        new_offender_offence = OffenderOffence(
            offender_id=offender_id,
            offence_id=offence_id,
            status=status,
            date_committed=date.fromisoformat(date_committed)
        )
        db.session.add(new_offender_offence)
        db.session.commit()
        
        flash('Violation created successfully!', 'green')
        return redirect(url_for('offender_offences.index'))
    
    offenders = Offender.query.all()
    offences = Offence.query.all()
    return render_template('offender_offences/new.html', offenders=offenders, offences=offences)


@offender_offences.route('/offender_offences/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    offender_offence = OffenderOffence.query.get_or_404(id)
    
    if request.method == 'POST':
        offender_offence.offender_id = request.form.get('offender_id')
        offender_offence.offence_id = request.form.get('offence_id')
        offender_offence.status = request.form.get('status')
        
        if not offender_offence.offender_id or not offender_offence.offence_id or not offender_offence.status:
            flash('All fields are required!', 'red')
            return redirect(url_for('offender_offences.edit', id=id))
        
        db.session.commit()
        
        flash('Violation relationship updated successfully!', 'green')
        return redirect(url_for('offender_offences.index'))
    
    offenders = Offender.query.all()
    offences = Offence.query.all()
    return render_template('offender_offences/edit.html', offender_offence=offender_offence, offenders=offenders, offences=offences)

@offender_offences.route('/offender_offences/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    offender_offence = OffenderOffence.query.get_or_404(id)
    db.session.delete(offender_offence)
    db.session.commit()
    
    flash('Violation relationship deleted successfully!', 'green')
    return redirect(url_for('offender_offences.index'))
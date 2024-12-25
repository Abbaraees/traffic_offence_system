from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Offender, OffenderOffence, Offence, db

offenders = Blueprint('offenders', __name__)

@offenders.route('/offenders')
@login_required
def index():
    offenders = Offender.query.all()
    return render_template('offenders/index.html', offenders=offenders)

@offenders.route('/offenders/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        license_number = request.form.get('license_number')
        plate_number = request.form.get('plate_number')
        contact_info = request.form.get('contact_info')
        
        if not name or not license_number or not plate_number or not contact_info:
            flash('All fields are required!', 'danger')
            return redirect(url_for('offenders.create'))
        
        new_offender = Offender(name=name, license_number=license_number, plate_number=plate_number, contact_info=contact_info)
        db.session.add(new_offender)
        db.session.commit()
        
        flash('Offender created successfully!', 'success')
        return redirect(url_for('offenders.index'))
    
    return render_template('offenders/new.html')

@offenders.route('/offenders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    offender = Offender.query.get_or_404(id)
    
    if request.method == 'POST':
        offender.name = request.form.get('name')
        offender.license_number = request.form.get('license_number')
        offender.plate_number = request.form.get('plate_number')
        offender.contact_info = request.form.get('contact_info')
        
        if not offender.name or not offender.license_number or not offender.plate_number or not offender.contact_info:
            flash('All fields are required!', 'danger')
            return redirect(url_for('offenders.edit', id=id))
        
        db.session.commit()
        
        flash('Offender updated successfully!', 'success')
        return redirect(url_for('offenders.index'))
    
    return render_template('offenders/edit.html', offender=offender)

@offenders.route('/offenders/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    offender = Offender.query.get_or_404(id)
    db.session.delete(offender)
    db.session.commit()
    
    flash('Offender deleted successfully!', 'success')
    return redirect(url_for('offenders.index'))
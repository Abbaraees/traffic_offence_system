from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Offence, db

offences = Blueprint('offences', __name__)

@offences.route('/offences')
@login_required
def index():
    offences = Offence.query.all()
    return render_template('offences/index.html', offences=offences)


@offences.route('/offences/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        offence_name = request.form.get('name')
        offence_description = request.form.get('description')
        offence_penalty = request.form.get('penalty')
        
        if not offence_name or not offence_description or not offence_penalty:
            flash('Name, description, and penalty are required!', 'danger')
            return redirect(url_for('offences.create'))
        
        new_offence = Offence(name=offence_name, description=offence_description, penalty=offence_penalty)
        db.session.add(new_offence)
        db.session.commit()
        
        flash('Offence created successfully!', 'success')
        return redirect(url_for('offences.index'))
    
    return render_template('offences/new.html')


@offences.route('/offences/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    offence = Offence.query.get_or_404(id)
    
    if request.method == 'POST':
        offence.name = request.form.get('name')
        offence.description = request.form.get('description')
        offence.penalty = request.form.get('penalty')
        
        if not offence.name or not offence.description or not offence.penalty:
            flash('Name, description, and penalty are required!', 'danger')
            return redirect(url_for('offences.edit', id=id))
        
        db.session.commit()
        
        flash('Offence updated successfully!', 'success')
        return redirect(url_for('offences.index'))
    
    return render_template('offences/edit.html', offence=offence)


@offences.route('/offences/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    offence = Offence.query.get_or_404(id)
    db.session.delete(offence)
    db.session.commit()
    
    flash('Offence deleted successfully!', 'success')
    return redirect(url_for('offences.index'))

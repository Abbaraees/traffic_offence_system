from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Payment, OffenderOffence, db

payments = Blueprint('payments', __name__)

@payments.route('/payments')
@login_required
def index():
    payments = Payment.query.all()
    return render_template('payments/index.html', payments=payments)

@payments.route('/payments/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        offender_offence_id = request.form.get('offender_offence_id')
        amount = request.form.get('amount')
        status = request.form.get('status')
        payment_date = request.form.get('payment_date')
        
        if not offender_offence_id or not amount or not status:
            flash('Offender-Offence, amount, and status are required!', 'red')
            return redirect(url_for('payments.create'))
        
        new_payment = Payment(
            offender_offence_id=offender_offence_id,
            amount=amount,
            status=status,
            payment_date=date.fromisoformat(payment_date) if payment_date else None
        )
        db.session.add(new_payment)
        db.session.commit()
        
        flash('Payment created successfully!', 'green')
        return redirect(url_for('payments.index'))
    
    offender_offences = OffenderOffence.query.all()
    return render_template('payments/new.html', offender_offences=offender_offences)

@payments.route('/payments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    payment = Payment.query.get_or_404(id)

    amount = request.form.get('amount')
    status = request.form.get('status')
    payment_date = request.form.get('payment_date')

    
    if request.method == 'POST':
        payment.offender_offence_id = request.form.get('offender_offence_id')
        payment.amount = amount
        payment.status = status
        payment.payment_date = date.fromisoformat(payment_date) if request.form.get('payment_date') else None
        
        if not payment.offender_offence_id or not payment.amount or not payment.status:
            flash('Offender-Offence, amount, and status are required!', 'red')
            return redirect(url_for('payments.edit', id=id))
        
        db.session.commit()
        
        flash('Payment updated successfully!', 'green')
        return redirect(url_for('payments.index'))
    
    offender_offences = OffenderOffence.query.all()
    return render_template('payments/edit.html', payment=payment, offender_offences=offender_offences)

@payments.route('/payments/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    
    flash('Payment deleted successfully!', 'green')
    return redirect(url_for('payments.index'))
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель для доходов и расходов
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'


# Создание базы данных
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense
    return render_template('index.html', transactions=transactions, total_income=total_income,
                           total_expense=total_expense, balance=balance)


@app.route('/add', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    category = request.form['category']
    trans_type = request.form['type']
    new_transaction = Transaction(amount=amount, category=category, type=trans_type)

    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

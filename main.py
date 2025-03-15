from flask import Flask, render_template, jsonify, request, redirect
from models import db, Transactions, app
from datetime import datetime

@app.route('/')
def index():
    transactions = Transactions.query.all()
    return render_template('home.html', transactions=transactions)



@app.route("/transactions", methods=['GET'])
def get_transaction(): 
    transactions = Transactions.query.all()
    json_transactions= list(map(lambda x: x.to_json(),transactions))
    return jsonify({"transactions": json_transactions})



@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    date = request.form['date']
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    description = request.form['description']
    category = request.form['category']
    amount = request.form['amount']

    if not date or not description or not category or not amount:
        return (jsonify({"message": "You must include a date, description, category and amount"}), 400)
    
    new_transaction = Transactions(date = date_object, description = description, category=category, amount=amount)
    print(new_transaction.to_json())

    try:
        db.session.add(new_transaction)
        db.session.commit()
    except Exception as e:
        return (jsonify({"message": str(e)}),400)
    
    print (jsonify({"message": "new transaction successfully logged!"}), 201)
    
    return redirect('/')



@app.route('/update_transaction/<int:id>', methods=['PATCH'])
def update_transaction(id):
    transaction = Transactions.query.get(id)

    if not transaction:
        return jsonify({"message": "transaction not found"}), 404
    
    data = request.json
    transaction.date = data.get("date", transaction.date )
    transaction.description = data.get("description", transaction.description)
    transaction.category = data.get("category", transaction.category)
    transaction.amount = data.get("amount", transaction.amount)
    db.session.commit()

    return jsonify({"message": "transaction updated."}), 200


@app.route("/delete_transaction/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    transaction = Transactions.query.get(id)

    if not transaction: 
        return jsonify({"message": "Transaction not found."}), 404
    
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted."}), 200




# main driver function
if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)

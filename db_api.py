# delete - DONE
# add user - DONE
# add expense - DONE
# get expenses for a user - sort by date (most recent) - DONE
# delete by transactionID - DONE
# update - optional

import datetime
from datetime import date as dt
import models
from app import DB

DB.create_all()
session = DB.session()


class DBQuery:
    user_id = ""
    email = ""
    first_name = ""
    last_name = ""
    

    # You HAVE to call the constructor before accessing any other functions
    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.add()

    def add(self):
        user = session.query(
            models.Users).filter_by(user_id=self.user_id).first()
        if user is None:
            to_add = models.Users(self.user_id, self.email, self.first_name,
                                  self.last_name)
            session.add(to_add)
            session.commit()

    def remove(self):
        user = session.query(models.Users).filter_by(user_id=self.user_id)
        user.delete()
        session.commit()

    def addTransaction(self, transaction_type, amount, date, location,
                       description):
        # transaction = session.query(models.Transaction).filter(
        #     models.Transaction.user_id == self.user_id,
        #     models.Transaction.transaction_id == transaction_id).first()
        if type(date) == str:
            date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        to_add = models.Transaction(self.user_id, transaction_type, amount,
                                    date, location, description)
        session.add(to_add)
        session.commit()
        
    def editTransaction(self, transaction_id, *args, **kwargs):
        '''
        Method to edit a transaction for a user.
        transaction_id is needed as to know which transaction to edit.
        Other variables are optional, but follow order:
            transaction_type, amount, date, location and description.
        Method allows setting specific things too, like:
            transaction_type=
            ...
        '''

        # dont do anything if nothing to edit
        if len(args) == len(kwargs) == 0:
            return

        args = list(args)  # since tuple does not have extend()
        to_edit = session.query(models.Transaction).filter(
            models.Transaction.transaction_id == transaction_id,
            models.Transaction.user_id == self.user_id).first()
        if to_edit is not None:

            # get pre-existing values for later
            transaction_info = [
                to_edit.transaction_type, to_edit.amount, to_edit.date,
                to_edit.location, to_edit.description
            ]
            # if not enough arguments are passed in, use the pre-existing values
            args.extend(transaction_info[len(args):])
            to_edit.transaction_type, to_edit.amount, to_edit.date, to_edit.location, to_edit.description = args

            # using dict.get(key, default) so that if the key DNE, it gets default value
            to_edit.transaction_type = kwargs.get("transaction_type",
                                                  to_edit.transaction_type)
            to_edit.amount = round(kwargs.get("amount", to_edit.amount), 2)
            to_edit.date = kwargs.get("date", to_edit.date)
            to_edit.location = kwargs.get("location", to_edit.location)
            to_edit.description = kwargs.get("description",
                                             to_edit.description)
            session.commit()    

    def removeTransaction(self, transaction_id):
        # match user id and transaction id to remove
        to_remove = session.query(models.Transaction).filter(
            models.Transaction.transaction_id == transaction_id,
            models.Transaction.user_id == self.user_id).first()
        if to_remove is not None:
            session.delete(to_remove)
            session.commit()

    def getTransactions(self):
        transactions = session.query(
            models.Users).filter_by(user_id=self.user_id).first().transactions
        transactions.sort(key=lambda x: x.date)
        transactions_list = []
        for transaction in transactions:
            transactions_list.append({
                "id": transaction.transaction_id,
                "type": transaction.transaction_type,
                "amount": transaction.amount,
                "date": transaction.date,
                "location": transaction.location,
                "description": transaction.description
            })
        return transactions_list
        
    def getUserInfo(self):
        transactions = session.query(
            models.Users).filter_by(user_id=self.user_id).first().transactions

        full_name = self.first_name + ' ' + self.last_name
        total_balance = 0
        total_income = 0
        total_expense = 0

        for transaction in transactions:
            if transaction.transaction_type == 'Income':
                total_balance += transaction.amount
                total_income += transaction.amount
            else:
                total_balance -= transaction.amount
                total_expense += transaction.amount

        return {"User": full_name,
                "Balance": round(total_balance, 2),
                "Income": round(total_income, 2),
                "Expense": round(total_expense, 2)}

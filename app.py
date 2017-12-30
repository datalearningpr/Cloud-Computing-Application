
import random
import os
import pandas as pd
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# this is the ORM for the marksix table
class Result(db.Model):
    __tablename__ = 'marksixresult'

    drawnumber = db.Column(db.String(), primary_key=True)
    drawdate = db.Column(db.Date())
    drawname = db.Column(db.String())

    number1 = db.Column(db.Integer())
    number2 = db.Column(db.Integer())   
    number3 = db.Column(db.Integer())
    number4 = db.Column(db.Integer())
    number5 = db.Column(db.Integer())
    number6 = db.Column(db.Integer())
    numberspecial = db.Column(db.Integer())


    def __init__(self, input_dict):
        self.drawnumber = input_dict["DrawNumber"]
        self.drawdate = input_dict["DrawDate"]
        self.drawname = input_dict["DrawName"]
        self.number1 = input_dict["Number1"]
        self.number2 = input_dict["Number2"]
        self.number3 = input_dict["Number3"]
        self.number4 = input_dict["Number4"]
        self.number5 = input_dict["Number5"]
        self.number6 = input_dict["Number6"]
        self.numberspecial = input_dict["NumberSpecial"]

    def __repr__(self):
        return '<drawnumber {}>'.format(self.drawnumber)


db.create_all()
import Marksix_UpdateDB, Marksix_PickNumber

# this is the home page
# it will process the forecast number
# it will also show how updated the database is 
@app.route('/')
def index():
    
    ResultTable=pd.read_sql("SELECT * FROM MarkSixResult ORDER BY DrawDate DESC", db.session.bind, parse_dates=["drawdate"])
    numbers = Marksix_PickNumber.GenerateForecastedNumbers(ResultTable)


    # forecast will only have 6 numbers, we need 8 numbers
    # the rest 2 we just randomly pick
    to_picked = set(range(1, 50)) - set(numbers)
    another_two = []
    another_two += random.sample(to_picked, 1)
    to_picked -= set(another_two)
    another_two += random.sample(to_picked, 1)
    numbers = sorted(list(numbers.values()) + another_two)

    # output of 8 nubmers as string
    msg = ''
    for i in range(1,len(numbers)+1):
        msg=msg + str(numbers[i-1])
        if i!=len(numbers):
            msg=msg+', '

    # get the lates date from database
    max_date = db.session.query(db.func.max(Result.drawdate)).scalar()

    return render_template(
        'index.html',
        msg = msg,
        max_date = max_date)
    

# call the update module
@app.route('/update', methods=['GET'])
def update():
    latest_date = Marksix_UpdateDB.updateDB()
    return "Latest draw date is: " + latest_date
    


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

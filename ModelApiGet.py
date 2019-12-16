import os
import dill as pickle
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import json
import requests

from flask import Flask, render_template, flash
from config import Config
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route('/')
@app.route('/loan')
def loan():
    return render_template('Model.html')
@app.route('/LoanPredictResult/<result>',methods=['POST'])
@app.route('/LoanPredictResult',methods=['POST'])
def predict_loan():
        """Setting the headers to send and accept json responses
        """
        if request.method == 'POST':
            result = request.form
        dictresult = result.to_dict(flat=False)
        header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}
        print(dictresult)
        """Reading test batch
        """
        df=pd.DataFrame.from_dict(dictresult)
        #df = pd.DataFrame(dictresult.items(), columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', \
         #           'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'])
        print(df)


        """Converting Pandas Dataframe to json
        """
        data = df.to_json(orient='records')

        resp = requests.post("http://127.0.0.1:5000/predict", \
                             data=json.dumps(data), \
                             headers=header)

        print(resp.status_code)

        print(resp.json())
        print(resp)
        temp = resp.json()['predictions']
        temp = '{"Predictions":'+temp+'}'
        result_dict = json.loads(temp)

        return render_template('loanResult.html',data = result_dict)


if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5001,debug=True)
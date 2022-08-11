
import sklearn
import pickle
import pandas as pd
import time 
from flask_cors import cross_origin
from flask import Flask, request, render_template
pred2 = 0
app = Flask(__name__)

mdl = pickle.load(open("fare_predict.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("flight.html")

@app.route("/price_calc", methods=["GET", "POST"])
@cross_origin()


def price_calc():
    if request.method == "POST":

        dep_date = request.form["Dep_Time"]
        dep_day = int(pd.to_datetime(dep_date, format="%Y-%m-%dT%H:%M").day)
        dep_month = int(pd.to_datetime(dep_date, format="%Y-%m-%dT%H:%M").month)
        dep_hour = int(pd.to_datetime(dep_date, format="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(dep_date, format="%Y-%m-%dT%H:%M").minute)

        arr_date = request.form["Arrival_Time"]
        arr_hour = int(pd.to_datetime(arr_date, format="%Y-%m-%dT%H:%M").hour)
        arr_min = int(pd.to_datetime(arr_date, format="%Y-%m-%dT%H:%M").minute) 


        jour_hour = abs(arr_hour - dep_hour)
        jour_min = abs(arr_min - dep_min)


        t_stops = int(request.form["stops"])

        airline = request.form['airline']
        Jet_Airways = airline[0]
        IndiGo = airline[1]
        Air_India = airline[2]
        Multiple_carriers = airline[3]
        SpiceJet = airline[4]
        Vistara = airline[5]
        GoAir = airline[6]
        Multiple_carriers_Premium_economy = airline[7]
        Jet_Airways_Business = airline[8]
        Vistara_Premium_economy = airline[9]
        Trujet = airline[10]

        Source = request.form["Source"]
        s_Delhi = Source[0]
        s_Kolkata = Source[1]
        s_Mumbai = Source[2]
        s_Chennai = Source[3]
        
        destination = request.form["Destination"]
        d_Cochin = destination[0]
        d_Delhi = destination[1]
        d_New_Delhi = destination[2]
        d_Hyderabad = destination[3]
        d_Kolkata = destination[4]

        pred = mdl.predict([[
            t_stops,
            dep_day,
            dep_month,
            dep_hour,
            dep_min,
            arr_hour,
            arr_min,
            jour_hour,
            jour_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        pred2 = round(pred[0])
        print("pred - " ,pred2)
        return render_template('flight.html', price = "pipeline" )
    return render_template("flight.html")    


if __name__ == "__main__":
    app.run(debug=True)






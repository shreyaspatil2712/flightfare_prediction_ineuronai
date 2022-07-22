from flask import Flask, render_template, request
import sklearn
import pickle
import pandas as pd

file = open(r"fare_predict.pkl", "rb")
model = pickle.load(file)

app = Flask(__name__)


@app.route("/")
def welcome():
        return render_template("welcome.html")

@app.route("/predictor", methods = ["GET", "POST"])
def predict():
    
    if request.method == "POST":
        
        # Departure Date
        dep_t = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(dep_t, format = "%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(dep_t, format = "%Y-%m-%dT%H:%M").month)
        
        # Departure Time
        Dep_hour = int(pd.to_datetime(dep_t, format = "%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(dep_t, format = "%Y-%m-%dT%H:%M").minute)
        
        # Arrival Date
        arr_t = request.form["Arr_Time"]
        Arrival_hour = int(pd.to_datetime(arr_t, format = "%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(arr_t, format = "%Y-%m-%dT%H:%M").minute)
        
        # Duration
        Duration_min = abs(Arrival_hour - Dep_hour)*60 + abs(Arrival_min - Dep_min)
        
        # Total stops
        Total_stops = int(request.form["Total_stops"])
        
        # Airline
        airline = request.form["Airline"]
        
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        Go_Air = 0 
        Multiple_carriers_Premium_economy = 0
        Vistara_Premium_economy = 0
        Jet_Airways_Business = 0
        Trujet = 0
        
        if airline == "Jet Airways":
            Jet_Airways = 1
            
        elif airline == "IndiGo":
            IndiGo = 1
           
        elif airline == "Air India":
            Air_India = 1
            
        elif airline == "Multiple carriers":
            Multiple_carriers = 1
            
        elif airline == "SpiceJet":
            SpiceJet = 1
            
        elif airline == "Vistara":
            Vistara = 1
            
        elif airline == "GoAir":
            Go_Air = 1
            
        elif airline == "Multiple carriers Premium Economy": 
            Multiple_carriers_Premium_economy = 1
            
        elif airline == "Vistara Premium economy":
            Vistara_Premium_economy = 1
            
        elif airline == "Jet Airways Business":
            Jet_Airways_Business = 1
             
        elif airline == "Trujet":
            Trujet = 1
            
        
        # Source
        source = request.form["Source"]
        
        s_Delhi = 0
        s_Kolkata = 0
        s_Mumbai = 0
        s_Chennai = 0
        
        if source == "Delhi":
            s_Delhi = 1
            
        elif source == "Kolkata":
            s_Kolkata = 1
            
        elif source == "Mumbai":
            s_Mumbai = 1
        
        elif source == "Chennai":
            s_Chennai = 1
            
        
        # Destination
        destination = request.form["Destination"]
        
        d_Cochin = 0
        d_Delhi = 0
        d_New_Delhi = 0
        d_Hyderabad = 0
        d_Kolkata = 0
        
        if destination == "Cochin":
            d_Cochin = 1
            
        elif destination == "Delhi":
            d_Delhi = 1
            
        if destination == "New Delhi":
            d_New_Delhi = 1
            
        if destination == "Hyderabad":
            d_Hyderabad = 1
            
        if destination == "Kolkata":
            d_Kolkata = 1
            
            
        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Arrival_hour,
            Arrival_min,
            Dep_hour,
            Dep_min,
            Duration_min,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi,
            Air_India,
            Go_Air,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy
        ]])
        
        output = round(prediction[0], 2)
        print(output)
        
        return render_template("predictor.html", 
                               prediction_text = "Your Flight Fare from {} to {} is Rs. {}".format(source, destination, output))
                   
        
    return render_template("predictor.html")


@app.route("/about")
def about():
    return render_template("aboutus.html")

if __name__ == "__main__":
    app.run(debug = True)
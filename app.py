from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pandas as pd

app = Flask(__name__)
model = pd.read_pickle("flight_rf.pkl")


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Date"] +" "+ request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Date"] +" "+ request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline=request.form['airline']
        airlines = {
            'Jet Airways': 0,
            'IndiGo': 0,
            'Air India': 0,
            'Multiple carriers': 0,
            'Vistara': 0,
            'GoAir': 0,
            'Multiple carriers Premium economy': 0,
            'Jet Airways Business': 0,
            'Vistara Premium economy': 0,
            'Trujet': 0
        }

        if({airline} <= airlines.keys()):
            airlines[airline] = 1

        # Source
        Source = request.form["Destination"]
        sources = {
            'Cochin': 0,
            'Delhi': 0,
            'New_Delhi': 0,
            'Hyderabad': 0,
            'Kolkata': 0
        }

        if({Source} <= sources.keys()):
            sources[Source] = 1

        print(sources,airlines)
        
        prediction=model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            airlines.get('Air India',0),
            airlines.get('GoAir',0),
            airlines.get('IndiGo',0),
            airlines.get('Jet Airways',0),
            airlines.get('Jet Airways Business',0),
            airlines.get('Multiple carriers',0),
            airlines.get('Multiple carriers Premium economy',0),
            airlines.get('SpiceJet',0),
            airlines.get('Trujet',0),
            airlines.get('Vistara',0),
            airlines.get('Vistara Premium economy',0),
            sources.get('Chennai',0),
            sources.get('Delhi',0),
            sources.get('Kolkata',0),
            sources.get('Mumbai',0),
            sources.get('Cochin',0),
            sources.get('Delhi',0),
            sources.get('Hyderabad',0),
            sources.get('Kolkata',0),
            sources.get('New_Delhi',0)
        ]])

        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)

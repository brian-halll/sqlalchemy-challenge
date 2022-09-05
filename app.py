from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

Base.prepare(engine, reflect = True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app  = Flask(__name__)




# home route 
@app.route("/")
def home():
    return(
        f"<center><h2> Welcome to the Hawaii Climate Analysis Local API...</h2></center>"
        f"<center><h3> Select from the available routes: </h3></center>"
        f"<center> /api/v1.0/precipitation </center>"
        f"<center> /api/v1.0/stations </center>"
        f"<center> /api/v1.0/tobs </center>"
        f"<center> /api/v1.0/<start> </center>"
        f"<center> /api/v1.0/<start>/<end> </center>"

    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Calculate the date one year from the last date in data set.
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()

    session.close()

    #  create dictionary
    precipitation = {date: prcp for date, prcp in results }


    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.name).all()

    session.close()

    station_names = list(np.ravel(stations))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= previous_year).all()

    temperatureList = list(np.ravel(results))
    
    session.close()

    

    return jsonify(temperatureList)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start = None, end = None):

    #selection statement

    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs) ]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        temp_list = list(np.ravel(results))

        session.close()

        return jsonify(temp_list)

    else: 
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date <= endDate).all()

        
        temp_list = list(np.ravel(results))

        session.close()

        return jsonify(temp_list)



# app laucher 
if __name__ == '__main__':
    app.run(debug = True)




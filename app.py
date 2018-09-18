import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# 1. Import Flask
from flask import Flask

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/<start><br />"
        f"/api/v1.0/<start><end><br />"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation observations from the lat year"""
    prcp_dict = {}

    prcps = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
        
    for prcp in prcps:
    	if prcp[0] not in prcp_dict:
    		prcp_dict[prcp[0]] = [prcp[1]]
    	else:
    		prcp_dict[prcp[0]].append(prcp[1])
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    tobs_dict = {}

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()
    stations = session.query(Measurement.station).group_by('station').all()
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature for the last year"""
    tobs_dict = {}

    results = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).all()

    last_year_tobs = list(np.ravel(results))
    return jsonify(last_year_tobs)

@app.route("/api/v1.0/<start>")
def calc_temps_without_end(start, end='2017-08-23'):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    calc_temps = list(np.ravel(results))
    return jsonify(calc_temps)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_with_end(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    calc_temps = list(np.ravel(results))
    return jsonify(calc_temps)

if __name__ == '__main__':
    app.run(debug=True)


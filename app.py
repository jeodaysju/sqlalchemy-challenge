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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/<start>")
def stats_start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
    func.max(Measurement.tobs), 
    func.avg(Measurement.tobs),]
    calculations = session.query(*sel).\
        filter(Measurement.date >= start).all()
    calculations

    session.close()

    # Convert list of tuples into normal list
    all_start = list(np.ravel(calculations))

    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def stats_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
    func.max(Measurement.tobs), 
    func.avg(Measurement.tobs),]
    calculations1 = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    calculations1

    session.close()

    # Convert list of tuples into normal list
    all_start_end = list(np.ravel(calculations1))

    return jsonify(all_start_end)

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    query_dt = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_dt).order_by(Measurement.date).all()

    session.close()

    all_precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        # precip_dict["prcp"] = prcp
        all_precip_data.append(precip_dict)

    return jsonify(all_precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    max_dt = session.query(Measurement.date).filter_by(station = "USC00519281").\
    order_by(Measurement.date.desc()).first()

    # Calculate the date 1 year ago from the last data point in the database
    query_dt = dt.date(2017, 8, 18) - dt.timedelta(days=365)
        
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_dt).filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)

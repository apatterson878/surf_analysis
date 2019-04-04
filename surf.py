import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start_date&gt;<br/>"
        f"/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    "Return the JSON representation of your dictionary."
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    prcp_dict = {}
    for row in results:
        prcp_dict[row[0]] = row[1]

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.station).distinct().all()
    all_stations = list(np.ravel(station))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():
    query = session.query(func.max(Measurement.date))
    max_date = query.first()[0]
    max_date = dt.datetime.strptime(max_date, '%Y-%m-%d').date()
    min_date = dt.date(max_date.year -1 , max_date.month, max_date.day)
   
    temp_query = session.query(Measurement.tobs)\
        .filter(Measurement.date.between(min_date, max_date)).all()
    temp = list(np.ravel(temp_query))
    return jsonify(temp)
    
@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
    
    start =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    date_start = list(np.ravel(start))
    return jsonify(date_start)

@app.route("/api/v1.0/<start_date>/<end_date>")
def days(start_date, end_date):
 
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    date_start = list(np.ravel(start_end))
    return jsonify(date_start)

if __name__ == '__main__':
    app.run(debug=True)
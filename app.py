# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

from flask import Flask, jsonify 


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table 1:38:58 zoom day 3
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return "Welcome :)"


@app.route("/api/precipitation")
def precipitation():
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date_time = datetime.strptime(recent_date, "%Y-%m-%d")
    one_year_ago = recent_date_time - timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago.strftime("%Y-%m-%d")).all()
    precipitation_data = {date: prcp for date, prcp in results}    
    return jsonify(precipitation_data)

@app.route("/api/stations")
def stations():
    stations = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    stations_data = [
        {
            "station": station, 
            "name": name,
            "latitude": latitude, 
            "longitude": longitude,
            "elevation": elevation
        } 
        for station, name, latitude, longitude, elevation in stations]    
    return jsonify(stations_data)

@app.route("/api/tobs")
def tobs():
    act_unq_station = 'USC00519281'
    rec_date_stat = session.query(func.max(measurement.date)).filter(measurement.station == act_unq_station).scalar()
    rec_date_time_stat = datetime.strptime(rec_date_stat, "%Y-%m-%d")    
    one_year_ago = rec_date_time_stat - timedelta(days=365)
    temp_data = session.query(measurement.date,measurement.tobs)\
                          .filter(measurement.station == act_unq_station)\
                          .filter(measurement.date >= one_year_ago.strftime("%Y-%m-%d"))\
                          .all()
    tobs_data = {date: tobs for date, tobs in temp_data}    
    return jsonify(tobs_data)

@app.route("/api/start/<start_date>")
def start(start_date): 
    start_date_time = datetime.strptime(start_date, "%Y-%m-%d")
    temp_stat = session.query(func.min(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.avg(measurement.tobs))\
                     .filter(measurement.date >= start_date_time)\
                     .all()
    
    if temp_stat:
        min_temp, max_temp, avg_temp = temp_stat[0]
        return jsonify({
            "start_date": start_date,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        })
    else:
        return jsonify({"error":"no data found for this start date"}), 404

@app.route("/api/start/<start_date>/end/<end_date>")
def start_end(start_date, end_date):
    start_date_time = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_time = datetime.strptime(end_date, "%Y-%m-%d")
    temp_stat = session.query(func.min(measurement.tobs), 
                            func.max(measurement.tobs), 
                            func.avg(measurement.tobs))\
                     .filter(measurement.date >= start_date_time)\
                     .filter(measurement.date <= end_date_time)\
                     .all()
    if temp_stat:
        min_temp, max_temp, avg_temp = temp_stat[0]
        return jsonify({
            "start_date": start_date,
            "end_date": end_date,
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        })
    else:
        return jsonify({"error":"no data found for this date range"}), 404

if __name__ == '__main__':
    app.run(debug=True)

session.close()
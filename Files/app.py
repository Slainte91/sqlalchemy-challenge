import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    results = session.query(measurement.date, measurement.prcp).all()

    session.close()


    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
       
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station = Base.classes.station
    results = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()

    session.close()


    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_active = session.query(measurement.date, measurement.tobs).\
                   filter(measurement.station == 'USC00519281').all()
    tobs_rows = [{"Date": result[0], "tobs": result[1]} for result in most_active]

    session.close()

    return jsonify(tobs_rows)


@app.route("/api/v1.0/<start>")
def startDateOnly(start):
    session = Session(engine)
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    single_rows = [{"Min": result[0], "Average": result[1], "Max": result[2]} for result in results]
    session.close()

    return jsonify(single_rows)



@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    multi_rows = [{"Min": result[0], "Average": result[1], "Max": result[2]} for result in results]
    session.close()

    return jsonify(multi_rows)

if __name__ == '__main__':
    app.run(debug=True)

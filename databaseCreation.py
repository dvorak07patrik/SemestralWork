from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, ForeignKey, Date, Time, Float, VARCHAR, BigInteger
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Database connection parameters
db_username = 'airflow'
db_password = 'airflow'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

# Create a database engine
engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

# Base class for declarative models
Base = declarative_base()

# Define dimension tables
class DimDrivers(Base):
    __tablename__ = 'dim_drivers'
    driverId = Column(Integer, primary_key=True)
    driverRef = Column(String(30))
    number = Column(SmallInteger)
    code = Column(String(3))
    forename = Column(String(50))
    surname = Column(String(50))
    dob = Column(Date)
    nationality = Column(String(50))
    url = Column(String(255))

class DimConstructors(Base):
    __tablename__ = 'dim_constructors'
    constructorId = Column(Integer, primary_key=True)
    constructorRef = Column(String(30))
    name = Column(String(100))
    nationality = Column(String(50))
    url = Column(String(255))

class DimRaces(Base):
    __tablename__ = 'dim_races'
    raceId = Column(Integer, primary_key=True)
    season = Column(Integer)
    round = Column(SmallInteger)
    circuitId = Column(Integer, ForeignKey('dim_circuits.circuitId'))
    name = Column(String(150))
    date = Column(Date)
    time = Column(Time)
    url = Column(String(255))
    circuit = relationship("DimCircuits")

class DimCircuits(Base):
    __tablename__ = 'dim_circuits'
    circuitId = Column(Integer, primary_key=True)
    circuitRef = Column(String(30))
    name = Column(String(100))
    location = Column(String(50))
    country = Column(String(30))
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer)
    url = Column(String(255))

# Define fact tables
class FactResults(Base):
    __tablename__ = 'fact_results'
    resultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    driverId = Column(Integer, ForeignKey('dim_drivers.driverId'))
    constructorId = Column(Integer, ForeignKey('dim_constructors.constructorId'))
    number = Column(SmallInteger)
    grid = Column(SmallInteger)
    position = Column(SmallInteger)
    positionText = Column(VARCHAR(3))
    positionOrder = Column(SmallInteger)
    points = Column(SmallInteger)
    timeOrRetired = Column(VARCHAR(50))

class FactDriverStandings(Base):
    __tablename__ = 'fact_driver_standings'
    driverStandingsId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    driverId = Column(Integer, ForeignKey('dim_drivers.driverId'))
    points = Column(Integer, default=0)
    position = Column(SmallInteger)
    positionText = Column(VARCHAR(3))
    wins = Column(SmallInteger, default=0)

class FactConstructorStandings(Base):
    __tablename__ = 'fact_constructor_standings'
    constructorStandingsId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    constructorId = Column(Integer, ForeignKey('dim_constructors.constructorId'))
    points = Column(SmallInteger)
    position = Column(SmallInteger)
    positionText = Column(VARCHAR(2))
    wins = Column(Integer)

class FactLapTimes(Base):
    __tablename__ = 'fact_lap_times'
    lapTimeId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    driverId = Column(Integer, ForeignKey('dim_drivers.driverId'))
    lap = Column(SmallInteger)
    position = Column(SmallInteger)
    time = Column(VARCHAR(50))
    milliseconds = Column(Integer)

class FactSafetyCars(Base):
    __tablename__ = 'fact_safety_cars'
    safetyCarId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    cause = Column(VARCHAR(255))
    deployed = Column(SmallInteger)
    retreated = Column(SmallInteger)
    fullLaps = Column(SmallInteger)
    type = Column(VARCHAR(1))

class FactRedFlags(Base):
    __tablename__ = 'fact_red_flags'
    redFlagId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    lap = Column(SmallInteger)
    resumed = Column(String(50))
    incident = Column(String(255))
    excluded = Column(String(255))

class FactQualifying(Base):
    __tablename__ = 'fact_qualifying'
    qualifyId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    driverId = Column(Integer, ForeignKey('dim_drivers.driverId'))
    constructorId = Column(Integer, ForeignKey('dim_constructors.constructorId'))
    number = Column(SmallInteger)
    position = Column(SmallInteger)
    q1 = Column(VARCHAR(50))
    q2 = Column(VARCHAR(50))
    q3 = Column(VARCHAR(50))

class FactPitStops(Base):
    __tablename__ = 'fact_pit_stops'
    pitStopId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('dim_races.raceId'))
    driverId = Column(Integer, ForeignKey('dim_drivers.driverId'))
    stops = Column(SmallInteger)
    lap = Column(SmallInteger)
    time = Column(VARCHAR(50))
    duration = Column(Float)
    milliseconds = Column(BigInteger)

# Create all tables in the database
Base.metadata.create_all(engine)

print("Database tables created successfully.")

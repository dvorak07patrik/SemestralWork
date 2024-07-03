-- Fact Table: Results
CREATE TABLE fact_results (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number SMALLINT,
    grid SMALLINT,
    position SMALLINT,
    positionText VARCHAR(3),
    positionOrder SMALLINT,
    points SMALLINT,
    timeOrRetired VARCHAR(50),
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (driverId) REFERENCES dim_drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES dim_constructors(constructorId)
);

-- Fact Table: Driver Standings
CREATE TABLE fact_driver_standings (
    driverStandingsId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    points INT DEFAULT 0,
    position SMALLINT,
    positionText VARCHAR(3),
    wins SMALLINT DEFAULT 0,
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (driverId) REFERENCES dim_drivers(driverId)
);

-- Fact Table: Constructor Standings
CREATE TABLE fact_constructor_standings (
    constructorStandingsId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points SMALLINT,
    position SMALLINT,
    positionText VARCHAR(2),
    wins INT,
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (constructorId) REFERENCES dim_constructors(constructorId)
);

-- Fact Table: Lap Times
CREATE TABLE fact_lap_times (
    lapTimeId SERIAL PRIMARY KEY,
    raceId INT,
    driverId INT,
    lap SMALLINT,
    position SMALLINT,
    time VARCHAR(50),
    milliseconds INT,
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (driverId) REFERENCES dim_drivers(driverId),
);

-- Fact Table: Safety Cars
CREATE TABLE fact_safety_cars (
    safetyCarId SERIAL PRIMARY KEY,
    raceId INT,
    cause VARCHAR(255),
    deployed SMALLINT,
    retreated SMALLINT,
    fullLaps SMALLINT,
    type VARCHAR(1),
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (timeId) REFERENCES dim_time(timeId)
);

-- Fact Table: Red Flags
CREATE TABLE fact_red_flags (
    redFlagId SERIAL PRIMARY KEY,
    raceId INT,
    lap SMALLINT,
    resumed CHAR(50),
    incident VARCHAR(255),
    excluded VARCHAR(255)
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (timeId) REFERENCES dim_time(timeId)
);

-- Fact Table: Qualifying
CREATE TABLE fact_qualifying (
    qualifyId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    number SMALLINT,
    position SMALLINT,
    q1 VARCHAR(50),
    q2 VARCHAR(50),
    q3 VARCHAR(50),
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (driverId) REFERENCES dim_drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES dim_constructors(constructorId)
);

-- Fact Table: Pit Stops
CREATE TABLE fact_pit_stops (
    pitStopId SERIAL PRIMARY KEY,
    raceId INT,
    driverId INT,
    stops SMALLINT,
    lap SMALLINT,
    time VARCHAR(50),
    duration FLOAT,
    milliseconds BIGINT,
    FOREIGN KEY (raceId) REFERENCES dim_races(raceId),
    FOREIGN KEY (driverId) REFERENCES dim_drivers(driverId)
);

-- Dimension Table: Drivers
CREATE TABLE dim_drivers (
    driverId INT PRIMARY KEY,
    driverRef VARCHAR(30),
    number SMALLINT,
    code VARCHAR(3),
    forename VARCHAR(50),
    surname VARCHAR(50),
    dob DATE,
    nationality VARCHAR(50),
    url VARCHAR(255)
);

-- Dimension Table: Constructors
CREATE TABLE dim_constructors (
    constructorId INT PRIMARY KEY,
    constructorRef VARCHAR(30),
    name VARCHAR(100),
    nationality VARCHAR(50),
    url VARCHAR(255)
);

-- Dimension Table: Races
CREATE TABLE dim_races (
    raceId INT PRIMARY KEY,
    season INT,
    round SMALLINT,
    circuitId INT,
    name VARCHAR(150),
    date DATE,
    time TIME,
    url VARCHAR(255),
    FOREIGN KEY (circuitId) REFERENCES dim_circuits(circuitId)
);

-- Dimension Table: Circuits
CREATE TABLE dim_circuits (
    circuitId INT PRIMARY KEY,
    circuitRef VARCHAR(30),
    name VARCHAR(100),
    location VARCHAR(50),
    country VARCHAR(30),
    lat FLOAT,
    lng FLOAT,
    alt INT,
    url VARCHAR(255)
);


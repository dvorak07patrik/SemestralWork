-- Creating table for driver standings
CREATE TABLE "driver_standings"(
    "driverStandingsId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "points" INT NOT NULL DEFAULT 0,
    "position" SMALLINT NOT NULL,
    "positionText" VARCHAR(3) NOT NULL,
    "wins" SMALLINT NOT NULL DEFAULT 0
);

-- Creating table for race results
CREATE TABLE "results"(
    "resultId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "constructorId" INT NOT NULL,
    "number" SMALLINT NOT NULL,
    "grid" SMALLINT NULL,
    "position" SMALLINT NULL,
    "positionText" VARCHAR(3) NULL,
    "positionOrder" SMALLINT NULL,
    "points" SMALLINT NULL,
    "timeOrRetired" VARCHAR(50) NOT NULL
);

CREATE TABLE "pit_stops"(
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "stops" SMALLINT NULL,
    "lap" SMALLINT NOT NULL,
    "time" VARCHAR(50) NULL,
    "duration" FLOAT NULL,
    "milliseconds" BIGINT NULL
);

CREATE TABLE "sprint_results"(
    "resultId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "constructorId" INT NOT NULL,
    "number" SMALLINT NOT NULL,
    "grid" SMALLINT NULL,
    "position" SMALLINT NULL,
    "positionText" VARCHAR(3) NULL,
    "positionOrder" SMALLINT NULL,
    "points" SMALLINT NULL,
    "timeOrRetired" VARCHAR(50) NOT NULL
);

CREATE TABLE "races"(
    "raceId" INT PRIMARY KEY,
    "year" INT NOT NULL,
    "round" SMALLINT NOT NULL,
    "circuitId" INT NOT NULL,
    "name" VARCHAR(150) NOT NULL,
    "date" DATE NOT NULL,
    "time" TIME NOT NULL,
    "url" VARCHAR(255) NULL,
    "fp1_date" DATE NULL,
    "fp1_time" TIME NULL
);

CREATE TABLE "constructors"(
    "constructorId" INT PRIMARY KEY,
    "constructorRef" VARCHAR(30) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "nationality" VARCHAR(50) NULL,
    "url" VARCHAR(255) NULL
);

CREATE TABLE "safety_cars"(
    "raceId" INT NOT NULL,
    "cause" VARCHAR(255) NULL,
    "deployed" SMALLINT NOT NULL,
    "retreated" SMALLINT NULL,
    "fullLaps" SMALLINT NULL,
    "type" VARCHAR(1) NOT NULL
);

CREATE TABLE "circuits"(
    "circuitId" INT PRIMARY KEY,
    "circuitRef" VARCHAR(30) NULL,
    "name" VARCHAR(100) NOT NULL,
    "location" VARCHAR(50) NOT NULL,
    "country" VARCHAR(30) NOT NULL,
    "lat" FLOAT NULL,
    "lng" FLOAT NULL,
    "alt" INT NULL,
    "url" VARCHAR(255) NULL
);

CREATE TABLE "lap_times"(
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "lap" SMALLINT NOT NULL,
    "position" SMALLINT NULL,
    "time" VARCHAR(50) NULL,
    "miliseconds" INT NULL
);

CREATE TABLE "seasons"(
    "year" INT NOT NULL,
    "url" VARCHAR(255) NULL
);

CREATE TABLE "qualifying"(
    "qualifyId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "driverId" INT NOT NULL,
    "constructorId" INT NOT NULL,
    "number" SMALLINT NULL,
    "position" SMALLINT NOT NULL,
    "q1" VARCHAR(50) NULL,
    "q2" VARCHAR(50) NULL,
    "q3" VARCHAR(50) NULL
);

CREATE TABLE "constructor_results"."csv"(
    "constructorsResultsId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "constructorId" INT NOT NULL,
    "points" INT NOT NULL,
    "status" VARCHAR(100) NULL
);

CREATE TABLE "constructor_standings"(
    "constructorStandingsId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "constructorId" INT NOT NULL,
    "points" SMALLINT NOT NULL,
    "position" SMALLINT NOT NULL,
    "positionText" VARCHAR(2) NOT NULL,
    "wins" INT NULL
);

CREATE TABLE "drivers"(
    "driverId" INT PRIMARY KEY,
    "driverRef" VARCHAR(30) NOT NULL,
    "number" SMALLINT NULL,
    "code" VARCHAR(3) NULL,
    "forename" VARCHAR(50) NOT NULL,
    "surname" VARCHAR(50) NOT NULL,
    "dob" DATE NULL,
    "nationality" VARCHAR(50) NULL,
    "url" VARCHAR(255) NULL
);

CREATE TABLE "red_flags"(
    "redFlagId" INT PRIMARY KEY,
    "raceId" INT NOT NULL,
    "lap" SMALLINT NOT NULL,
    "resumed" CHAR(50) NOT NULL,
    "incident" VARCHAR(255) NULL,
    "excluded" VARCHAR(255) NULL
);

ALTER TABLE
    "red_flags" ADD CONSTRAINT "red_flags_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "constructor_results"."csv" ADD CONSTRAINT "constructor_results_csv_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "sprint_results" ADD CONSTRAINT "sprint_results_driverid_foreign" FOREIGN KEY("driverId") REFERENCES "drivers"("driverId");
ALTER TABLE
    "lap_times" ADD CONSTRAINT "lap_times_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "constructor_results"."csv" ADD CONSTRAINT "constructor_results_csv_constructorid_foreign" FOREIGN KEY("constructorId") REFERENCES "constructors"("constructorId");
ALTER TABLE
    "results" ADD CONSTRAINT "results_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "pit_stops" ADD CONSTRAINT "pit_stops_driverid_foreign" FOREIGN KEY("driverId") REFERENCES "drivers"("driverId");
ALTER TABLE
    "constructor_standings" ADD CONSTRAINT "constructor_standings_constructorid_foreign" FOREIGN KEY("constructorId") REFERENCES "constructors"("constructorId");
ALTER TABLE
    "safety_cars" ADD CONSTRAINT "safety_cars_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "driver_standings" ADD CONSTRAINT "driver_standings_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "driver_standings" ADD CONSTRAINT "driver_standings_driverid_foreign" FOREIGN KEY("driverId") REFERENCES "drivers"("driverId");
ALTER TABLE
    "seasons" ADD CONSTRAINT "seasons_year_foreign" FOREIGN KEY("year") REFERENCES "races"("year");
ALTER TABLE
    "races" ADD CONSTRAINT "races_circuitid_foreign" FOREIGN KEY("circuitId") REFERENCES "circuits"("circuitId");
ALTER TABLE
    "qualifying" ADD CONSTRAINT "qualifying_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "results" ADD CONSTRAINT "results_constructorid_foreign" FOREIGN KEY("constructorId") REFERENCES "constructors"("constructorId");
ALTER TABLE
    "qualifying" ADD CONSTRAINT "qualifying_driverid_foreign" FOREIGN KEY("driverId") REFERENCES "drivers"("driverId");
ALTER TABLE
    "results" ADD CONSTRAINT "results_driverid_foreign" FOREIGN KEY("driverId") REFERENCES "drivers"("driverId");
ALTER TABLE
    "sprint_results" ADD CONSTRAINT "sprint_results_constructorid_foreign" FOREIGN KEY("constructorId") REFERENCES "constructors"("constructorId");
ALTER TABLE
    "pit_stops" ADD CONSTRAINT "pit_stops_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "sprint_results" ADD CONSTRAINT "sprint_results_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
ALTER TABLE
    "constructor_standings" ADD CONSTRAINT "constructor_standings_raceid_foreign" FOREIGN KEY("raceId") REFERENCES "races"("raceId");
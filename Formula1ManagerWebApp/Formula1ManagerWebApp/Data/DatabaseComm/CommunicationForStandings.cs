using Formula1ManagerWebApp.Data;
using Formula1ManagerWebApp.Data.Models;
using Microsoft.EntityFrameworkCore;


namespace Formula1ManagerWebApp.Data.DatabaseComm
{

    class DatabaseCommunicationForStandings
    {
        private readonly ApplicationDbContext _dbContext;

        public DatabaseCommunicationForStandings(ApplicationDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task<List<LapTime>> GetDriverLapTimes(int driverId, int? raceId)
        {
            List<LapTime> driverLapTimes = await _dbContext.LapTimes
                .Where(lt => lt.driverId == driverId && lt.raceId == raceId)
                .OrderBy(lt => lt.lap)
                .ToListAsync();
            return driverLapTimes;
        }
        
        public async Task<List<int>> GetAllSeasons()
        {
            List<int> seasonsToReturn = await _dbContext.Races
                .Select(r => r.season)
                .Distinct()
                .OrderByDescending(season => season)
                .ToListAsync();
            return seasonsToReturn;
        }

        public async Task<List<Race>> GetRacesForSeason(int season)
        {
            List<Race> racesToReturn = await _dbContext.Races
                .Where(r => r.season == season)
                .OrderBy(r => r.date)
                .ToListAsync();
            return racesToReturn;
        }

        public async Task<List<Result>> GetResultsForRace(int? raceId)
        {
            List<Result> resultsToReturn = await _dbContext.Results
                .Where(r => r.raceId == raceId)
                .ToListAsync();
            return resultsToReturn;
        }

        public async Task<List<DriverStanding>> GetDriverStandingsForRace(int? raceId)
        {
            List<DriverStanding> standingsToReturn = await _dbContext.DriverStandings
                .Where(ds => ds.raceId == raceId)
                .OrderBy(ds => ds.position)
                .ToListAsync();
            return standingsToReturn;
        }

        public async Task<List<ConstructorStanding>> GetConstructorStandingsForRace(int? raceId)
        {
            List<ConstructorStanding> standingsToReturn = await _dbContext.ConstructorStandings
                .Where(ds => ds.raceId == raceId)
                .OrderBy(ds => ds.position)
                .ToListAsync();
            return standingsToReturn;
        }

        public async Task<List<Driver>> GetDriversForRace(List<DriverStanding> driverStandingsForRace)
        {
            List<int>? driverIds = driverStandingsForRace
                .Select(ds => ds.driverId)
                .Distinct()
                .ToList();
            var driversToReturn = await GetDriversByIds(driverIds);

            return driversToReturn;
        }

        public async Task<List<Constructor>> GetConstructorsForRace(List<ConstructorStanding> constructorStandingsForRace)
        {
            List<int>? constructorIds = constructorStandingsForRace
                .Select(ds => ds.constructorId)
                .Distinct()
                .ToList();
            var constructorsToReturn = await GetConstructorsByIds(constructorIds);

            return constructorsToReturn;
        }

        public async Task<List<Constructor>> GetConstructorsForRaceFromResults(List<Result> results)
        {
            List<int> constructorIds = results
                .Select(r => r.constructorId)
                .Distinct()
                .ToList();
            var constructorsToReturn = await _dbContext.Constructors
                .Where(c => constructorIds.Contains(c.constructorId))
                .ToListAsync();

            return constructorsToReturn;
        }

        public async Task<List<Driver>> GetDriversByIds(List<int> driverIds)
        {
            List<Driver> driversToReturn = new List<Driver>();
            // done by cycle so we keep the right order
            foreach (int driverId in driverIds)
            {
                var driver = await _dbContext.Drivers
                    .Where(d => d.driverId == driverId)
                    .FirstAsync();
                driversToReturn.Add(driver);
            }
            return driversToReturn;
        }

        public async Task<List<Constructor>> GetConstructorsByIds(List<int> constructorIds)
        {
            List<Constructor> constructorsToReturn = new List<Constructor>();
            // done by cycle so we keep the right order
            foreach (int constructorId in constructorIds)
            {
                var constructor = await _dbContext.Constructors
                    .Where(d => d.constructorId == constructorId)
                    .FirstAsync();
                constructorsToReturn.Add(constructor);
            }
            return constructorsToReturn;
        }

        public async Task<List<Driver>> GetDriversForResult(List<Result> results)
        {
            List<int> driverIds = results
                .Select(r => r.driverId)
                .Distinct()
                .ToList();
            var driversToReturn = await GetDriversByIds(driverIds);
            return driversToReturn;
        }

        public async Task<Driver> GetDriver(int driverId)
        {
            Driver driverToReturn = await _dbContext.Drivers
                .Where(d => d.driverId == driverId)
                .FirstAsync();
            return driverToReturn;
        }

        public async Task<Race> GetRace(int? raceId)
        {
            Race raceToReturn = await _dbContext.Races
                .Where(r => r.raceId == raceId)
                .FirstAsync();
            return raceToReturn;
        }
    }
    
}

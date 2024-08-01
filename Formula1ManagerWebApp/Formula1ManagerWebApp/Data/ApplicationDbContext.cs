using Formula1ManagerWebApp.Data.Models;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace Formula1ManagerWebApp.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }
        public DbSet<Driver> Drivers { get; set; }
        public DbSet<Constructor> Constructors { get; set; }
        public DbSet<Race> Races { get; set; }
        public DbSet<Circuit> Circuits { get; set; }
        public DbSet<Result> Results { get; set; }
        public DbSet<DriverStanding> DriverStandings { get; set; }
        public DbSet<ConstructorStanding> ConstructorStandings { get; set; }
        public DbSet<LapTime> LapTimes { get; set; }
        public DbSet<SafetyCar> SafetyCars { get; set; }
        public DbSet<RedFlag> RedFlags { get; set; }
        public DbSet<Qualifying> Qualifyings { get; set; }
        public DbSet<PitStop> PitStops { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseNpgsql("Host=localhost;Database=postgres;Username=airflow;Password=airflow");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Additional configuration here if needed
        }
    }
}

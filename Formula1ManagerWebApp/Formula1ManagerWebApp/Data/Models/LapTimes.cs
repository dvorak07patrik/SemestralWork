using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_lap_times")]
    public class LapTime
    {
        [Key]
        public int lapTimeId { get; set; }
        public int raceId { get; set; }
        public int driverId { get; set; }
        public short lap { get; set; }
        public short position { get; set; }
        public string time { get; set; }
        public int milliseconds { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }

        [ForeignKey("DriverId")]
        public Driver driver { get; set; }
    }
}

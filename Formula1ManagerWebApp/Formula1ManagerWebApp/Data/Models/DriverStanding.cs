using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_driver_standings")]
    public class DriverStanding
    {
        [Key]
        public int driverStandingsId { get; set; }
        public int raceId { get; set; }
        public int driverId { get; set; }
        public float points { get; set; }
        public short position { get; set; }
        public string positionText { get; set; }
        public short wins { get; set; }

        [ForeignKey("raceId")]
        public Race race { get; set; }

        [ForeignKey("driverId")]
        public Driver driver { get; set; }
    }
}

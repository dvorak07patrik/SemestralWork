using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_pit_stops")]
    public class PitStop
    {
        [Key]
        public int pitStopId { get; set; }
        public int raceId { get; set; }
        public int driverId { get; set; }
        public short stops { get; set; }
        public short lap { get; set; }
        public string time { get; set; }
        public float duration { get; set; }
        public long milliseconds { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }

        [ForeignKey("DriverId")]
        public Driver driver { get; set; }
    }
}

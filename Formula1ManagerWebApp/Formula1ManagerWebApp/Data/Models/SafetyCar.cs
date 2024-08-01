using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_safety_cars")]
    public class SafetyCar
    {
        [Key]
        public int safetyCarId { get; set; }
        public int raceId { get; set; }
        public string cause { get; set; }
        public short deployed { get; set; }
        public short retreated { get; set; }
        public short fullLaps { get; set; }
        public string type { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }
    }
}

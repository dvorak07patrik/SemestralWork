using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_qualifying")]
    public class Qualifying
    {
        [Key]
        public int qualifyId { get; set; }
        public int raceId { get; set; }
        public int driverId { get; set; }
        public int constructorId { get; set; }
        public short number { get; set; }
        public short position { get; set; }
        public string q1 { get; set; }
        public string q2 { get; set; }
        public string q3 { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }

        [ForeignKey("DriverId")]
        public Driver driver { get; set; }

        [ForeignKey("ConstructorId")]
        public Constructor constructor { get; set; }
    }
}

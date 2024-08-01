using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_results")]
    public class Result
    {
        [Key]
        public int resultId { get; set; }
        public int raceId { get; set; }
        public int driverId { get; set; }
        public int constructorId { get; set; }
        public short number { get; set; }
        public short grid { get; set; }
        public short position { get; set; }
        public string positionText { get; set; }
        public short positionOrder { get; set; }
        public float points { get; set; }
        public string timeOrRetired { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }

        [ForeignKey("DriverId")]
        public Driver driver { get; set; }

        [ForeignKey("ConstructorId")]
        public Constructor constructor { get; set; }
    }

}

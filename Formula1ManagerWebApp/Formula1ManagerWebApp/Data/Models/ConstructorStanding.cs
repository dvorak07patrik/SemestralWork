using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_constructor_standings")]
    public class ConstructorStanding
    {
        [Key]
        public int constructorStandingsId { get; set; }
        public int raceId { get; set; }
        public int constructorId { get; set; }
        public float points { get; set; }
        public short position { get; set; }
        public string positionText { get; set; }
        public int wins { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }

        [ForeignKey("ConstructorId")]
        public Constructor constructor { get; set; }
    }
}

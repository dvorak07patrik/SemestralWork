using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("fact_red_flags")]
    public class RedFlag
    {
        [Key]
        public int redFlagId { get; set; }
        public int raceId { get; set; }
        public short lap { get; set; }
        public string resumed { get; set; }
        public string incident { get; set; }
        public string excluded { get; set; }

        [ForeignKey("RaceId")]
        public Race race { get; set; }
    }
}

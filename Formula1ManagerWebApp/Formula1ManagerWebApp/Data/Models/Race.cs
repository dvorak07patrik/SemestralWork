using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("dim_races")]
    public class Race
    {
        [Key]
        public int raceId { get; set; }
        public int season { get; set; }
        public short round { get; set; }
        public int circuitId { get; set; }
        public string name { get; set; }
        public DateTime date { get; set; }
        public TimeSpan time { get; set; }
        public string url { get; set; }

        [ForeignKey("circuitId")]
        public Circuit circuit { get; set; }
    }
}

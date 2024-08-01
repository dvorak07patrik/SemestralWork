using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("dim_circuits")]
    public class Circuit
    {
        [Key]
        public int circuitId { get; set; }
        public string circuitRef { get; set; }
        public string name { get; set; }
        public string location { get; set; }
        public string country { get; set; }
        public float lat { get; set; }
        public float lng { get; set; }
        public int alt { get; set; }
        public string url { get; set; }
    }
}

using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("dim_drivers")]
    public class Driver
    {
        [Key]
        public int driverId { get; set; }
        public string? driverRef { get; set; }
        public short number { get; set; }
        public string? code { get; set; }
        public string? forename { get; set; }
        public string? surname { get; set; }
        public DateTime dob { get; set; }
        public string? nationality { get; set; }
        public string? url { get; set; }
    }
}

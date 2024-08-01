using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Formula1ManagerWebApp.Data.Models
{
    [Table("dim_constructors")]
    public class Constructor
    {
        [Key]
        public int constructorId { get; set; }
        public string? constructorRef { get; set; }
        public string? name { get; set; }
        public string? nationality { get; set; }
        public string? url { get; set; }
    }
}

using Formula1ManagerWebApp.Data;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;

namespace Formula1ManagerWebApp.Data
{
    public class IdentityDbContext : IdentityDbContext<ApplicationUser>
    {
        public IdentityDbContext(DbContextOptions<IdentityDbContext> options)
            : base(options)
        {
        }

    }

}


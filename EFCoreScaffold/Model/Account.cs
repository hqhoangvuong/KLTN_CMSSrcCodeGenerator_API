using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class Account
    {
        public Account()
        {
            SystemLogs = new HashSet<SystemLog>();
        }

        public string UserName { get; set; }
        public string DisplayName { get; set; }
        public string PassWord { get; set; }
        public int Type { get; set; }
        public bool Isdelete { get; set; }

        public virtual ICollection<SystemLog> SystemLogs { get; set; }
    }
}

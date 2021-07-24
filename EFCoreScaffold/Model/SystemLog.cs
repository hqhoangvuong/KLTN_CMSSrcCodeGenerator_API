using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class SystemLog
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Displayname { get; set; }
        public int Type { get; set; }
        public DateTime? Datelogin { get; set; }
        public DateTime? Datelogout { get; set; }

        public virtual Account UsernameNavigation { get; set; }
    }
}

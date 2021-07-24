using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class SystemTableConfig
    {
        public SystemTableConfig()
        {
            SystemTableColumnConfigs = new HashSet<SystemTableColumnConfig>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string ExplicitName { get; set; }
        public bool IsHidden { get; set; }
        public string ActionGroup { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        public bool IsDeleted { get; set; }

        public virtual ICollection<SystemTableColumnConfig> SystemTableColumnConfigs { get; set; }
    }
}

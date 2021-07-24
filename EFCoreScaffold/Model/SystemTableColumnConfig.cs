using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class SystemTableColumnConfig
    {
        public int Id { get; set; }
        public int TableId { get; set; }
        public string Name { get; set; }
        public string ExplicitName { get; set; }
        public string DataType { get; set; }
        public string ExplicitDataType { get; set; }
        public int OrdinalPosition { get; set; }
        public string ColumnDefault { get; set; }
        public int CharacterMaximumLength { get; set; }
        public int CharacterOctetLength { get; set; }
        public int DisplayComponent { get; set; }
        public string IsNullable { get; set; }
        public bool IsPrimaryKey { get; set; }
        public bool IsForeignKey { get; set; }
        public bool IsHidden { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        public bool IsDeleted { get; set; }

        public virtual SystemTableConfig Table { get; set; }
    }
}

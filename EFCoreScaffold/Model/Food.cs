using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class Food
    {
        public Food()
        {
            BillInfos = new HashSet<BillInfo>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public double Price { get; set; }
        public string Category { get; set; }
        public bool IsDelete { get; set; }
        public int? Discount { get; set; }

        public virtual ICollection<BillInfo> BillInfos { get; set; }
    }
}

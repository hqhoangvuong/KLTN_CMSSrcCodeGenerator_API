using System;
using System.Collections.Generic;

#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class Voucher
    {
        public int Id { get; set; }
        public int Discountpercent { get; set; }
        public string Name { get; set; }
        public int Status { get; set; }
        public double Minbillprice { get; set; }
        public double Maxbillprice { get; set; }
        public DateTime Effectivedate { get; set; }
        public DateTime Expireddate { get; set; }
        public DateTime? Useddate { get; set; }
        public int Usedbillid { get; set; }
        public bool Isdeleted { get; set; }
    }
}

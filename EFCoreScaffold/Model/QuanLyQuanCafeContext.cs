using Microsoft.EntityFrameworkCore;


#nullable disable

namespace EFCoreScaffoldexample.Model
{
    public partial class QuanLyQuanCafeContext : DbContext
    {
        public QuanLyQuanCafeContext()
        {
        }

        public QuanLyQuanCafeContext(DbContextOptions<QuanLyQuanCafeContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Account> Accounts { get; set; }
        public virtual DbSet<AspNetRole> AspNetRoles { get; set; }
        public virtual DbSet<AspNetRoleClaim> AspNetRoleClaims { get; set; }
        public virtual DbSet<AspNetUser> AspNetUsers { get; set; }
        public virtual DbSet<AspNetUserClaim> AspNetUserClaims { get; set; }
        public virtual DbSet<AspNetUserLogin> AspNetUserLogins { get; set; }
        public virtual DbSet<AspNetUserRole> AspNetUserRoles { get; set; }
        public virtual DbSet<AspNetUserToken> AspNetUserTokens { get; set; }
        public virtual DbSet<Bill> Bills { get; set; }
        public virtual DbSet<BillInfo> BillInfos { get; set; }
        public virtual DbSet<Food> Foods { get; set; }
        public virtual DbSet<GetAllCheckedoutBill> GetAllCheckedoutBills { get; set; }
        public virtual DbSet<GetAllFood> GetAllFoods { get; set; }
        public virtual DbSet<GetAllVouncher> GetAllVounchers { get; set; }
        public virtual DbSet<SysLogDisp> SysLogDisps { get; set; }
        public virtual DbSet<SystemLog> SystemLogs { get; set; }
        public virtual DbSet<SystemMasterConfig> SystemMasterConfigs { get; set; }
        public virtual DbSet<SystemTableColumnConfig> SystemTableColumnConfigs { get; set; }
        public virtual DbSet<SystemTableConfig> SystemTableConfigs { get; set; }
        public virtual DbSet<SystemTableForeingKeyConfig> SystemTableForeingKeyConfigs { get; set; }
        public virtual DbSet<TableFood> TableFoods { get; set; }
        public virtual DbSet<Voucher> Vouchers { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("Server=vuonghuynhsolutions.tech;Database=QuanLyQuanCafe;Persist Security Info=True;User ID=vuongqhhuynh;Password=Hoangvuong1024");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.HasAnnotation("Relational:Collation", "SQL_Latin1_General_CP1_CI_AS");

            modelBuilder.Entity<Account>(entity =>
            {
                entity.HasKey(e => e.UserName)
                    .HasName("PK__Account__C9F2845794A9F385");

                entity.ToTable("Account");

                entity.Property(e => e.UserName).HasMaxLength(100);

                entity.Property(e => e.DisplayName)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasDefaultValueSql("(N'Kter')");

                entity.Property(e => e.Isdelete).HasColumnName("isdelete");

                entity.Property(e => e.PassWord)
                    .IsRequired()
                    .HasMaxLength(1000)
                    .HasDefaultValueSql("((0))");
            });

            modelBuilder.Entity<AspNetRole>(entity =>
            {
                entity.HasIndex(e => e.NormalizedName, "RoleNameIndex")
                    .IsUnique()
                    .HasFilter("([NormalizedName] IS NOT NULL)");

                entity.Property(e => e.Name).HasMaxLength(256);

                entity.Property(e => e.NormalizedName).HasMaxLength(256);
            });

            modelBuilder.Entity<AspNetRoleClaim>(entity =>
            {
                entity.HasIndex(e => e.RoleId, "IX_AspNetRoleClaims_RoleId");

                entity.Property(e => e.RoleId).IsRequired();

                entity.HasOne(d => d.Role)
                    .WithMany(p => p.AspNetRoleClaims)
                    .HasForeignKey(d => d.RoleId);
            });

            modelBuilder.Entity<AspNetUser>(entity =>
            {
                entity.HasIndex(e => e.NormalizedEmail, "EmailIndex");

                entity.HasIndex(e => e.NormalizedUserName, "UserNameIndex")
                    .IsUnique()
                    .HasFilter("([NormalizedUserName] IS NOT NULL)");

                entity.Property(e => e.Email).HasMaxLength(256);

                entity.Property(e => e.NormalizedEmail).HasMaxLength(256);

                entity.Property(e => e.NormalizedUserName).HasMaxLength(256);

                entity.Property(e => e.UserName).HasMaxLength(256);
            });

            modelBuilder.Entity<AspNetUserClaim>(entity =>
            {
                entity.HasIndex(e => e.UserId, "IX_AspNetUserClaims_UserId");

                entity.Property(e => e.UserId).IsRequired();

                entity.HasOne(d => d.User)
                    .WithMany(p => p.AspNetUserClaims)
                    .HasForeignKey(d => d.UserId);
            });

            modelBuilder.Entity<AspNetUserLogin>(entity =>
            {
                entity.HasKey(e => new { e.LoginProvider, e.ProviderKey });

                entity.HasIndex(e => e.UserId, "IX_AspNetUserLogins_UserId");

                entity.Property(e => e.UserId).IsRequired();

                entity.HasOne(d => d.User)
                    .WithMany(p => p.AspNetUserLogins)
                    .HasForeignKey(d => d.UserId);
            });

            modelBuilder.Entity<AspNetUserRole>(entity =>
            {
                entity.HasKey(e => new { e.UserId, e.RoleId });

                entity.HasIndex(e => e.RoleId, "IX_AspNetUserRoles_RoleId");

                entity.HasOne(d => d.Role)
                    .WithMany(p => p.AspNetUserRoles)
                    .HasForeignKey(d => d.RoleId);

                entity.HasOne(d => d.User)
                    .WithMany(p => p.AspNetUserRoles)
                    .HasForeignKey(d => d.UserId);
            });

            modelBuilder.Entity<AspNetUserToken>(entity =>
            {
                entity.HasKey(e => new { e.UserId, e.LoginProvider, e.Name });

                entity.HasOne(d => d.User)
                    .WithMany(p => p.AspNetUserTokens)
                    .HasForeignKey(d => d.UserId);
            });

            modelBuilder.Entity<Bill>(entity =>
            {
                entity.ToTable("Bill");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.DateCheckIn)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("(getdate())");

                entity.Property(e => e.DateCheckOut).HasColumnType("datetime");

                entity.Property(e => e.IdTable).HasColumnName("idTable");

                entity.Property(e => e.Status).HasColumnName("status");

                entity.Property(e => e.Totalprice)
                    .HasColumnName("totalprice")
                    .HasDefaultValueSql("((-1))");

                entity.HasOne(d => d.IdTableNavigation)
                    .WithMany(p => p.Bills)
                    .HasForeignKey(d => d.IdTable)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__Bill__status__49C3F6B7");
            });

            modelBuilder.Entity<BillInfo>(entity =>
            {
                entity.ToTable("BillInfo");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Count).HasColumnName("count");

                entity.Property(e => e.IdBill).HasColumnName("idBill");

                entity.Property(e => e.IdFood).HasColumnName("idFood");

                entity.HasOne(d => d.IdBillNavigation)
                    .WithMany(p => p.BillInfos)
                    .HasForeignKey(d => d.IdBill)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__BillInfo__count__4D94879B");

                entity.HasOne(d => d.IdFoodNavigation)
                    .WithMany(p => p.BillInfos)
                    .HasForeignKey(d => d.IdFood)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__BillInfo__idFood__4E88ABD4");
            });

            modelBuilder.Entity<Food>(entity =>
            {
                entity.ToTable("Food");

                entity.HasIndex(e => e.Category, "idx_fcate");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Category)
                    .HasMaxLength(50)
                    .HasColumnName("category");

                entity.Property(e => e.Discount).HasColumnName("discount");

                entity.Property(e => e.IsDelete).HasColumnName("isDelete");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("name")
                    .HasDefaultValueSql("(N'Chưa đặt tên')");

                entity.Property(e => e.Price).HasColumnName("price");
            });

            modelBuilder.Entity<GetAllCheckedoutBill>(entity =>
            {
                entity.HasNoKey();

                entity.ToView("GetAllCheckedoutBill");

                entity.Property(e => e.DateCheckIn).HasColumnType("datetime");

                entity.Property(e => e.DateCheckOut).HasColumnType("datetime");

                entity.Property(e => e.Id)
                    .ValueGeneratedOnAdd()
                    .HasColumnName("id");

                entity.Property(e => e.IdTable).HasColumnName("idTable");

                entity.Property(e => e.Status).HasColumnName("status");

                entity.Property(e => e.Totalprice).HasColumnName("totalprice");
            });

            modelBuilder.Entity<GetAllFood>(entity =>
            {
                entity.HasNoKey();

                entity.ToView("GetAllFood");

                entity.Property(e => e.Category)
                    .HasMaxLength(50)
                    .HasColumnName("category");

                entity.Property(e => e.Discount).HasColumnName("discount");

                entity.Property(e => e.Id)
                    .ValueGeneratedOnAdd()
                    .HasColumnName("id");

                entity.Property(e => e.IsDelete).HasColumnName("isDelete");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("name");

                entity.Property(e => e.Price).HasColumnName("price");
            });

            modelBuilder.Entity<GetAllVouncher>(entity =>
            {
                entity.HasNoKey();

                entity.ToView("GetAllVouncher");

                entity.Property(e => e.Discountpercent).HasColumnName("discountpercent");

                entity.Property(e => e.Effectivedate)
                    .HasColumnType("datetime")
                    .HasColumnName("effectivedate");

                entity.Property(e => e.Expireddate)
                    .HasColumnType("datetime")
                    .HasColumnName("expireddate");

                entity.Property(e => e.Id)
                    .ValueGeneratedOnAdd()
                    .HasColumnName("id");

                entity.Property(e => e.Isdeleted).HasColumnName("isdeleted");

                entity.Property(e => e.Maxbillprice).HasColumnName("maxbillprice");

                entity.Property(e => e.Minbillprice).HasColumnName("minbillprice");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("name");

                entity.Property(e => e.Status).HasColumnName("status");

                entity.Property(e => e.Usedbillid).HasColumnName("usedbillid");

                entity.Property(e => e.Useddate)
                    .HasColumnType("datetime")
                    .HasColumnName("useddate");
            });

            modelBuilder.Entity<SysLogDisp>(entity =>
            {
                entity.HasNoKey();

                entity.ToView("SysLog_Disp");

                entity.Property(e => e.Datelogin)
                    .HasColumnType("datetime")
                    .HasColumnName("datelogin");

                entity.Property(e => e.Datelogout)
                    .HasColumnType("datetime")
                    .HasColumnName("datelogout");

                entity.Property(e => e.Displayname)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("displayname");

                entity.Property(e => e.Username)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("username");
            });

            modelBuilder.Entity<SystemLog>(entity =>
            {
                entity.ToTable("SystemLog");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Datelogin)
                    .HasColumnType("datetime")
                    .HasColumnName("datelogin");

                entity.Property(e => e.Datelogout)
                    .HasColumnType("datetime")
                    .HasColumnName("datelogout");

                entity.Property(e => e.Displayname)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("displayname")
                    .HasDefaultValueSql("(N'Employee')");

                entity.Property(e => e.Username)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("username");

                entity.HasOne(d => d.UsernameNavigation)
                    .WithMany(p => p.SystemLogs)
                    .HasForeignKey(d => d.Username)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK_SystemLog_Account");
            });

            modelBuilder.Entity<SystemMasterConfig>(entity =>
            {
                entity.HasIndex(e => e.ConfigName, "IX_SystemMasterConfigs_ConfigName")
                    .IsUnique();

                entity.Property(e => e.ConfigName)
                    .IsRequired()
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.ConfigValue)
                    .HasMaxLength(200)
                    .IsUnicode(false);
            });

            modelBuilder.Entity<SystemTableColumnConfig>(entity =>
            {
                entity.HasIndex(e => new { e.TableId, e.Name }, "IX_SystemTableColumnConfigs_TableId_Name")
                    .IsUnique();

                entity.Property(e => e.ColumnDefault)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.DataType)
                    .IsRequired()
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.ExplicitDataType)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.ExplicitName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.IsNullable)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.HasOne(d => d.Table)
                    .WithMany(p => p.SystemTableColumnConfigs)
                    .HasForeignKey(d => d.TableId);
            });

            modelBuilder.Entity<SystemTableConfig>(entity =>
            {
                entity.HasIndex(e => e.Name, "IX_SystemTableConfigs_Name")
                    .IsUnique();

                entity.Property(e => e.ActionGroup)
                    .IsRequired()
                    .HasMaxLength(10)
                    .IsUnicode(false);

                entity.Property(e => e.ExplicitName)
                    .IsRequired()
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(200)
                    .IsUnicode(false);
            });

            modelBuilder.Entity<SystemTableForeingKeyConfig>(entity =>
            {
                entity.Property(e => e.FkName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.MappedRefrencedColumnName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.RefrencedColumnName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.RefrencedTableName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.SourceColumnName)
                    .HasMaxLength(200)
                    .IsUnicode(false);

                entity.Property(e => e.SourceTableName)
                    .HasMaxLength(200)
                    .IsUnicode(false);
            });

            modelBuilder.Entity<TableFood>(entity =>
            {
                entity.ToTable("TableFood");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("name")
                    .HasDefaultValueSql("(N'Bàn chưa có tên')");

                entity.Property(e => e.RentTime)
                    .HasColumnType("datetime")
                    .HasColumnName("rentTime")
                    .HasDefaultValueSql("('1/1/1900 00:00:00')");

                entity.Property(e => e.Status)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("status")
                    .HasDefaultValueSql("(N'Trống')");
            });

            modelBuilder.Entity<Voucher>(entity =>
            {
                entity.HasKey(e => new { e.Id, e.Discountpercent })
                    .HasName("PK__Voucher__3213E83FB45F11BF");

                entity.ToTable("Voucher");

                entity.Property(e => e.Id)
                    .ValueGeneratedOnAdd()
                    .HasColumnName("id");

                entity.Property(e => e.Discountpercent).HasColumnName("discountpercent");

                entity.Property(e => e.Effectivedate)
                    .HasColumnType("datetime")
                    .HasColumnName("effectivedate");

                entity.Property(e => e.Expireddate)
                    .HasColumnType("datetime")
                    .HasColumnName("expireddate");

                entity.Property(e => e.Isdeleted).HasColumnName("isdeleted");

                entity.Property(e => e.Maxbillprice)
                    .HasColumnName("maxbillprice")
                    .HasDefaultValueSql("((-1))");

                entity.Property(e => e.Minbillprice).HasColumnName("minbillprice");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("name");

                entity.Property(e => e.Status)
                    .HasColumnName("status")
                    .HasDefaultValueSql("(N'0')");

                entity.Property(e => e.Usedbillid)
                    .HasColumnName("usedbillid")
                    .HasDefaultValueSql("((-1))");

                entity.Property(e => e.Useddate)
                    .HasColumnType("datetime")
                    .HasColumnName("useddate");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using CustomerTemplateAPI.Repositories.Interfaces;
using CustomerTemplateAPI.Data;
using CustomerTemplateAPI.Models;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using CustomerTemplateAPI.Extensions;

namespace CustomerTemplateAPI.Repositories
{
    public class ---RepositoryName--- : GenericRepository<---ModelName--->, ---InterfaceName---
    {
        private readonly ApplicationDbContext context;

        public ---RepositoryName---(ApplicationDbContext context) : base(context)
        {
            this.context = context ?? throw new ArgumentNullException(nameof(context));
        }

        public IEnumerable<---ModelName---> FindAll()
        {
            return GetAll().AsQueryable();
        }

        public IEnumerable<---ModelName---> FindAllWithPaging(int pageIndex, int pageSize)
        {
            var result = FindAll();
            if (pageIndex > 0 && pageSize > 0)
            {
                return result.Paging(pageIndex, pageSize);
            }

            return result;
        }

        public async Task<---ModelName---> FindById(---FKParams---)
        {
            object[] parameters = new object[<--NumberOfFK-->];
            // Some binding here
            return await GetItemById(parameters);
        }

        public async Task<---ModelName---> Insert(---ModelName--- item)
        {
            return await Create(item);
        }

        public async Task<---ModelName---> Modify(---ModelName--- item)
        {
            return await Update(item);
        }

        public async Task<int> DeleteItem(---ModelName--- item)
        {
            return await Delete(item);
        }
    }
}

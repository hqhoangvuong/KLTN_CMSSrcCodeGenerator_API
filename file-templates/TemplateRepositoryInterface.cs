using CustomerTemplateAPI.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CustomerTemplateAPI.Repositories.Interfaces
{
    public interface ---InterfaceName---
    {
        public IEnumerable<---ModelName---> FindAll();
        public IEnumerable<---ModelName---> FindAllWithPaging(int pageIndex, int pageSize);
        public Task<---ModelName---> FindById(---FKParams---);
        public Task<---ModelName---> Insert(---ModelName--- item);
        public Task<---ModelName---> Modify(---ModelName--- item);
        Task<int> DeleteItem(---ModelName--- item);
    }
}
using Microsoft.AspNetCore.Authorization;
using CustomerTemplateAPI.Commons;
using CustomerTemplateAPI.Models;
using CustomerTemplateAPI.Repositories.Interfaces;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

namespace CustomerTemplateAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize]
    public class [ClassController] : ControllerBase
    {
        private readonly [RepositoryInterface] _repo;

        public [ClassController]([RepositoryInterface] repository)
        {
            _repo = repository;
        }

        /** Uncomment Get all
        [HttpGet]
        [ProducesResponseType((int)HttpStatusCode.OK)]
        [ProducesResponseType((int)HttpStatusCode.InternalServerError)]
        public IEnumerable<[ModelName]> Get()
        {
            return _repo.FindAll();
        }
        Uncomment Get all **/

        /** Uncomment Get all with paging
        [HttpGet("paging")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public virtual IEnumerable<[ModelName]> GetWithPaging(int pageIndex, int pageSize)
        {
            var result = _repo.FindAllWithPaging(pageIndex, pageSize);

            return result;
        }
        Uncomment Get all with paging **/

        /** Uncomment Get by Id
        [HttpGet("id")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public virtual async Task<ActionResult<[ModelName]>> GetById(---FKParams---)
        {
            var result = await _repo.FindById(---Params---);

            if(result == null)
            {
                return CheckData<[ModelName]>.ItemNotFound(--DeleteItemNotFound--);
            }

            return Ok(result);
        }
        Uncomment Get by Id **/

        /** Uncomment Post
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public virtual async Task<ActionResult> Post([FromBody] [ModelName] newItem)
        {
            var value = await _repo.FindById(--PostFkCallParams--).ConfigureAwait(true);
            if(value != null)
            {
                return CheckData<[ModelName]>.ItemIntExists("[FirstFK]", value.[FirstFK]);
            }

            var result = await _repo.Insert(newItem).ConfigureAwait(true);
            return Created("", result);
        }
        Uncomment Post **/


        /** Uncomment Put
        [HttpPut()]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public virtual async Task<ActionResult<[ModelName]>> Put([FromBody] [ModelName] updatedItem)
        {
            var exsited = await _repo.FindById(--PutFkCallParams--).ConfigureAwait(true);

            if(exsited == null)
            {
                return CheckData<[ModelName]>.ItemNotFound(updatedItem.[FirstFK]);
            }

            var updatedResult = await _repo.Modify(updatedItem);
            return Ok(updatedResult);
        }
        Uncomment Put **/


        /** Uncomment Delete
        [HttpDelete()]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<ActionResult<int>> Delete(---FKParams---)
        {
            try
            {
                var deleteItem = await _repo.FindById(--DeleteFkCallParams--);
                if (deleteItem == null)
                {
                    return CheckData<[ModelName]>.ItemNotFound(--DeleteItemNotFound--);
                }

                int deletedItemCount = await _repo.DeleteItem(deleteItem);
                return Ok(deletedItemCount);
            }
            catch(Exception ex)
            {
                return BadRequest(ex.InnerException.Message);
            }
        }
        Uncomment Delete **/
    }
}

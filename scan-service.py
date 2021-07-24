import redis
from models import ApiCreateResult
from rq.job import Job
from rq import Queue
from worker import conn
import time
from string import Template
from rq.registry import FinishedJobRegistry, StartedJobRegistry
from DbReader import AdminDbReader
from SendingMail import MaillingService
q = Queue(connection=conn)

touched_jobs = []


def read_template():
    filename = './file-templates/EmailTemplate.txt'
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_all_job():
    registry = StartedJobRegistry('default', connection=conn)
    registry_finished = FinishedJobRegistry('default', connection=conn)
    queued_job_ids = registry.get_queue().job_ids
    running_job_ids = registry.get_job_ids()
    finished_job_ids = registry_finished.get_job_ids()
    all_job_ids = queued_job_ids + running_job_ids + finished_job_ids
    keys = conn.keys('rq:job*')
    job_list = []
    all_untouch_job = (x for x in all_job_ids if x not in touched_jobs)
    for job_id in all_untouch_job:
        job = Job.fetch(job_id, connection=conn)
        result = None
        if job.is_finished:
            job_result = job.result
            result = ApiCreateResult(job_result.Status,
                                     job_result.ApiGuid,
                                     job_result.ApiDownloadLink,
                                     job_result.ErrorMessage,
                                     job_result.PackageName,
                                     job_result.DbGuid,
                                     job_result.ClientAppGuid,
                                     job_result.ClientAppDownloadLink)
            touched_jobs.append(job_id)
        else:
            job_status = ''
            if job.is_queued:
                job_status = 'in-queue'
            elif job.is_started:
                job_status = 'waiting'
            elif job.is_failed:
                job_status = 'failed'
                touched_jobs.append(job_id)
            result = ApiCreateResult(job_status,
                                     '',
                                     ''
                                     )
        job_list.append(result)
    return job_list


def main():
    reset_count = 0
    while True:
        if reset_count == 100:
            touched_jobs = []

        update_count = 0
        job_results = get_all_job()
        for result in job_results:
            if result.DbGuid != '':
                AdminDbReader().populate_status(
                    result.DbGuid, 
                    result.ApiDownloadLink, 
                    result.ApiGuid,
                    result.ClientAppGuid,
                    result.ClientAppDownloadLink)
                MaillingService().send_result(result.DbGuid, 
                                              result.ApiDownloadLink, 
                                              'https://www.npmjs.com/package/@hqhoangvuong/api-client-' + str(result.PackageName), 
                                              result.ClientAppDownloadLink,
                                              str(result.PackageName))
                update_count += 1
        print('Updated {0} object(s)'.format(update_count))
        reset_count += 1
        time.sleep(30)


if __name__ == '__main__':
    main()

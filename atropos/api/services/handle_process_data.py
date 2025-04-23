import logging

from sqlmodel import Session
from atropos.db import engine
from time import sleep

from atropos.api.services.handle_task import HandleTask
from atropos.api.services.get_task_by_id import GetTaskById
from atropos.api.models.task import Task as TaskRecord

from atropos.api.errors import RecordNotFoundError


class HandleProcessData(HandleTask):
    def handle_process_data_helper(self, task: TaskRecord, data: dict):
        """This task is more of an example of a possible long running task
        right now. So the function just sleeps for a while and then returns a
        mock download link
        """
        sleep(30)
        logging.info(f"Simulated processing complete for task {task.id}")
        return "https://example.com/download_link"

    def __call__(self, task_id: str, data: dict) -> None:
        with Session(engine) as session:
            try:
                task = GetTaskById()(task_id, session)
                task.status = "in-progress"
                session.add(task)
                session.commit()

                download_link = self.handle_process_data_helper(task, data)

                task.status = "succeeded"
                task.download_url = download_link
                session.add(task)
                session.commit()

            except RecordNotFoundError:
                logging.error(f"Task with ID {task_id} not found")

            except:
                logging.exception("Error processing task")

                task.status = "failed"
                session.add(task)
                session.commit()

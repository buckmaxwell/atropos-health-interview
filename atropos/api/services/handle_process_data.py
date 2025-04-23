from atropos.api.services.handle_task import HandleTask


class HandleProcessData(HandleTask):
    def __call__(self, task_id: str, data: dict) -> None:
        print(f"[Worker] Processing data for task {task_id}")
        # Look up the task in the DB, mark in-progress, do work, mark succeeded

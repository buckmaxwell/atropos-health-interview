class AtroposError(Exception):
    """Base class for all exceptions raised by Atropos."""

    pass


class RecordNotFoundError(AtroposError):
    pass


class InvalidTaskTypeError(AtroposError):
    def __init__(self, task_type: str, valid_types: list[str]):
        self.task_type = task_type
        self.valid_types = valid_types
        self.message = f"Unsupported task type: '{task_type}'"
        super().__init__(self.message)

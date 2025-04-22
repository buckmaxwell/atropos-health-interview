from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Literal, Any, Dict, Optional
from pydantic.json_schema import GenerateJsonSchema


from atropos.api.schemas.task_type.base import TaskType


class DataProcessingPayload(BaseModel):
    file_url: HttpUrl = Field(
        ..., description="Publicly accessible URL pointing to the input CSV file."
    )
    delimiter: Optional[str] = Field(
        default=",", description="Optional delimiter used in the CSV file."
    )

    model_config = ConfigDict(title="Data Processing Input Schema")


def get_full_schema_doc() -> Dict[str, Any]:
    schema = DataProcessingPayload.model_json_schema(
        schema_generator=GenerateJsonSchema
    )
    schema["$schema"] = GenerateJsonSchema.schema_dialect
    return schema


class DataProcessingResponse(TaskType):
    type: Literal["data-processing"] = "data-processing"
    description: Literal[
        "Processes a CSV file from a public URL and generates a summary report."
    ] = "Processes a CSV file from a public URL and generates a summary report."
    payload_schema: Dict[str, Any] = Field(default_factory=get_full_schema_doc)

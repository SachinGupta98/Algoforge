from pydantic import BaseModel, Field


class CoachRequest(BaseModel):
    question: str = Field(min_length=3)
    topic: str = "Arrays"
    student_level: str = "Beginner"


class CoachResponse(BaseModel):
    reply: str
    provider: str


class ExecuteRequest(BaseModel):
    source_code: str = Field(min_length=1)
    language_id: int
    stdin: str = ""


class ExecuteResponse(BaseModel):
    stdout: str | None = None
    stderr: str | None = None
    compile_output: str | None = None
    status: str
    time: str | None = None
    memory: int | None = None

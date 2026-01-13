from datetime import date
from pydantic import BaseModel, Field

class IngestResponse(BaseModel):
    run_id: str
    rows_received: int

class AttendanceRow(BaseModel):
    employee_id: str = Field(min_length = 1)
    date: date
    status: str = Field(min_length= 1)
import csv, io, uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..core.db import get_db
from ..models.schemas import IngestResponse

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/attendance", response_model = IngestResponse)
async def ingest_attendance(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(status_code = 400, detail = "Only CSV files are supported!")
    
    raw_bytes = await file.read()
    try:
        text_data = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code = 400, detail = "CSV must be UTF-8 encoded.")
    
    reader = csv.DictReader(io.StringIO(text_data))
    required = {"employee_id", "date", "status"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise HTTPException(status_code = 400, detail = f"CSV must include columns: {sorted(required)}")
    
    run_id = str(uuid.uuid4())
    rows = 0

    insert_sql = text("""
        INSERT INTO raw.attendance (run_id, employee_id, date, status, source_file)
        VALUES (:run_id, :employee_id, :date, :status, :source_file)
        ON CONFLICT (run_id, employee_id, date) DO NOTHING
    """)

    for r in reader: 
        employee_id = (r.get("employee_id") or "").strip()
        date_val = (r.get("date") or "").strip()
        status = (r.get("status") or "").strip()

        if not employee_id or not date_val or not status:
            continue

        db.execute(insert_sql, {
            "run_id": run_id,
            "employee_id": employee_id,
            "date": date_val,
            "status": status,
            "source_file": file.filename,
        })
        rows += 1

    db.commit()
    return IngestResponse(run_id = run_id, rows_received = rows)

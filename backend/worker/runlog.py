from contextlib import contextmanager
from datetime import datetime, timezone

from core.db import SessionLocal
from core.models import IngestRun


@contextmanager
def logged_run(job: str):
    result: dict = {"status": "ok", "rows": 0, "failed": 0, "error": None}
    with SessionLocal() as s:
        run = IngestRun(job=job)
        s.add(run)
        s.commit()
        try:
            yield result
        except Exception as exc:
            result.update(status="failed", error=str(exc)[:500])
        run.status = result["status"]
        run.rows_written = result["rows"]
        run.tickers_failed = result["failed"]
        run.error = result["error"]
        run.finished_at = datetime.now(timezone.utc)
        s.commit()
    return result

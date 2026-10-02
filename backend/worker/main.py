import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from core.config import get_settings
from worker.jobs import ingest_fundamentals, sync_companies
from worker.pipeline import run_daily_pipeline


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    cfg = get_settings()
    sched = BlockingScheduler(timezone=cfg.timezone)
    common = {"max_instances": 1, "coalesce": True, "misfire_grace_time": 3600}
    sched.add_job(
        run_daily_pipeline,
        CronTrigger(day_of_week="mon-fri", hour=cfg.pipeline_hour, minute=0),
        id="daily_pipeline",
        **common,
    )
    sched.add_job(
        sync_companies.run,
        CronTrigger(day_of_week="mon", hour=6),
        id="sync_companies",
        **common,
    )
    sched.add_job(
        ingest_fundamentals.run,
        CronTrigger(day_of_week="sat", hour=8),
        id="fundamentals",
        **common,
    )
    sched.start()


if __name__ == "__main__":
    main()

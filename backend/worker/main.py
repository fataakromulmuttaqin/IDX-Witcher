import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from core.config import get_settings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    cfg = get_settings()
    sched = BlockingScheduler(timezone=cfg.timezone)
    common = {"max_instances": 1, "coalesce": True, "misfire_grace_time": 3600}
    sched.add_job(
        lambda: None,
        CronTrigger(day_of_week="mon-fri", hour=cfg.pipeline_hour, minute=0),
        id="daily_pipeline",
        **common,
    )
    sched.start()


if __name__ == "__main__":
    main()

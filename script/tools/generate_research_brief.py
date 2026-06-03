import argparse
import logging

from src.config_loader import load_config
from src.research_brief import ResearchBriefGenerator, resolve_period


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Generate a weekly, monthly, or date-range Research Brief.")
    parser.add_argument(
        "--mode",
        choices=["week", "month", "range"],
        default="week",
        help="Default period type when no explicit --week/--month/date range is provided.",
    )
    parser.add_argument("--week", help="ISO week, for example 2026-W23.")
    parser.add_argument("--month", help="Month, for example 2026-06.")
    parser.add_argument("--from-date", dest="from_date", help="Range start date, YYYY-MM-DD.")
    parser.add_argument("--to-date", dest="to_date", help="Range end date, YYYY-MM-DD.")
    parser.add_argument("--last-days", type=int, help="Generate a rolling range ending at --date or today.")
    parser.add_argument("--date", dest="date_value", help="Anchor date for automatic week/month/range, YYYY-MM-DD.")
    parser.add_argument("--max-top", type=int, default=8, help="Maximum papers in the Top Papers table.")
    parser.add_argument("--max-questions", type=int, default=10, help="Maximum open questions to include.")
    args = parser.parse_args()

    start_date, end_date, period_label, brief_type = resolve_period(
        mode=args.mode,
        week=args.week,
        month=args.month,
        from_date=args.from_date,
        to_date=args.to_date,
        last_days=args.last_days,
        date_value=args.date_value,
    )
    config = load_config()
    generator = ResearchBriefGenerator(config)
    path = generator.generate(
        start_date=start_date,
        end_date=end_date,
        period_label=period_label,
        brief_type=brief_type,
        max_top=args.max_top,
        max_questions=args.max_questions,
    )
    logger.info("Research Brief written to %s", path)


if __name__ == "__main__":
    main()

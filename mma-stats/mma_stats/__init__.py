# fmt: off
from dagster import Definitions, load_assets_from_modules
from .jobs import ufc_athletes_update_job
from .schedules import ufc_athletes_update_schedule
from .assets import ufc_athletes
from .resources.clickhouse_resource import clickhouse_resource
from dotenv import load_dotenv
import os
load_dotenv()

clickhouse_resource_config = {
    "host": os.getenv("CLICKHOUSE_HOST"),
    "port": int(os.getenv("CLICKHOUSE_PORT")),
    "user": os.getenv("CLICKHOUSE_USER"),
    "password": os.getenv("CLICKHOUSE_PASSWORD"),
    "database": os.getenv("CLICKHOUSE_DATABASE"),
}

ufc_athletes_assets = load_assets_from_modules([ufc_athletes])

all_jobs = [ufc_athletes_update_job]
all_schedules = [ufc_athletes_update_schedule]

defs = Definitions(
    assets=[*ufc_athletes_assets],
    jobs=all_jobs,
    schedules=all_schedules,
    resources={
        "clickhouse": clickhouse_resource.configured(clickhouse_resource_config),
    }
)
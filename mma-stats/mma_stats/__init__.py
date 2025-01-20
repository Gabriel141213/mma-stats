# fmt: off
from dagster import Definitions, load_assets_from_modules
from .jobs import ufc_athletes_update_job
from .schedules import ufc_athletes_update_schedule
from .assets import ufc_athletes

ufc_athletes_assets = load_assets_from_modules([ufc_athletes])
all_jobs = [ufc_athletes_update_job]
all_schedules = [ufc_athletes_update_schedule]
defs = Definitions(
    assets=[*ufc_athletes_assets],
    jobs=all_jobs,
    schedules=all_schedules
)

from dagster import ScheduleDefinition
from ..jobs import ufc_athletes_update_job

ufc_athletes_update_schedule = ScheduleDefinition(
    job=ufc_athletes_update_job,
    cron_schedule="0 12 * * 0", # todos os domingos às 12:00
)
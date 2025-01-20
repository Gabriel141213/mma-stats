from dagster import AssetSelection, define_asset_job


ufc_athletes_update_job = define_asset_job(
    name="ufc_athletes_update_job",
    selection=AssetSelection.all()
)
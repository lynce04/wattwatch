from database.models.smard_data import SmardData
from app.provider.smard_main import get_latest_data

async def import_smard_data(filter_id,region,db):
    data = await get_latest_data(filter_id, region)
    series = data["series"]
    count = 0
    for item in series:
        timestamp,value = item

        if value is None:
            continue

        record =SmardData(filter_id=filter_id,region=region ,timestamp=timestamp,value=value)
        db.add(record)
        count += 1
    db.commit()

    return count
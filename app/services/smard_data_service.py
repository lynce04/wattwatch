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

def get_all_smard_data(db):
    return db.query(SmardData).all()

def get_all_filtered_smard_data(db,skip:int=0,limit:int=10,from_date:int=None,to_date:int=None):
    query=db.query(SmardData)

    if from_date:
        query = query.filter(SmardData.timestamp >= from_date)
    if to_date:
        query= query.filter(SmardData.timestamp <= to_date)

    query = query.offset(skip).limit(limit).all()
    return query

def get_smard_by_id(id,db):
    return db.query(SmardData).filter(SmardData.id == id).first()

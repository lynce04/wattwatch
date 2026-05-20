from fastapi import Depends ,HTTPException ,APIRouter,Query
from sqlalchemy.orm import Session
from database.session import get_db
from app.services.smard_data_service import import_smard_data ,get_smard_by_id,get_all_filtered_smard_data,get_all_smard_data
from datetime import datetime
from database.models.smard_data import SmardData

router = APIRouter(prefix="/api/smard" , tags=["SMARD"])

@router.post("/import")
async def import_data(filter_id: int, region: str,db= Depends(get_db)):
    result= await import_smard_data(filter_id,region,db)
    return  {"inserted_rows": result}
@router.get("/filter")
async def get_all_smards_with_filters(
    db=Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    from_date: str = Query(
        None,
        description="Format: YYYY-MM-DD",
        openapi_examples={
            "example": {
                "summary": "Start date",
                "value": "2026-01-01"
            }
        }
    ),
    to_date: str = Query(
        None,
        description="Format: YYYY-MM-DD",
        openapi_examples={
            "example": {
                "summary": "End date",
                "value": "2026-12-31"
            }
        }
    )
):
    from_ts = None
    to_ts = None

    if from_date:
        from_ts = int(datetime.strptime(from_date, "%Y-%m-%d").timestamp())
    if to_date:
        to_ts = int(datetime.strptime(to_date, "%Y-%m-%d").timestamp())

    return get_all_filtered_smard_data(db, skip, limit, from_ts, to_ts)
@router.get("/")
async def get_all_smards(db=Depends(get_db)):
    return get_all_smard_data(db)
@router.get("/{id}")
async def get_data_by_id(id: int, db= Depends(get_db)):
    result = get_smard_by_id(id,db)
    if result is None: raise HTTPException(status_code=404, detail="Smard data not found")
    return result


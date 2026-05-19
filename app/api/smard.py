from fastapi import APIRouter
from fastapi import Depends
from database.session import get_db
from app.services.smard_data_service import import_smard_data

router = APIRouter(prefix="/api/smard" , tags=["SMARD"])

@router.post("/import")
async def import_data(filter_id: int, region: str,db= Depends(get_db)):
    result= await import_smard_data(filter_id,region,db)
    return  {"inserted_rows": result}

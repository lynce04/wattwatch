from fastapi import Depends ,HTTPException ,APIRouter
from sqlalchemy.orm import Session
from database.session import get_db
from app.services.smard_data_service import import_smard_data , get_all_smard_data,get_smard_by_id

router = APIRouter(prefix="/api/smard" , tags=["SMARD"])

@router.post("/import")
async def import_data(filter_id: int, region: str,db= Depends(get_db)):
    result= await import_smard_data(filter_id,region,db)
    return  {"inserted_rows": result}
@router.get("/")
async  def get_all_smards(db = Depends(get_db),skip: int = 0,limit: int = 10 ,from_date:int =None,to_date:int =None):
     return get_all_smard_data(db, skip, limit, from_date,to_date)

@router.get("/{id}")
async def get_data_by_id(id: int, db= Depends(get_db)):
    result = get_smard_by_id(id,db)
    if result is None: raise HTTPException(status_code=404, detail="Smard data not found")
    return result

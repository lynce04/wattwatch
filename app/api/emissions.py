from fastapi import Depends, HTTPException,APIRouter
from database.session import get_db
from app.services.emission_service import get_emission_by_id,get_all_emissions,calculate_and_store_emission
from database.schemas.emission_schema import EmissionResponse
router = APIRouter(prefix="/api/emissions" , tags=["Emissions"])


@router.post("/calculate", response_model=EmissionResponse)
async def calculate_emissions(region: str, db=Depends(get_db)):
    result = await calculate_and_store_emission(region, db)
    if result is None:
        return {"error": "Not enough data from SMARD"}
    return result

@router.get("/", response_model=list[EmissionResponse])
async def get_emissions(db=Depends(get_db)):
    return get_all_emissions(db)

@router.get("/{id}", response_model=EmissionResponse)
async def get_emission_by_id_route(id: int, db=Depends(get_db)):
    result = get_emission_by_id(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result
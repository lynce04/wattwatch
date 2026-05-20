from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException,Query

from database.session import get_db
from app.services.simulation_service import create_simulation, get_all_simulations,get_simulation_by_id

router = APIRouter(prefix="/api/simulation" , tags=["Simulation"])

@router.post("/create")
async def create_simulation_route (
        name:str,
        description:str,
        scenario: str = Query(None, description="Options: high_wind, no_coal, high_gas, renewable_only"),
        start_date: str = Query(None, description="Format: YYYY-MM-DD"),
        end_date: str = Query(None, description="Format: YYYY-MM-DD"),
        db=Depends(get_db)):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    result = create_simulation(name, description, scenario, start, end, db)

    if result is None:
        raise HTTPException(status_code=400,
                            detail="Invalid scenario. Options: high_wind, no_coal, high_gas, renewable_only")

    return result

@router.get("/")
async def all_simulations(db=Depends(get_db)):
    return get_all_simulations(db)

@router.get("/{id}")
async def simulation_by_id(id:int,db=Depends(get_db)):
    result=  get_simulation_by_id(id,db)
    if result is None: raise HTTPException(status_code=404, detail="Simulation not found")
    return result
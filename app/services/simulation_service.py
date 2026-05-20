from datetime import datetime, timezone
from database.models.simulation import Simulations
from database.models.simulation_result import SimulationResult
from database.models.emission import Emission

# Scenario modifiers — each represents a what-if energy scenario
# The value is a multiplier applied to the current CO2 intensity
SCENARIO_MODIFIERS = {
    "high_wind":      0.7,   # 30% less CO2 — more wind energy
    "no_coal":        0.6,   # 40% less CO2 — coal removed
    "high_gas":       1.4,   # 40% more CO2 — gas dominates
    "renewable_only": 0.3,   # 70% less CO2 — only renewables
}

def create_simulation(name: str, description: str, scenario: str, start_date: datetime, end_date: datetime, db):
    # Step 1 — Validate scenario
    if scenario not in SCENARIO_MODIFIERS:
        return None

    # Step 2 — Create and save the simulation record
    simulation = Simulations(
        name=name,
        description=description,
        scenario=scenario,
        start_date=start_date,
        end_date=end_date
    )
    db.add(simulation)
    db.commit()
    db.refresh(simulation)

    # Step 3 — Get the most recent real CO2 intensity from emissions table
    latest_emission = db.query(Emission).order_by(Emission.timestamp.desc()).first()

    # Step 4 — If no emission data exists, we can't calculate
    if latest_emission is None:
        return simulation

    # Step 5 — Apply scenario modifier to get simulated CO2
    real_co2 = latest_emission.co2_intensity
    modifier = SCENARIO_MODIFIERS[scenario]
    simulated_co2 = round(real_co2 * modifier, 2)

    # Step 6 — Calculate difference and percentage change
    difference = round(simulated_co2 - real_co2, 2)
    percentage_change = round((difference / real_co2) * 100, 2)

    # Step 7 — Save simulation result
    result = SimulationResult(
        simulation_id=simulation.id,
        real_co2=real_co2,
        simulated_co2=simulated_co2,
        difference=difference,
        percentage_change=percentage_change
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return {"simulation": simulation, "result": result}


def get_all_simulations(db):
    return db.query(Simulations).all()


def get_simulation_by_id(id: int, db):
    return db.query(Simulations).filter(Simulations.id == id).first()
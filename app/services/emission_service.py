from datetime import datetime, timezone
from database.models.emission import Emission
from app.provider.smard_main import get_latest_data

# CO2 emission factors in grams per MWh
CO2_FACTORS = {
    "wind_onshore": 11,
    "wind_offshore": 11,
    "solar": 41,
    "hydro": 24,
    "biomass": 230,
    "nuclear": 12,
    "gas": 490,
    "hard_coal": 820,
    "brown_coal": 1050
}

# SMARD filter IDs for each energy source
SMARD_SOURCES = {
    "wind_onshore": 1223,
    "wind_offshore": 1228,
    "solar": 4066,
    "hydro": 1225,
    "biomass": 1224,
    "nuclear": 1226,
    "hard_coal": 4169,
    "brown_coal": 1227,
    "gas": 4071
}

async def calculate_and_store_emission(region: str, db):
    #  Fetch data for all sources and calculate averages
    averages = {}

    for source_name, filter_id in SMARD_SOURCES.items():
        # Fetch data for this source from SMARD
        data = await get_latest_data(filter_id, region)

        # Extract only valid (non-None) values
        values = [v for _, v in data["series"] if v is not None]

        # Only include this source if it has actual data
        if values:
            averages[source_name] = sum(values) / len(values)

    #  Safety check
    # If we got no data at all we can't calculate
    if not averages:
        return None

    #  Calculate total production across all sources
    total_production = sum(averages.values())

    # Apply weighted CO2 formula
    co2_intensity = sum(
        avg * CO2_FACTORS[source]
        for source, avg in averages.items()
    ) / total_production

    #  Get current timestamp
    timestamp = int(datetime.now(timezone.utc).timestamp())


    # Check if we already have a record for this timestamp
    existing = db.query(Emission).filter(
        Emission.timestamp == timestamp,
        Emission.region == region
    ).first()

    if existing:
        return existing  # return existing record, don't save duplicate

    #  Save to database
    emission = Emission(
        region=region,
        co2_intensity=round(co2_intensity, 2),
        timestamp=timestamp
    )
    db.add(emission)
    db.commit()
    db.refresh(emission)

    return emission


def get_all_emissions(db):
    return db.query(Emission).all()


def get_emission_by_id(id: int, db):
    return db.query(Emission).filter(Emission.id == id).first()
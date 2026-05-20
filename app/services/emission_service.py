from datetime import datetime, timezone
from database.models.emission import Emission
from app.provider.smard_main import get_latest_data

# CO2 emission factors in grams per kWh
# These are standard European average values
CO2_FACTORS = {
    "wind": 11,
    "gas": 490
}

async def calculate_and_store_emission(region: str, db):
    # fetch data for all three energy sources from SMARD
    wind_onshore_data = await get_latest_data(1223, region)
    wind_offshore_data = await get_latest_data(1228, region)
    gas_data = await get_latest_data(4071, region)

    # Extract valid values from each series
    # Remember series is a list of (timestamp, value) tuples
    # We filter out None values since some timestamps have no data
    wind_onshore_values = [v for _, v in wind_onshore_data["series"] if v is not None]
    wind_offshore_values = [v for _, v in wind_offshore_data["series"] if v is not None]
    gas_values = [v for _, v in gas_data["series"] if v is not None]

    # If any source has no valid data, we can't calculate
    if not wind_onshore_values or not wind_offshore_values or not gas_values:
        return None

    # Calculate average for each source
    avg_wind_onshore = sum(wind_onshore_values) / len(wind_onshore_values)
    avg_wind_offshore = sum(wind_offshore_values) / len(wind_offshore_values)
    avg_gas = sum(gas_values) / len(gas_values)

    # Apply CO2 intensity formula
    # Wind onshore + offshore combined
    wind_total = avg_wind_onshore + avg_wind_offshore
    # Total energy produced by all three sources
    total_production = wind_total + avg_gas

    # Weighted average CO2 intensity
    co2_intensity = (
        wind_total * CO2_FACTORS["wind"] +
        avg_gas * CO2_FACTORS["gas"]
    ) / total_production

    #  Get current timestamp in seconds
    timestamp = int(datetime.now(timezone.utc).timestamp())

    # Create and save the Emission record
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
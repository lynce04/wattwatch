import httpx
from datetime import datetime, UTC

BASE_URL = "https://www.smard.de/app/chart_data"


async def fetch_available_timestamps(filter_id: int, region: str, resolution: str) -> list[int]:
    # Build the index URL using the resolution
    # Example: /410/DE/index_hour.json
    url = f"{BASE_URL}/{filter_id}/{region}/index_{resolution}.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Return the list of timestamps or empty list if none found
        return data.get("timestamps", [])


async def fetch_timeseries(filter_id: int, region: str, resolution: str, timestamp: int):
    # Build the data URL — resolution comes BEFORE timestamp
    # Example: /410/DE/410_DE_hour_1609459200000.json
    url = f"{BASE_URL}/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # If SMARD returns 404 for this timestamp → no data available
            # Return empty list instead of crashing
            if exc.response.status_code == 404:
                return []
            raise

        series = response.json().get("series", [])

        # Convert raw data into clean (datetime, value) tuples
        normalized = []
        for ts_ms, value in series:
            # SMARD timestamps are in milliseconds → divide by 1000 for seconds
            dt = datetime.fromtimestamp(ts_ms / 1000, UTC)
            normalized.append((dt, value))

        return normalized


async def get_latest_data(filter_id: int, region: str):
    # Step 1 — Get all available timestamps for hourly resolution
    timestamps = await fetch_available_timestamps(filter_id, region, "hour")

    # Step 2 — Loop backwards (newest first) until we find real data
    for timestamp in reversed(timestamps):
        series = await fetch_timeseries(filter_id, region, "hour", timestamp)

        # Skip empty series or series with all None values
        valid = [item for item in series if item[1] is not None]

        if valid:
            # Return in a format the service expects
            return {"series": [(dt.timestamp(), value) for dt, value in series]}

    # Nothing found
    return {"series": []}
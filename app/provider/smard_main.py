import httpx

BASE_URL = "https://www.smard.de/app/chart_data"

async def get_latest_data(filter_id: int, region: str):
    #  Build and fetch the index URL
    index_url = f"{BASE_URL}/{filter_id}/{region}/index_quarterhour.json"

    async with httpx.AsyncClient() as client:
        # Fetch the index
        index_response = await client.get(index_url)
        index_response.raise_for_status()

        #  Extract timestamps and pick the most recent
        timestamps = index_response.json()["timestamps"]
        latest_timestamp = timestamps[-2]

        #  Build the data URL using the latest timestamp
        data_url = f"{BASE_URL}/{filter_id}/{region}/{filter_id}_{region}_{latest_timestamp}_quarterhour.json"

        #  Fetch the actual energy data
        data_response = await client.get(data_url)
        data_response.raise_for_status()

        # Return the raw data as a Python dictionary
        return data_response.json()
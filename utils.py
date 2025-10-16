import requests
import pandas as pd

def get_population_data(api_token, aoi):
    headers = {"Authorization": f"Bearer {api_token}"}
    url_pop = "https://api.tellusxdp.com/api/v1/datasets/population/v1/mesh"
    response = requests.post(url_pop, headers=headers, json={"aoi": aoi})
    data = response.json()["features"]
    df = pd.DataFrame(data)
    return df

def get_temperature_data(api_token, aoi):
    headers = {"Authorization": f"Bearer {api_token}"}
    url_temp = "https://api.tellusxdp.com/api/v1/datasets/temperature/v1/average"
    response = requests.post(url_temp, headers=headers, json={"aoi": aoi})
    data = response.json()["features"]
    df = pd.DataFrame(data)
    return df

def merge_data(pop_df, temp_df):
    merged = pop_df.merge(temp_df, on="mesh_id", how="inner")
    return merged

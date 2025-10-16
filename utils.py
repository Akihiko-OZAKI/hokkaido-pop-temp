import requests
import pandas as pd
import geopandas as gpd

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

def load_hokkaido_shapefile(shapefile_path="hokkaido_municipalities.shp"):
    """北海道市町村のシェイプファイルを読み込む"""
    gdf = gpd.read_file(shapefile_path)
    return gdf

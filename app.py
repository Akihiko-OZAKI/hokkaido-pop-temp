from flask import Flask, Response
import matplotlib.pyplot as plt
import io
import base64
from utils import get_population_data, get_temperature_data, merge_data, load_hokkaido_shapefile

app = Flask(__name__)

API_TOKEN = "bgGT4clbizBS7lj0128rhnwJ27SfFago"
AOI_HOKKAIDO = {
    "type": "Polygon",
    "coordinates": [[[139.0, 41.0], [139.0, 46.0], [146.0, 46.0], [146.0, 41.0], [139.0, 41.0]]]
}

@app.route("/")
def hello():
    return "Hello from Hokkaido Population-Temperature API!"

@app.route("/hokkaido-heatmap")
def hokkaido_heatmap():
    pop_df = get_population_data(API_TOKEN, AOI_HOKKAIDO)
    temp_df = get_temperature_data(API_TOKEN, AOI_HOKKAIDO)
    merged = merge_data(pop_df, temp_df)

    # シェイプファイル読み込み
    gdf = load_hokkaido_shapefile()
    # 人口密度×気温を gdf に結合（ここでは仮に人口密度を color 指標に）
    gdf = gdf.merge(merged, left_on="mesh_id", right_on="mesh_id", how="left")

    # プロット
    fig, ax = plt.subplots(figsize=(10,10))
    gdf.plot(column="population_density", cmap="coolwarm", legend=True, ax=ax, edgecolor='black')
    ax.set_title("Hokkaido Municipalities Population Density Heatmap")
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    html = f'<img src="data:image/png;base64,{img_base64}"/>'
    return Response(html, mimetype='text/html')

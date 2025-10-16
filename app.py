from flask import Flask, jsonify, Response
import matplotlib.pyplot as plt
import io
import base64
from utils import get_population_data, get_temperature_data, merge_data

app = Flask(__name__)

API_TOKEN = "bgGT4clbizBS7lj0128rhnwJ27SfFago"

# 北海道のAOI（Polygonで囲む）
AOI_HOKKAIDO = {
    "type": "Polygon",
    "coordinates": [[[139.0, 41.0], [139.0, 46.0], [146.0, 46.0], [146.0, 41.0], [139.0, 41.0]]]
}

@app.route("/")
def hello():
    return "Hello from Hokkaido Population-Temperature API!"

@app.route("/hokkaido-data")
def hokkaido_data():
    # データ取得
    pop_df = get_population_data(API_TOKEN, AOI_HOKKAIDO)
    temp_df = get_temperature_data(API_TOKEN, AOI_HOKKAIDO)
    merged = merge_data(pop_df, temp_df)
    return merged.to_json(orient="records")

@app.route("/hokkaido-plot")
def hokkaido_plot():
    pop_df = get_population_data(API_TOKEN, AOI_HOKKAIDO)
    temp_df = get_temperature_data(API_TOKEN, AOI_HOKKAIDO)
    merged = merge_data(pop_df, temp_df)

    # 散布図作成
    plt.figure(figsize=(8,6))
    plt.scatter(merged["temperature"], merged["population_density"], alpha=0.6)
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Population Density (persons/km²)")
    plt.title("Population Density vs Temperature in Hokkaido")

    # 画像をバイトに変換して返す
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    html = f'<img src="data:image/png;base64,{img_base64}"/>'
    return Response(html, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True)

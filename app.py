from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_TOKEN = "bgGT4clbizBS7lj0128rhnwJ27SfFago"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route("/")
def hello():
    return "Hello from Tellus API via Render!"

@app.route("/hokkaido-data")
def hokkaido_data():
    AOI = {
        "type": "Polygon",
        "coordinates": [[[139.0, 41.0], [139.0, 46.0], [146.0, 46.0], [146.0, 41.0], [139.0, 41.0]]]
    }

    # 人口データ取得例
    url_pop = "https://api.tellusxdp.com/api/v1/datasets/population/v1/mesh"
    response_pop = requests.post(url_pop, headers=HEADERS, json={"aoi": AOI})
    data = response_pop.json()
    return jsonify(data)

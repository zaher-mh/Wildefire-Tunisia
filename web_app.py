from flask import Flask, render_template
from create_geojson import construct_geojson
from collect_data_viirs import download_VIIRS_data
from multiprocessing import Process


app = Flask(__name__)

@app.route('/get-info')
def get_active_fire():
    return construct_geojson()

@app.route("/active-fires",methods=['GET'])
def get_info():
    return render_template("leaflet.html")


if __name__ == '__main__':
    p = Process(target=download_VIIRS_data, args=())
    p.start()
    app.run(debug=True, host='0.0.0.0', port=8090)
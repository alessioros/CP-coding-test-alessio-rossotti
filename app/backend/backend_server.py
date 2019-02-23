from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from utils.constants import SCRAPER_CONF, RECORD_HEADERS
from utils.database_utils import DatabaseUtils
from utils.web_scraper import FtpWebScraper
from utils import utils
import json

app = Flask(__name__)

@app.route("/get_ids", methods=['GET'])
@cross_origin(origin='0.0.0.0', headers=['Content- Type', 'Authorization'])
def get_ids():
    try:
        db_utils = DatabaseUtils()
        stations_ids = [s[0] for s in db_utils.get_stations_ids()]
        vars_names = [v[0] for v in db_utils.get_variables_names()]

        return json.dumps({"stationsIds": stations_ids, "varsNames": vars_names})

    except Exception as e:
        print(e)
    


@app.route("/download_files", methods=['GET'])
@cross_origin(origin='0.0.0.0', headers=['Content- Type', 'Authorization'])
def download_files():
    try:
        db_utils = DatabaseUtils()
        
        ftp = FtpWebScraper(SCRAPER_CONF, db_utils)

        num_files = ftp.download_time_series(remove_files=False, extract_zip=True)

        return json.dumps({"numFiles": num_files})

    except Exception as e:
        print(e)
        return 'problems while downloading file'

@app.route("/get_data/<string:station_id>/<string:variable_name>", methods=['GET'])
@cross_origin(origin='0.0.0.0', headers=['Content- Type', 'Authorization'])
def get_data(station_id, variable_name):
    try:
        db_utils = DatabaseUtils()
        records = [utils.format_record(v) for v in db_utils.get_data(station_id, variable_name)]

        return json.dumps({"records": records})

    except Exception as e:
        print(e)
        return 'problems while downloading file'
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
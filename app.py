import json
import requests
from simplexml import dumps
from random import choices
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

address_post_args = reqparse.RequestParser()
address_post_args.add_argument("address", type=str, help="Address is required", required=True)
address_post_args.add_argument("output_format", type=str, choices=['json','xml'], help="Output format is required(either json or xml)", required=True)

class GeoLocation(Resource):
    def post(self):
        args = address_post_args.parse_args()   # POST Arguments
        address = args['address']
        output_format = args['output_format']
        geocode_response = self.geo_coding_api(address) 

        if geocode_response['status'] == "OK":
            lat_n_lng = geocode_response['results'][0]['geometry']["location"]
            output_dict = {'coordinates' : lat_n_lng, 'address' : address}
        else:
            output_dict = geocode_response

        return self.output_data(output_dict, output_format)

    # function to return response based on the given output format
    def output_data(self, output_dict, format):
        if format.lower() == "xml":
            xml_dict = {'root':output_dict} #It will add root tag to XML response.
            response = make_response(dumps(xml_dict))   #Generate XML and make response
            response.headers["Content-Type"] = "application/xml"
        else:
            response = make_response(json.dumps(output_dict))   #Generate JSON string and make response
            response.headers["Content-Type"] = "application/json"

        return response

    # Google Geocode API Request
    def geo_coding_api(self, address):
        end_point = "https://maps.googleapis.com/maps/api/geocode/json"
        API_KEY = "YOUR-API-KEY" #Google Developer API
        args = {"address":address,"key":API_KEY}
        response = requests.get(end_point,params=args)  #get request to fetch address's geocoding
        return response.json()  #return response as JSON object

api.add_resource(GeoLocation, "/getAddressDetails")

if __name__ == "__main__":
    app.run(debug=True)
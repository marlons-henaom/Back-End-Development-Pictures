from . import app
from db import get_database
import os
import json
from bson import json_util
import requests
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

db = get_database("pictures")
picturesCollection = db["pictures"]

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    try:
        picturesCollection.drop()
        picturesCollection.insert_many(data)
        count = picturesCollection.count_documents({})
        return jsonify({"length": count}), 200
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        data= list(picturesCollection.find({}))
        return jsonify((parse_json(data))), 200
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        data = picturesCollection.find_one({"id": id}, {"_id": 0})
        if data:
            return jsonify((parse_json(data))), 200
        return {"Message": "Something went wrong!"}, 404
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        post_data = request.get_json()
        if post_data:
            song_id = post_data.get("id")
            data = picturesCollection.find_one({"id": song_id})
            if data:
                return {"Message": f"picture with id {song_id} already present"}, 302
            
            result = picturesCollection.insert_one(post_data)
            if result.acknowledged:
                return jsonify((parse_json(post_data))), 201
        
        return {"Message": "Something went wrong!"}, 404
    except requests.exceptions.RequestException as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    try:
        post_data = request.get_json()
        if post_data:
            result = picturesCollection.update_one({"id": id}, {"$set": post_data})
            if result.modified_count > 0:
                return jsonify((parse_json(post_data))), 200

        return {"Message": "Something went wrong!"}, 404
    except Exception as e:
        return {"Message": f"Request failed: {e}"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        result = picturesCollection.delete_one({"id": id})
        if result.deleted_count > 0:
            return "", 204

        return {"Message": "Something went wrong!"}, 404
    except Exception as e:
        return {"Message": f"Request failed: {e}"}, 500

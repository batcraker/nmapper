from flask import Blueprint, jsonify, request
from tools.Nmapper import Nmapper
import os
import uuid

api = Blueprint('api_nmapper', __name__)

# Api ROUTES
@api.route("/api/nmapper", methods=["POST"])
def __nmapper__():
    file = request.files['file']
    filename = file.filename
    name, ext = os.path.splitext(filename)
    file_hash = uuid.uuid4()
    file_name = str(file_hash) + ext

    file.save('./uploads/' + file_name)
    return jsonify({
        'message':'File uploaded successfull',
        'file_saved':file_name,
        'filename_original':filename
    })

@api.route("/api/nmapper/<filename>", methods=["GET"])
def _parser_(filename):
    nmapper = Nmapper(f'./uploads/{filename}')
    parsed_json = nmapper.parser_to_json()
    return jsonify(parsed_json)

@api.route("/api/<filename>", methods=["DELETE"])
def delete_file(filename):
    try:
        os.remove(f'./uploads/{filename}')
        return jsonify({'removed':True})
    
    except Exception as ex:
        return jsonify({'message':'Error has ocurred to delete file'})
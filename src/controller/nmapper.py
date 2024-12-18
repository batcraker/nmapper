from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, stream_with_context
from helpers.Nmapper import Nmapper
import os
import uuid


nmapper_bp = Blueprint('nmapper_bp', __name__, url_prefix='/nmapper')

# Get Routes
@nmapper_bp.route('/', methods=['GET'])
def index():
    files = []
    for file in os.listdir('./src/uploads'):
        if os.path.isfile(os.path.join('./src/uploads', file)):
            files.append(file)
    return render_template('home.html', files=files)



@nmapper_bp.route('/file/<filename>', methods=['GET'])
def nmapper(filename):
    nmapper = Nmapper(f'./src/uploads/{filename}')
    nmapper.parser_to_json()

    getWithOpenPorts = request.args.get('openPorts')
    getWithDomainName = request.args.get('domainNames')

    if getWithOpenPorts:
        nmapper.get_by_up_ports()
    if getWithDomainName:
        nmapper.get_by_hostname()
    if getWithOpenPorts and getWithDomainName:
        nmapper.get_by_up_ports_and_hostname()

    print(getWithOpenPorts)

    parsed_json = nmapper.get_data()

    return render_template('viewer.html', file=filename, data=parsed_json)


# Make word file
@nmapper_bp.route('/file/<filename>/word', methods=['GET'])
def make_word_file(filename):

    openPorts = request.args.get('openPorts')
    
    nmapper = Nmapper(f'./src/uploads/{filename}')
    nmapper.parser_to_json()
    if openPorts == 'true':
        nmapper.get_by_up_ports()

    nmapper.filter_with_open_ports()
    [content, filename_doc] = nmapper.get_word_doc()
    nmapper.remove_file(filename_doc)
    def generate():
        for chunk in content:
            yield chunk
    headers = {
        'Content-Disposition': f'attachment; filename={filename_doc}',
        'Location': url_for('nmapper_bp.index')
    }
    return stream_with_context(generate()), 200, headers
    

# Post Routes
@nmapper_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file:
        flash('No file selected', 'error')
        return redirect(url_for('nmapper_bp.index'))

    filename = file.filename
    name, ext = os.path.splitext(filename)
    file_hash = uuid.uuid4()
    file_name = f"{name}-{str(file_hash)}" + ext

    file.save('./src/uploads/' + file_name)
    flash('File uploaded successfully', 'success')
    return redirect(url_for('nmapper_bp.index', filename=file_name))





# Delete Routes
@nmapper_bp.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(f'./src/uploads/{filename}')
        flash('File deleted successfully', 'success')

    except Exception as ex:
        flash('File not found', 'error')
    
    finally:
        return jsonify({'message': 'File deleted successfully'})
        


import os
import uuid
from flask import Flask, request, jsonify, send_file
import pypandoc
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/convert', methods=['POST'])
def convert_text():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'output_format' not in data:
            return jsonify({'error': 'Missing required fields: text and output_format'}), 400
            
        text = data['text']
        output_format = data['output_format']
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.{output_format}"
        output_path = os.path.join(UPLOAD_FOLDER, filename)
        extra_args = []
        
        if output_format == 'pdf':
            extra_args = ['--pdf-engine=xelatex','-V','CJKmainfont=Noto Sans CJK SC']

        # Convert text using pandoc
        pypandoc.convert_text(
            text,
            output_format,
            format='markdown',
            outputfile=output_path,
            extra_args=extra_args
        )
        
        return jsonify({
            'message': 'File converted successfully',
            'filename': filename,
            'download_url': f'/download/{filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Secure the filename to prevent directory traversal
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        return send_file(
            file_path,
            as_attachment=True,
            download_name=safe_filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        # Secure the filename to prevent directory traversal
        safe_filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        # Check if file is within the uploads directory
        if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_FOLDER)):
            return jsonify({'error': 'Invalid file path'}), 400
            
        # Delete the file
        os.remove(file_path)
        
        return jsonify({
            'message': 'File deleted successfully',
            'filename': safe_filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
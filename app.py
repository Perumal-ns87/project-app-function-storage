from flask import Flask, request, redirect, url_for # type: ignore
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient # type: ignore

app = Flask(__name__)

# Azure Blob Storage Configuration
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=perustracct001;AccountKey=+lDGm+6T6lC6ZQZ6RzSdb36A9ihm+ZV7xokG+1ssi050UUmgh2PaQROc4mG8LE7ZybzYVI3ce9Oj+AStJoXKig==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "upload-files"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route('/')
def index():
    return '''
        <html><body>
            <h1>Upload File</h1>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
        </body></html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # Upload file to Azure Blob Storage
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file)

    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
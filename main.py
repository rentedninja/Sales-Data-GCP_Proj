import os
from flask import Flask, request, render_template
from google.cloud import storage

app = Flask(__name__)

# Configure the GCS bucket name
GCS_BUCKET_NAME = 'bkt_sales_1'

# Ensure the environment variable for the GCS service account key is set
service_account_path = 'E:\GCP\primeval-rune-425516-i3-dfef4e84c50d.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

# Explicitly specify your Google Cloud project ID
project_id = 'primeval-rune-425516-i3'

try:
    # Initialize the Google Cloud Storage client with the project ID
    storage_client = storage.Client(project=project_id)
except Exception as e:
    print(f"Error initializing Google Cloud Storage client: {e}")
    exit(1)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            try:
                # Upload the file to GCS
                bucket = storage_client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(file.filename)
                blob.upload_from_file(file.stream)
                return f'File {file.filename} uploaded to {GCS_BUCKET_NAME}.'
            except Exception as e:
                return f"Error uploading file: {e}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

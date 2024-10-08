from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Azure DevOps details
organization = 'ascendionava'
project = 'Azure-MLOps'
pipeline_id = 2
personal_access_token = os.getenv('AZURE_DEVOPS_PAT')
# The route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to trigger the pipeline
@app.route('/trigger_pipeline', methods=['POST'])
def trigger_pipeline():
    branch = request.form.get('branch', 'refs/heads/master')  # Default to 'master' if no branch is specified
    debug_mode = request.form.get('debug', 'false').lower() == 'true'

    url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs?api-version=6.0-preview.1"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "resources": {
            "repositories": {
                "self": {
                    "refName": branch  # Branch specified in the form
                }
            }
        },
        "variables": {
            "system.debug": debug_mode  # Debug mode based on form input
        },
        "pool": {
            "vmImage": "ubuntu-20.04"
        }
    }

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth('', personal_access_token), json=payload)

    if response.status_code == 200 or response.status_code == 201:
        return f"Pipeline triggered successfully! Status Code: {response.status_code}", 200
    else:
        return f"Failed to trigger pipeline. Status Code: {response.status_code}, Response: {response.text}", 500

if __name__ == '__main__':
    app.run(debug=True)

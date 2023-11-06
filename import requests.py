import requests
import json

def download_google_takeout():
    # Get the Google Takeout URL
    google_takeout_url = "https://takeout.google.com/"

    # Sign in to your Google account
    session = requests.Session()
    session.auth = (input("Enter your Google username: "), input("Enter your Google password: "))

    # Create a request to get all of your data
    request = session.get(f"{google_takeout_url}?all=1")

    # Check the response status code
    if request.status_code != 200:
        raise Exception("Failed to get all of your data: " + request.status_code)

    # Get the export ID
    content = json.loads(request.content)
    if "id" not in content:
        raise Exception("Failed to get export ID")
    
    export_id = content["id"]

    # Wait for the export to be ready
    while True:
        request = session.get(f"{google_takeout_url}/{export_id}")

        # Check the response status code
        if request.status_code != 200:
            raise Exception("Failed to get export status: " + request.status_code)

        # Check the export status
        export_status = json.loads(request.content)["status"]
        if export_status == "ready":
            break

        # Sleep for 10 seconds
        time.sleep(10)

    # Download the export
    request = session.get(f"{google_takeout_url}/{export_id}/download")

    # Save the export to a file
    with open("google_takeout.zip", "wb") as f:
        f.write(request.content)

if __name__ == "__main__":
    download_google_takeout()
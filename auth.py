
import requests

AUTH_URL = "https://api.devii.io/auth"

def get_access_token():
    """Retreive access token for the application"""

    # Create a dictionary to store the form data with your Devii credentials
    data = {
        "login": "<your Devii user name>",
        "password": "<your Devii Root role password>",
        "tenantid": "<your tenant ID>",
    }

    # Make the POST request to the Devii authentication endpoint with the provided data.
    response = requests.post(AUTH_URL, data=data)

    # Check for a successful response
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the access token
        access_token = json_response.get("access_token")
        if access_token:
            # uncomment the line below if you would like to test the retrival of the access token
            # print("this is your access token:", access_token)
            return access_token
        else:
            print("Access token not found in the response.")
    # If the response status code is not 200, it prints an error message along with the status code and the response text.
    else:
        print("Error:", response.status_code)
        print(response.text)

access_token = get_access_token()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
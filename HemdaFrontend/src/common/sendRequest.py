import requests
import json
# The URL of the API endpoint you want to get data from

def sendRequest(url, payload, requestType):
    url = 'http://127.0.0.1:8001/' + url

    # The data you would typically put in the body of a POST request,
    # but for a GET request, it goes into the URL as query parameters.

    data = None

    try:
        # Send the GET request with the 'params' argument
        if requestType == "get":
            response = requests.get(url, params=payload)
        if requestType == "post":
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload,headers=headers)
        # Raise an exception for bad status codes
        response.raise_for_status()

        print("GET request successful!")
        print("URL with query parameters:", response.url)
        if requestType == "get":
            data = json.loads(response.json())


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return data


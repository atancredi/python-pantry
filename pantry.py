import requests, json, os
import requests
from math import sqrt, pow


BASE_URL = "https://getpantry.cloud/apiv1/pantry/"
HEADERS = {"Content-Type": "application/json"}


class Utility:
    # Write json File
    def write_json(self, path, data):
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file)
        except TypeError:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(json.dumps(data), file)
        except Exception as e:
            print(f"Got Exception {e}.\nPlease report.")

    # Read json file
    def read_json(self, path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                return json.load(file)
        except Exception as e:
            print(f"Got Exception {e}.\nPlease report.")
            exit(0)

    def is_path(self, path):
        return os.path.exists(path)


class Pantry(Utility):
    def __init__(self, api_key=None) -> None:
        if api_key:
            self.api_key = api_key
        else:
            raise "Provide an API Key."

        self.get_account()

    def get_account(self):
        url = f"{BASE_URL}{self.api_key}"
        res = requests.get(url, headers=HEADERS)
        self.account = res.json()
        self.baskets = [x["name"] for x in self.account["baskets"]]

    def basket(self, basket=None, outputfile=None):
        self.outputfile = outputfile
        if basket:
            url = f"{BASE_URL}{self.api_key}/basket/{basket}"
            self.res = requests.get(url, headers=HEADERS)
            return self.check_response()

    def update(self, basket, data: dict, outputfile=None):
        self.outputfile = outputfile

        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")

        url = f"{BASE_URL}{self.api_key}/basket/{basket}"
        res = requests.put(url, headers=HEADERS, json=data)
        return res

    def create(self, basket):
        url = f"{BASE_URL}{self.api_key}/basket/{basket}"
        res = requests.post(url, headers=HEADERS)
        if res.status_code != 200:
            raise ConnectionError(res.text)

    def delete(self, basket=None):
        if basket:
            url = f"{BASE_URL}{self.api_key}/basket/{basket}"
            self.res = requests.delete(url, headers=HEADERS)
            return self.check_response()

    def check_response(self):
        data = None
        if self.res:
            try:
                data = self.res.json()
            except json.decoder.JSONDecodeError or TypeError:
                data = self.res.text

        if self.outputfile:
            self.write_json(path=self.outputfile, data=data)

        return data


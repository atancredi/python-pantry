import json, os
from requests import get, post, put, delete, Response
from dotenv import load_dotenv
from os import environ as env
from dataclasses import dataclass

BASE_URL = "https://getpantry.cloud/apiv1/pantry/"
HEADERS = {"Content-Type": "application/json"}


class Utility:
    res: Response
    outputfile: str

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

@dataclass
class PantryAccount:
    name: str
    description: str
    errors: list
    notifications: bool
    percentFull: float
    baskets: list

@dataclass
class Pantry(Utility):
    account: PantryAccount

    def __init__(self, api_key=None) -> None:
        if not api_key:
            # Get from .env
            load_dotenv()
            api_key = env.get("PANTRY_ID")
        
        self.api_key = api_key
        self.outputfile = None

        self.get_account()

    def get_account(self):
        """
        Delete basket
        :param basket<str>: basket id
        :return: text ('... was removed from your Pantry!')
        """
        url = f"{BASE_URL}{self.api_key}"
        self.res = get(url, headers=HEADERS)
        if self.res.status_code != 200:
            raise ConnectionError(self.res.text)
        self.account = PantryAccount(**self.res.json())
        # self.baskets = [x["name"] for x in self.account.baskets]

    def get_basket(self, basket: str = None, outputfile=None):
        """
        Delete basket
        :param basket<str>: basket id
        :return: text ('... was removed from your Pantry!')
        """
        self.outputfile = outputfile
        if basket:
            url = f"{BASE_URL}{self.api_key}/basket/{basket}"
            self.res = get(url, headers=HEADERS)
            if self.res.status_code != 200:
                raise ConnectionError(self.res.text)
            return self.check_response()
        
    def update(self, basket, data: dict, outputfile=None):
        """
        Delete basket
        :param basket<str>: basket id
        :return: text ('... was removed from your Pantry!')
        """
        self.outputfile = outputfile

        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")

        url = f"{BASE_URL}{self.api_key}/basket/{basket}"
        self.res = put(url, headers=HEADERS, json=data)
        if self.res.status_code != 200:
            raise ConnectionError(self.res.text)
        return self.check_response()

    def create_basket(self, basket: str):
        """
        Create a new basket
        :param basket<str>: basket id
        :return: text ('Your Pantry was updated with basket: ...')
        """
        url = f"{BASE_URL}{self.api_key}/basket/{basket}"
        self.res = post(url, headers=HEADERS)
        if self.res.status_code != 200:
            raise ConnectionError(self.res.text)
        self.account.baskets.append()
        return self.check_response()

    def delete(self, basket=None):
        """
        Delete basket
        :param basket<str>: basket id
        :return: text ('... was removed from your Pantry!')
        """
        if basket:
            url = f"{BASE_URL}{self.api_key}/basket/{basket}"
            self.res = delete(url, headers=HEADERS)
            if self.res.status_code != 200:
                raise ConnectionError(self.res.text)
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


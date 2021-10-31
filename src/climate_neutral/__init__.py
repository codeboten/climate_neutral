# Copyright 2019 codeboten
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import Optional
import urllib

import requests
from requests.auth import HTTPBasicAuth

_URL = "https://api.goclimateneutral.org/v1/flight_footprint"
# _URL = "http://localhost:8080"
CLASS_ECONOMY = "economy"


class Footprint:
    def __init__(self, tons):
        self.tons = tons


class Segment:
    def __init__(self, origin: str, destimation: str):
        self.origin = origin
        self.destination = destimation


class GoClimateNeutralAPI:
    def __init__(self, key: str, cabin_class: Optional[str] = CLASS_ECONOMY):
        self.key = key
        self.currencies = ["USD"]
        self.segments = []
        self.cabin_class = cabin_class

    def add_segment(self, segment):
        self.segments.append(segment)

    def add_currency(self, currency):
        self.currencies.append(currency)

    def send(self):
        """ Sends the requests to the API """
        segments = ""
        for index, segment in enumerate(self.segments, start=0):
            segments += "segments[{}][origin]={}&segments[{}][destination]={}".format(
                index, segment.origin, index, segment.destination
            )

        currencies = ""
        for currency in self.currencies:
            currencies += "currencies[]={}".format(currency)

        params = "{}&cabin_class={}&{}".format(segments, self.cabin_class, currencies)
##        params = "{}&cabin_class=economy&{}".format(segments, currencies)
        response = requests.get(
            _URL, params=params, auth=HTTPBasicAuth(self.key, None),
        )
        if not response:
            print("Error: [{}:{}]".format(response.status_code, response.text))
            return
        output = json.loads(response.text)
        # response
        return Footprint(output["footprint"] / 1000)

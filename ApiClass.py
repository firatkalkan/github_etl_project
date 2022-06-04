import requests
import json
from datetime import datetime, timedelta

class ApiClass:

    def __init__(self, userName, repoName, logging):

        self.url = "https://api.github.com/repos/" + userName + "/" + repoName + "/events"
        self.logging = logging

    # protected method
    def _getApiData(self):
        try:
            headers = {'Accept': 'application/vnd.github.v3+json'}
            response = requests.get(self.url, headers=headers)
            self.logging.info("REST API connection has been started")

            if response.status_code == 200:
                self.logging.info("REST API returns successfully, Status Code:" + str(response.status_code))
                return json.loads(response.text)
            else:
                self.logging.error("API STATUS CODE ISSUE: " + str(response.status_code))

        except:
            self.logging.error("some problem at _getApiData func")

    # public method
    def avaragePullReqTime(self):

        try:
            apiData = self._getApiData()
            pullReqType = "PullRequestEvent"

            totalPullReqCounter = 1     # starts 0 index
            totalPullReqTime = 0

            for response in apiData:
                if (response["type"] == pullReqType):

                    createdDate = datetime.strptime(response['payload']['pull_request']['created_at'], "%Y-%m-%dT%H:%M:%SZ")

                    if response['payload']['pull_request']['merged_at']:
                        mergedDate = datetime.strptime(response['payload']['pull_request']['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
                    else:
                        mergedDate = datetime.now()

                    delta = mergedDate - createdDate

                    totalPullReqCounter += 1
                    totalPullReqTime += (delta.total_seconds() / 60)   # as a minute

            self.logging.info("AVARAGE PULL REQUEST TIME: " + (str)(totalPullReqTime / totalPullReqCounter) + " MINUTES")
        except:
            self.logging.error("some problem at avaragePullReqTime func")

    # public method
    def totalGroupEvent(self, offset):

        try:
            apiData = self._getApiData()
            if offset and offset.isdigit():
                apiData = list(filter(lambda response: ((datetime.strptime(response['created_at'], "%Y-%m-%dT%H:%M:%SZ") > datetime.now() - timedelta(minutes=int(offset)))), apiData))
                self.logging.info("Api Data has been filtering for last " + str(offset) + " minutes")

            types = ["WatchEvent", "PullRequestEvent", "IssuesEvent"]
            groupType = {}
            for type in types:
                groupType[type] = 0
                for response in apiData:
                    if (response["type"] == type):
                        groupType[type] += 1
            self.logging.info("TOTAL EVENT NUMBER FOR EVENTS")
            self.logging.info(groupType)
        except:
            self.logging.error("some problem at totalGroupEvent func")


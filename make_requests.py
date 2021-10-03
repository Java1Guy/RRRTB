# importing the requests library
import datetime

import requests

from threading import Timer, Lock
import time

# api-endpoint
# [{"PLATE":4014,"CAT":"6th Grade Boys","NAME":"DYLAN ROYSTER","CLUB":"Gainesville Composite","START TIME":"14:16:22.5","FINISH TIME":"14:53:00.0","TIME":"36:37.50"},
BASE_URL = "https://api.raceresult.com/"


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class ResultsSubsystem:
    def __init__(self, event_id, api_key):
        self.url = BASE_URL + f'{event_id}/{api_key}'
        self.data = {}
        self.lock = Lock()
        self.timer: Timer = None

    def _read_results(self):
        # global data
        self.lock.acquire()
        # sending get request and saving the response as response object
        r = requests.get(url=self.url)
        # extracting data in json format
        self.data = r.json()
        self.last_read = datetime.datetime.now()
        self.lock.release()
        print('Updated...\n')

    def start_subsystem(self, interval):
        self.timer = RepeatTimer(interval, self._read_results)
        self.timer.start()
        print("Results reader started, reading every %d seconds" % interval)

    def stop_subsystem(self):
        self.timer.cancel()
        print("Result reader stopped")


def test_subsystem(rrss: ResultsSubsystem):
    time.sleep(5)
    for result in rrss.data:
        # printing the output
        print("Plate:%s\tCat:%s\tName:%s"
          % (result['PLATE'], result['CAT'], result['NAME']))
    time.sleep(5)
    for result in rrss.data:
        # printing the output
        print("Plate:%s\tCat:%s\tName:%s"
          % (result['PLATE'], result['CAT'], result['NAME']))
    time.sleep(5)
    for result in rrss.data:
        # printing the output
        print("Plate:%s\tCat:%s\tName:%s"
          % (result['PLATE'], result['CAT'], result['NAME']))


if __name__ == "__main__":
    rrss = ResultsSubsystem(169319, "WHAMSCNWEIK2PE6SV0YLP8AL2A3UV65I")
    rrss.start_subsystem(5)
    test_subsystem(rrss)
    rrss.stop_subsystem()

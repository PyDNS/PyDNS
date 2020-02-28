import glob
import os
import json
from pydns.utils import resources


class FileBackend:

    def __init__(self):
        self.path = os.path.join(resources.getWriteableResourcePath(), 'zones')
        self.zones = {}

        # Check if zones folder exists, if not, create it
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        zoneFiles = glob.glob('{0}/*.zone'.format(self.path))
        for zone in zoneFiles:
            with open(zone) as zonedata:
                data = json.load(zonedata)
                domain = data['domain']
                self.zones[domain] = data

    def getZones(self):
        return self.zones

    def getZone(self, domain):
        return self.zones[domain]

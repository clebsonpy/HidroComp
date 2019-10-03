from abc import ABCMeta
import xml.etree.ElementTree as ET
import requests

class ApiBiuld(metaclass=ABCMeta):

    def requests(self):
        response = requests.get(self.url, self.params)
        if not response:
            raise ConnectionError

        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        return root

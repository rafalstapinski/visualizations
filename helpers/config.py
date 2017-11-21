import os
import json

def xpath_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            elem = elem.get(x)
    except:
        pass

    return elem


class Config:

    @staticmethod
    def get(path):

        config = json.loads(os.environ['vis_config'])
        return xpath_get(config, path)

    @staticmethod
    def set():

        this = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(this, '../config/config.json'))
        os.environ['vis_config'] = f.read()
        f.close()

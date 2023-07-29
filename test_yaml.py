from pprint import pprint

import yaml

with open("prj.yaml", mode="r", encoding="utf-8") as yf:
    data = yaml.load(yf, Loader=yaml.Loader)

pprint(data)

from types import SimpleNamespace
import json
f = open("sizes.json", "r")
f = f.read()
x = json.loads(f, object_hook=lambda d: SimpleNamespace(**d))
robot = x.robot
bed = x.bed
del x
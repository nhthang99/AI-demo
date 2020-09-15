import os
import sys
PYTHON_PATH = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(PYTHON_PATH, '..')))
import json

f = open(os.path.join('streaming', 'info.json'), "r")
data = json.load(f)
IP = data['IP']
port = data['PORT']
camera_source = data['Video_Source']
if camera_source == '0':
    camera_source = 0
api = data['API']
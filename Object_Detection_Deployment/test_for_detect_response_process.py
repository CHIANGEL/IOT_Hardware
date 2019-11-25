import requests
from detect_response_process import *

def load_classes(path):
    """
    加载label信息
    """
    fp = open(path, "r")
    names = fp.read().split("\n")[:-1]
    return names

PyTorch_REST_API_URL = "http://127.0.0.1:32442/detect"

is_shaked = 0

response = requests.post(PyTorch_REST_API_URL).json()
            
print('Response process result: %d' % detect_response_process(is_shaked, response, 'chair'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import datetime
import json
def curtime():
    return datetime.datetime.now()
def uuid_v4():
    import uuid
    return str(uuid.uuid4())
    
def json_str_to_dict(json_str:str)->dict:
    return json.loads(json_str)

def dict_to_json_str(dict_obj:dict)->str:
    return json.dumps(dict_obj)

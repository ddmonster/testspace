import datetime

def curtime():
    return datetime.datetime.now()
def uuid_v4():
    import uuid
    return str(uuid.uuid4())
class message:
    command = None
    body = None
    file = None

def create(body=None, file=None):
    messageTo = message
    messageTo.body = body
    messageTo.file = file
    return messageTo

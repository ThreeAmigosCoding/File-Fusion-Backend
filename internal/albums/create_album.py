from internal.model.my_response import my_response

def create_album(event, context):
    return my_response(200, {"message": "works"})

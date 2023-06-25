from internal.model.my_response import my_response

def update_file(event, context):
    return my_response(200, {"message": "works"})
from internal.model.my_response import my_response

def get_all_user_albums(event, context):
    return my_response(200, {"message": "works"})
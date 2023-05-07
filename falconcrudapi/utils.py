import falcon.http_error
from falconcrudapi.models import User

#this method checks that the fields in the json body correspond to the fields needed - Name and Type. Anything else will throw an error.
def validate_json_fields(json_body):
    expected_json_keys = {"name", "type"}
    json_keys = set(json_body.keys())
    if expected_json_keys == json_keys:
        try:
            user_data = User(json_body["name"], json_body["type"])
            return user_data
        except:
            message = "Missing or misspelled user fields. Please make sure it is of the correct format. It should only include 2 fields: name and type."
            raise falcon.HTTPBadRequest(title='Bad request', description=message)
    else:
        message = "Unexpected fields found in the JSON body. Please make sure it is of the correct format. It should only include 2 fields: name and type"
        raise falcon.HTTPBadRequest(title="Bad Request", description= message)


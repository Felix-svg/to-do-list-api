from flask import make_response


def server_error(e):
    return make_response({"error": "Internal Server Error: " + str(e)}, 500)


def not_found(model_instance):
    return make_response({"error": f"{model_instance} not found"}, 404)


def missing_required_fields():
    return make_response({"error": "Missing required fields"}, 400)


def no_input():
    return make_response({"error": "No input data provided"}, 400)


def created(model_instance):
    return make_response({"message": f"{model_instance} created successfully"}, 201)


def updated(model_instance):
    return make_response({"message": f"{model_instance} updated successfully"}, 200)


def deleted(model_instance):
    return make_response({"message": f"{model_instance} deleted successfully"}, 200)

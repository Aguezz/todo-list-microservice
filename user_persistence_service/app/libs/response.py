from flask import jsonify

def success(message='', data=None):
    return jsonify(success=True, message=message, data=data)

def fail(message='', data=None):
    return jsonify(success=False, message=message, data=data)


INTERNAL_SERVER_ERROR = 'Internal server error.'
RECORD_NOT_FOUND = 'Record not found.'
MISSING_FIELD = 'Missing some field.'

UPDATED_SUCCESSFULLY = 'Data updated successfully'
DELETED_SUCCESSFULLY = 'Data deleted successfully'

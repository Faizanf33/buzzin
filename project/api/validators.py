import os
from email_validator import validate_email

from project.exceptions import APIError

TYPE_NAMES = {
    int: "integer", float: "float", bool: "boolean", str: "string", dict: "dict"
}

check_deliverability = os.getenv("CHECK_DELIVERABILITY")

def field_type_validator(request_data={}, field_types={}, prefix=""):
    """
    Validate given dict of fields and their types
    """
    cleaned_data = {}

    for field in field_types.keys():
        field_value = request_data.get(field)

        if field_value is not None:
            field_type = field_types[field]

            if field_type == float:
                try:
                    field_value = float(field_value)
                except Exception as e:
                    pass

            if type(field_value) != field_type:
                type_name = TYPE_NAMES.get(field_type, field_type.__name__)

                if prefix:
                    message = f"{prefix} {field} should be {type_name} value"
                else:
                    message = f"{field} should be {type_name} value"

                raise APIError(message)

        cleaned_data[field] = field_value

    return cleaned_data


def required_validator(request_data={}, required_fields=[], prefix=""):
    """
    Validate required fields of given dict of data
    """
    for field in required_fields:
        if request_data.get(field) in [None, ""]:

            if prefix:
                message = f"{prefix} {field} is required"
            else:
                message = f"{field} is required"

            raise APIError(message)

def email_validator(email:str):
    """
    Validate email
    """
    try:
        deliverability = bool(int(check_deliverability)) if check_deliverability else False

        valid = validate_email(email, check_deliverability=deliverability)
        email = valid.email

    except Exception as e:        
        raise APIError(f"Invalid email: {email}, {str(e)}")

''' User register, login error codes '''
INVALID_USER_INFO = 9903
INVALID_USER_PROFILE_INFO = 9904

G_EXCEPTION = 1111


def parse_exception(e: Exception, code: int) -> dict:
    err_str = ""
    if isinstance(e.args, tuple):
        for er in e.args:
            err_str = parse_dict(er)
    return get_error_dict(code, err_str)


def parse_dict(er):
    err_str = ""
    if isinstance(er, dict):
        for k, v in er.items():
            err_str += parse_dict(v)
            break
    if isinstance(er, list):
        for v in er:
            err_str += parse_dict(v)
            break
    if isinstance(er, str):
        err_str += er + " "
    return err_str


def get_error_dict(code, desc):
    return {"error_code": code, "error_desc": desc}

HTTP_BLOG_NOT_AVAILABLE = get_error_dict(9910, "No blogs created yet.")
HTTP_BLOGS_NOT_AVAILABLE = get_error_dict(9911, "Unable to find rest_auth you are looking for, you might have deleted this rest_auth.")
HTTP_BLOG_NOT_CREATED = get_error_dict(9912, "Problem in rest_auth creation")

# copyright 2009 David Ignacio <deignacio@gmail.com>

__all__ = [ "ApiVersionMiddleWare",
            "versioned_method",
            "run_versioned_func",
            "is_api_version",
            "get_api_version" ]

_DEFAULT_DEFAULT_VERSION = '0'

class ApiVersionMiddleware(object):
    """
    Ensures that all requests have an 'api_version' property set,
    regardless of the path actually requested.  This ensures that
    clients that existed even before api versions were introduced
    follow the convention, as well as removing the api_version
    kwarg so that all existing non-versioned request handlers could
    remain untouched.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_kwargs.has_key("api_version"):
            request.api_version = view_kwargs["api_version"]
            del view_kwargs["api_version"]
        else:
            request.api_version = '0'
        return None

def versioned_method(versions=None):
    """
    a parameterized request handler decorator to help simplify
    versioning api requests.  for clarifications, this is intended for versioning backwards
    incompatible requests from each other, not versioning all request changes.  the largest
    use case is so that if there are changes that involve simultaneous changes to the server
    and client.  the developer will want to version that request because we cannot guarantee
    that all clients will be updated.

    even though all request handlers can be versioned w/o this decorator, it's use
    allows for simpler tracking of versioned method changes.  it also lets others
    know that if they are changing this method, they should think about how that will
    impact the other existing versions.

    usage info:

    version_dict = { "1":_foo_handler_version_1,
                     "3":_foo_handler_version_3,
                     "3.1":_foo_handler_version_3_1,
                     "7":_foo_new_feature_something }

    @versioned_method(versions=version_dict)
    def foo(request, *args, **kwargs):
        raise new NotImplementedError("this request didn't exist then, how did you call it?")

    this defines a versioned method "foo."  if called w/a versioned api, the highest
    versioned handler >= that of the client's version is run.  if no version is supplied,
    the decorated function is called instead.

    example
    /foo -> foo is used.  this is used to show that a versioned function was introduced in
            version 1, so calling it w/an older client raises a NotImplementedError
    /v/1/foo/ -> _foo_handler_version_1 is used
    /v/2/foo/ -> _foo_handler_version_1 is used
    /v/3/foo/ -> _foo_handler_version_3 is used
    /v/3.1/foo/ -> _foo_handler_version_3_1 is used
    /v/5/foo/ -> _foo_handler_version_3_1 is used
    /v/7/foo/ -> _foo_handler_version_7 is used
    """
    if not versions:
        versions = {}
    def inner_versioned_func(func):
        if versions.has_key(_DEFAULT_DEFAULT_VERSION):
            raise Error("can't specify a version '0' function w/the decorator")
        versions[_DEFAULT_DEFAULT_VERSION] = func
        def actual_versioned_func(request, *args, **kwargs):
            client_version = get_api_version(request)
            api_version, handler = _get_versioned_func(versions, client_version,
                                                       _DEFAULT_DEFAULT_VERSION)
            response = handler(request, *args, **kwargs)
            return response
        return actual_versioned_func
    return inner_versioned_func

def _get_versioned_func(versions, desired_version, default_version):
    """
    fetches the appropriate version of a function.  if the desired version
    is lower than all specified versions, default_version is used.
    """
    if not versions.has_key(default_version):
        raise Error("default_version not present in versions dictionary")
    func = versions.get(desired_version)
    if func:
        return [desired_version, func]
    keys = versions.keys()
    keys.sort()
    key_to_return = -1
    for key in keys:
        if _version_cmp(desired_version, key):
            break
        else:
            key_to_return = key
    if key_to_return == -1:
        if default_function is not None:
            return [key_to_return, default_function]
        elif default_version is not None and versions.has_key(default_version):
            return [default_version, versions.get(default_version)]
        else:
            # this code should never be reached.
            raise Error("unreachable code.  default version presence alread checked")

    return [key_to_return, versions.get(key_to_return)]

def run_versioned_func(versions, request, default_version,
                       func_args, func_kwargs):
    """
    allows the specification of a versioned function, along with a default if the
    client's version is older than the first version provided.

    useful for making changes in which the difference from version to version involves
    entirely different logic or implementation, and there aren't any implied relationships
    between current and previous versions of the function.
    """
    client_version = get_api_version(request)
    api_version, func = _get_versioned_func(versions, client_version, default_version)
    func(*func_args, **func_kwargs)

def _version_cmp(v_a, v_b):
    if v_a.find(".") != -1:
        a_major, a_minor = map(int, v_a.split("."))
    else:
        a_major = int(v_a)
        a_minor = 0
    if v_b.find(".") != -1:
        b_major, b_minor = map(int, v_b.split("."))
    else:
        b_major = int(v_b)
        b_minor = 0
    if a_major == b_major:
        return a_minor <= b_minor
    else:
        return a_major <= b_major

def is_api_version(request, desired_version):
    """
    checks if the request was made by an appropriately versioned client

    useful for making a changes that are not backwards compatible w/earlier
    versions of the client.  a good example is any server change that also
    involves a corresponding change in the client.  this way, older clients
    will not see this version of the request.
    """
    val = _version_cmp(desired_version, get_api_version(request))
    return val

def get_api_version(request):
    """ returns the api version of the requesting client """
    return request.api_version

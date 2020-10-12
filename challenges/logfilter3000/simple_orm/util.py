import re

# shout outs to
# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def easy_decorator(decorator):
    def _wrap(*args, **kwargs):
        if not kwargs and len(args) == 1:
            return decorator(args[0])
        else:
            def __wrap(f):
                return decorator(f, *args, **kwargs)
            return __wrap
    return _wrap

import os
import sys


def get_env_var(name, required=True, cast_func=None, default=None):
    value = os.getenv(name, default)
    if required and not value:
        print(f"Error: Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    if cast_func and value is not None:
        try:
            value = cast_func(value)
        except Exception as e:
            print(
                f"Error: Could not cast {name} to required type: {e}", file=sys.stderr
            )
            sys.exit(1)
    return value

import sys, os
from variantbrowser import app

DOCKER_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)


# To funksjoner for aa sjekke om virtualenv er aktivert:
def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix


def in_docker():
    if DOCKER_KEY:
        return True
    else:
        return False


def main():

    if not in_virtualenv() and not in_docker():
        print("\n\n--Har du husket aa aktivere virtualenv--\n\n--source env/bin/activate--\n")
        exit()

    backendport = 5001
    ##
    if in_docker():
        from waitress import serve
        # Keep 0.0.0.0 in docker.
        serve(app, host='0.0.0.0', port=backendport)
    else:
        # For running not in docker:
        # Change IP, remember to have the same IP and port in frontend/src/config.js
        app.run(host='172.16.0.3', port=backendport, threaded=True, debug=True)


if __name__ == '__main__':
    main()
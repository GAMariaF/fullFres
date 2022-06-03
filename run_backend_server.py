import sys, os

SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

# To funksjoner for aa sjekke om virtualenv er aktivert:
def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

def in_docker():
    if SECRET_KEY:
        return True
    else:
        return False

if not in_virtualenv() or not in_docker():
    print("\n\n--Har du husket aa aktivere virtualenv--\n\n--source env/bin/activate--\n")
    exit()

from backend import app

if __name__ == '__main__':
    print( "in_virtualenv()")
    app.run(port=5000, threaded=True, debug=True)
    #app.run('172.16.0.3', port=5000, threaded=True, debug=True)
    

    

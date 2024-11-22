"""
Runner for Dan's Coffee Shop flask app

Inspired by werk.py written by Jim Eddy.
"""

import traceback

from coffee_shop import app

if __name__ == '__main__':

    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()

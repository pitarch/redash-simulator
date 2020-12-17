import os

from .api import api

if __name__ == "__main__":
    PORT = os.environ["REDASH_PORT"] or 5000
    api.run(host="0.0.0.0")

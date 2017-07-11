import common
import requests

PROTOCOL = "http"
HOST = common.SERVER_HOST
PORT = common.SERVER_PORT
path = "/hi"

uri = "{protocol}://{host}:{port}{path}".format(
    protocol=PROTOCOL,
    host=HOST,
    port=PORT,
    path=path
)

response = requests.get(uri)
print('{status_code}: {text}...'.format(
    status_code=response.status_code,
    text=response.text
))

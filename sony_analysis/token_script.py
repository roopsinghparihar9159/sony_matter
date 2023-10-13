from akamai.edgeauth import EdgeAuth, EdgeAuthError
import requests # just for this example

ET_HOSTNAME = 'edgeauth.akamaized.net'
ET_ENCRYPTION_KEY = 'YourEncryptionKey'
DEFAULT_WINDOW_SECONDS = 500 # seconds

et = EdgeAuth(**{'key': ET_ENCRYPTION_KEY,
                  'window_seconds': DEFAULT_WINDOW_SECONDS})
token = et.generate_url_token("/akamai/edgeauth")
url = "http://{0}{1}".format(ET_HOSTNAME, "/akamai/edgeauth")
response = requests.get(url, cookies={et.token_name: token})
print(response) # Maybe not 403

# 2) Query string
token = et.generate_url_token("/akamai/edgeauth")
url = "http://{0}{1}?{2}={3}".format(ET_HOSTNAME, "/akamai/edgeauth", et.token_name, token)
response = requests.get(url)
print(response)

# 1) Header using *
et = EdgeAuth(**{'key': ET_ENCRYPTION_KEY,
                  'window_seconds': DEFAULT_WINDOW_SECONDS})
token = et.generate_acl_token("/akamai/edgeauth/list/*")
url = "http://{0}{1}".format(ET_HOSTNAME, "/akamai/edgeauth/list/something")
response = requests.get(url, headers={et.token_name: token})
print(response)

# 2) Cookie Delimited by '!'
acl_path = ["/akamai/edgeauth", "/akamai/edgeauth/list/*"]
token = et.generate_acl_token(acl_path)
# url = "http://{0}{1}".format(ET_HOSTNAME, "/akamai/edgeauth")
url = "http://{0}{1}".format(ET_HOSTNAME, "/akamai/edgeauth/list/something2")
response = requests.get(url, cookies={et.token_name: token})
print(response)
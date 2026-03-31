import schemathesis
from requests.structures import CaseInsensitiveDict

print("Testing headers...")
headers = {"X-Security-Protection": "Active", "X-Security-protection": "Active", "x-security-protection": "Active"}
print("Exists directly?", "X-Security-Protection" in headers)

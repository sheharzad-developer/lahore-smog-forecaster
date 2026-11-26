import requests
from collect_data import BASE_URL, OPENAQ_API_KEY

SENSOR_ID = 13191315

url = f"{BASE_URL}/sensors/{SENSOR_ID}"

response = requests.get(
    url,
    headers={"X-API-Key": OPENAQ_API_KEY},
    timeout=30,
)

response.raise_for_status()

data = response.json()
sensor = data.get("results", {})

print("Johar Town sensor metadata:")
print(sensor)

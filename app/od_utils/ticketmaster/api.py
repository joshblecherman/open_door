import requests

API_KEY = "eKRil5sqCyPFlHFxHTB7ubR4avgMG1pI"
API_SECRET = "J0zAFpB9xDbb9o4Y"

PAGE_SIZE = 10
CITY = "New York City"

BASE_URL = "https://app.ticketmaster.com/discovery/v2"
EVENTS_URL = f"{BASE_URL}/events.json?"

NYC_EVENTS_URL = f"{EVENTS_URL}city={CITY}&size={PAGE_SIZE}&apikey={API_KEY}"


def get_ticketmaster_events_nyc():
    try:
        r = requests.get(NYC_EVENTS_URL)
    # catches any request-related exception
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    print(r.json())



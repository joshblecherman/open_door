import requests


def get_json(url: str, expected_status: int) -> dict:
    """
    :param url: target url for GET request
    :param expected_status: status code expected
    :return: json of the response object
    """
    try:
        r = requests.get(url)
    # catches any request-related exception
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    assert r.status_code == expected_status, \
        f"expected status {expected_status}, received status {r.status_code}"

    return r.json()

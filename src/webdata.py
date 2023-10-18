from pathlib import Path


class WebData():
    # user-agent so Google doesn't block the search
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36"
    }

    # valid recipe websites
    path = Path(__file__).resolve().parents[1] / "src" / "valid_websites.txt"
    with open(path, 'r') as f:
        valid_sites = [x for x in f.read().strip().splitlines()]

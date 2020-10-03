import requests

def get_avg_rank(username):
    url = f"http://api.whatpulse.org/user.php?user={username}&format=json"
    with requests.get(url) as r:
        json = r.json()
        ranks = json["Ranks"]
        keys = int(ranks["Keys"])
        clicks = int(ranks["Clicks"])
        download = int(ranks["Download"])
        upload = int(ranks["Upload"])
        uptime = int(ranks["Uptime"])
        return (keys + clicks + download + upload + uptime) / 5

if __name__ == "__main__":
    username = input("What is your WhatPulse username?\n>> ")
    avg = get_avg_rank(username)
    print(f"Your average ranking is: {avg}")
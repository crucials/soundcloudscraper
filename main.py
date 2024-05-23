import urllib.request
import regex
import json

limit = 1000


def clientid():
    agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
    headers = {"User-Agent": agent}
    req = urllib.request.Request("https://m.soundcloud.com", headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode()
    match = regex.search(r'"clientId":"([0-9a-zA-Z\-_]{32})",', html)
    if match:
        return match.group(1)
    else:
        print("unable to fetch")


def userid(artist, id):
    url = f"https://api-v2.soundcloud.com/resolve?url=https://soundcloud.com/{artist}&client_id={id}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        with open("export.txt", "a") as file:
            file.write(str(data))
            file.write("\n")
    return data["id"]


def getfollowerdata(userid, id):
    url = f"https://api-v2.soundcloud.com/users/{userid}/followers?client_id={id}&limit={limit}&offset=0&linked_partitioning=1"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        with open("export.txt", "a", encoding="utf-8") as file:
            for follower in data["collection"]:
                followerid = follower["urn"].split(":")[2]
                tracksurl = f"https://api-v2.soundcloud.com/users/{followerid}/tracks?limit={limit}&client_id={id}"
                tracksrequest = urllib.request.Request(tracksurl)
                with urllib.request.urlopen(tracksrequest) as tracks_response:
                    tracksdata = json.loads(tracks_response.read())
                    if tracksdata["collection"]:
                        for track in tracksdata["collection"]:
                            file.write(str(track))
                            file.write("\n")


id = clientid()
print(id)
artist = input("artist url: \n")
userid = userid(artist, id)
print(userid)
getfollowerdata(userid, id)

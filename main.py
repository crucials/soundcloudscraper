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


def getfollowersdata(userid,
                     id,
                     max_followers_depth: int,
                     current_followers_depth: int = 0,
                     username=None):
    if current_followers_depth > max_followers_depth:
        return

    print(f'getting followers of {username or userid}')

    url = f"https://api-v2.soundcloud.com/users/{userid}/followers?client_id={id}&limit={limit}&offset=0&linked_partitioning=1"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        with open("export.txt", "a", encoding="utf-8") as file:
            for follower in data["collection"]:
                followerid = follower["urn"].split(":")[2]
                follower_username = follower['username']
                print(f'follower of {userid}: {follower_username}')
                tracksurl = f"https://api-v2.soundcloud.com/users/{followerid}/tracks?limit={limit}&client_id={id}"
                tracksrequest = urllib.request.Request(tracksurl)
                with urllib.request.urlopen(tracksrequest) as tracks_response:
                    tracksdata = json.loads(tracks_response.read())
                    if tracksdata["collection"]:
                        for track in tracksdata["collection"]:
                            file.write(str(track))
                            file.write("\n")
                
                getfollowersdata(followerid, id, max_followers_depth,
                                 current_followers_depth + 1, username=follower['username'])


id = clientid()
print(id)
artist = input("artist url: \n")

try:
    followers_collecting_depth = input('\nhow deep to collect followers (1 - get followers '
                                       +'of followers, 2 - followers of followers of '
                                       + 'followers and so on) \npress enter to skip '
                                       + 'and collect only followers of target user:\n')
    if len(followers_collecting_depth.strip()) == 0:
        followers_collecting_depth = 0
    else:
        followers_collecting_depth = int(followers_collecting_depth)
    
    userid = userid(artist, id)
    print(userid)
    getfollowersdata(userid, id, int(followers_collecting_depth), username=artist)
except ValueError as error:
    print('entered value must be a number')

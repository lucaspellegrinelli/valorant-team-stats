import requests
from bs4 import BeautifulSoup

class MapData:
    def __init__(self, player, account, episode, act, mapname, winrate, wins, losses, kd, adr, acs, hs, aces, clutches, thrifty, flawless, plants, defuses):
        self.player = player
        self.account = account
        self.episode = episode
        self.act = act
        self.mapname = mapname
        self.winrate = winrate
        self.wins = wins
        self.losses = losses
        self.kd = kd
        self.adr = adr
        self.hs = hs
        self.aces = aces
        self.clutches = clutches
        self.thrifty = thrifty
        self.flawless = flawless
        self.plants = plants
        self.defuses = defuses

    def __repr__(self):
        return f"{self.name} - {self.wins}W {self.losses}L"

class StatsGrabber:
    SEASONS = {
        "4-3": "",
        "4-2": "?season=d929bc38-4ab6-7da4-94f0-ee84f8ac141e",
        "4-1": "?season=573f53ac-41a5-3a7d-d9ce-d6a6298e5704",
        "3-3": "?season=a16955a5-4ad0-f761-5e9e-389df1c892fb",
        "3-2": "?season=4cb622e1-4244-6da3-7276-8daaf1c01be2",
        "3-1": "?season=2a27e5d2-4d30-c9e2-b15a-93b8909a442c",
        "2-3": "?season=52e9749a-429b-7060-99fe-4595426a0cf7",
        "2-2": "?season=ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff",
        "2-1": "?season=97b6e739-44cc-ffa7-49ad-398ba502ceb0",
        "1-3": "?season=46ea6166-4573-1128-9cea-60a15640059b",
        "1-2": "?season=0530b9c4-4980-f2ee-df5d-09864cd00542",
        "1-1": "?season=3f61c772-4560-cd3f-5d3f-a7ab5abda6b3"
    }

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"

    def __init__(self, player, account, episode, act):
        self.player = player
        self.account = account
        self.episode = episode
        self.act = act
        self.season = episode * 3 + act

    def grab(self):
        resp = requests.get(
            url=self.build_url(),
            headers = {
                "Accept-Encoding": "identity",
                "User-Agent": StatsGrabber.USER_AGENT
            }
        )

        print("Status Code:", resp.status_code)

        req_html = resp.text
        soup = BeautifulSoup(req_html, "html.parser")

        output = []
        mydivs = soup.find_all("div", { "class": "st-content__item" })
        for div in mydivs:
            map_data = []
            info_div = div.find_all("div", { "class", "info" })
            for info in info_div:
                inhtml = info.find("div", { "class", "value" }).encode_contents().decode("ascii")
                map_data.append(inhtml)

            try:
                output.append(MapData(self.player, self.account, self.episode, self.act, *map_data))
            except:
                continue

        return output

    def build_url(self):
        uri_acc = self.account.replace("#", "%23")
        season_url = StatsGrabber.SEASONS[f"{self.episode}-{self.act}"]
        return f"https://tracker.gg/valorant/profile/riot/{uri_acc}/maps{season_url}"
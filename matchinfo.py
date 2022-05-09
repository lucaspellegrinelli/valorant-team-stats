class PlayerScore:
    def __init__(self, kda_str):
        parts = kda_str.split(" / ")
        self.kills = int(parts[0])
        self.deaths = int(parts[1])
        self.assists = int(parts[2])

class MatchInfo:
    def __init__(self, player, account, episode, act, result, rr, place, queue, score, mapname, kda_ratio, kda, kpr, adr, hs, avgscore, when):
        self.player = player
        self.account = account
        self.episode = episode
        self.act = act

        self.mapname = mapname
        self.agent = ""

        score_parts = score.split(" - ")
        self.rounds_won = int(score_parts[0])
        self.rounds_lost = int(score_parts[1])

        kda_parts = kda.split(" / ")
        self.kills = int(kda_parts[0])
        self.deaths = int(kda_parts[1])
        self.assists = int(kda_parts[2])

        self.kpr = float(kpr.split(" KPR")[0])
        self.adr = float(adr.split(" ADR")[0])
        self.hs = float(hs.split("% HS")[0]) / 100
        self.avgscore = float(avgscore.split(" Avg. Score")[0])

    def set_agent(self, agent):
        self.agent = agent

    def process_rr(self, rr):
        number = rr.split(" RR")[0]
        return 0 if number == "-" else int(number)

    def process_place(self, place):
        if place == "MVP":
            return 1
        else:
            return int("".join(s for s in place if s.isdigit() and len(s) > 0))
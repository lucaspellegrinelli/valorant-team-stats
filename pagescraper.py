import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from matchinfo import MatchInfo

class PageScraper:
    AGENT_IMAGE_CLASS = "profile_match-image"
    MATCHES_XPATH = "/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/div"
    ITEMS_PER_MATCH = 13

    def __init__(self, load_wait=10):
        self.load_wait = load_wait

    def scrap(self, player, acc_name, acc_tag, episode, act, queue="competitive"):
        # Open page in given URL
        driver = webdriver.Firefox()
        driver.get(f"https://blitz.gg/valorant/profile/{acc_name}-{acc_tag}?actName=e{episode}act{act}&queue={queue}")

        for _ in range(self.load_wait):
            time.sleep(1)
            try:
                elem = driver.find_element_by_tag_name("footer")
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            except:
                continue

        try:
            matches = driver.find_element(by=By.XPATH, value=PageScraper.MATCHES_XPATH)
        except:
            return []

        match_data = matches.text.split("\n")[:-3]

        match_infos = []
        for i in range(len(match_data) // PageScraper.ITEMS_PER_MATCH):
            s = i * PageScraper.ITEMS_PER_MATCH
            e = (i + 1) * PageScraper.ITEMS_PER_MATCH
            match_infos.append(MatchInfo(player, f"{acc_name}#{acc_tag}", episode, act, *match_data[s : e]))

        agent_images = driver.find_elements_by_class_name(PageScraper.AGENT_IMAGE_CLASS)
        for i, agent_image in enumerate(agent_images):
            style_txt = agent_image.get_attribute("style")
            agent = style_txt.split("matchtile/")[1].split("-art")[0]
            match_infos[i].set_agent(agent)

        driver.close()
        return match_infos
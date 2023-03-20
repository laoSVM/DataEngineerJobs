import argparse
import requests
from bs4 import BeautifulSoup


class CookSoup:

    def __init__(self, location="United States", profession="Data Engineer"):
        self.location = location
        self.profession = profession

    def web_scraper(self):
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={self.profession}&location={self.location}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        with open(
            f"Linkedin Source/{self.profession}_{self.location}.html",
            "w",
            encoding="utf8",
        ) as f:
            f.write(soup.prettify())
        return None


class CookJD:

    def __init__(self, job_url:str):
        self.job_url = job_url

    def web_scraper(self):
        try:
            response = requests.get(self.job_url, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        with open(
            "Linkedin Source/JD.html",
            "w",
            encoding="utf8",
        ) as f:
            f.write(soup.prettify())
        return None

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-l", "--location", type=str, required=False, default="United States"
    # )
    # parser.add_argument(
    #     "-p", "--profession", type=str, required=False, default="Data Engineer"
    # )
    # args = parser.parse_args()
    # location = args.location
    # profession = args.profession

    # CookSoup(location, profession).web_scraper()
    # CookJD("https://www.linkedin.com/jobs/view/data-engineer-analytics-generalist-at-instagram-3512575738?refId=HpFFHu9HC7MALi91WOQUxA%3D%3D&amp;trackingId=PfoygNQJ1tedgwoZZBbrdw%3D%3D&amp;position=2&amp;pageNum=0&amp;trk=public_jobs_jserp-result_search-card").web_scraper()
    # CookJD("https://www.linkedin.com/jobs/view/data-engineer-analytics-generalist-at-instagram-3512575738").web_scraper()

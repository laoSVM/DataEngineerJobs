from search_jobs import Scraper
import requests

if __name__ == '__main__':
    url = 'https://www.linkedin.com/jobs/view/data-analyst-at-indiana-university%E2%80%93purdue-university-indianapolis-3520089131'
    # try:
    #     response = requests.get(url, timeout=10)
    #     response.raise_for_status()
    # except requests.HTTPError as err:
    #     print(f"[!!] Something went wrong! {err}")
    # result = Scraper().jd_parsing(html = response.text)
    # print(result)
    Scraper().cook_soup(url, "Linkedin Source/JD_new_nohouzhui.html")
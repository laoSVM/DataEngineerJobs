import argparse
import re
import requests
from bs4 import BeautifulSoup
from random import randint
import time


# class Test:
#     def __init__(self, location="New York", profession="Data Engineer"):
#         self.location = location
#         self.profession = profession

#     def web_scraper_dep(self):
#         """从 base-search-card__info 获取基本信息, 但是Job ID 在上一个层级无法获取到"""
#         try:
#             response = requests.get(
#                 f"https://www.linkedin.com/jobs/search/?keywords={self.location}",
#                 timeout=10,
#             )
#             response.raise_for_status()
#         except requests.HTTPError as err:
#             print(f"[!!] Something went wrong! {err}")
#             return None
#         # create beautifulsoup
#         soup = BeautifulSoup(response.text, "html.parser")
#         result_list = []
#         for result in soup.find_all("div", {"class": "base-search-card__info"}):
#             result_dict = {}
#             result_dict["Job Title"] = result.find(
#                 "h3", {"class": "base-search-card__title"}
#             ).text.strip()
#             result_dict["Location"] = result.find(
#                 "span", {"class": "job-search-card__location"}
#             ).text.strip()
#             time_tag = result.find("time", {"class": "job-search-card__listdate"})
#             time_tag_new = result.find(
#                 "time", {"class": "job-search-card__listdate--new"}
#             )
#             if time_tag is not None:
#                 result_dict["Publish Date"] = time_tag["datetime"]
#             elif time_tag_new is not None:
#                 result_dict["Publish Date"] = time_tag_new["datetime"]
#             else:
#                 result_dict["Publish Date"] = None
#             result_list.append(result_dict)

#         for i in result_list[:5]:
#             print(i, "\n")

#         print("Job Finished")
#         return None

#     def web_scraper_dep_2(self):
#         try:
#             response = requests.get(
#                 f"https://www.linkedin.com/jobs/search/?keywords={self.location}",
#                 timeout=10,
#             )
#             response.raise_for_status()
#         except requests.HTTPError as err:
#             print(f"[!!] Something went wrong! {err}")
#             return None
#         # create beautifulsoup
#         soup = BeautifulSoup(response.text, "html.parser")
#         search_results = soup.find("ul", {"class": "jobs-search__results-list"})
#         result_list = []
#         for result in search_results.find_all("li"):
#             result_dict = {}
#             # RE match Job ID
#             url = result.find("a", {"class": "base-card__full-link"})["href"]
#             match = re.search(r"(\d+)\?", url)
#             # Check if there is a match
#             if match:
#                 # print(match.group(1)) # 3529282119
#                 result_dict["Job ID"] = match.group(1)
#             else:
#                 # Print an error message
#                 print("No match found")
#                 result_dict["Job ID"] = None

#             result_dict["Job Title"] = result.find(
#                 "h3", {"class": "base-search-card__title"}
#             ).text.strip()
#             result_dict["Location"] = result.find(
#                 "span", {"class": "job-search-card__location"}
#             ).text.strip()
#             time_tag = result.find("time", {"class": "job-search-card__listdate"})
#             time_tag_new = result.find(
#                 "time", {"class": "job-search-card__listdate--new"}
#             )
#             if time_tag is not None:
#                 result_dict["Publish Date"] = time_tag["datetime"]
#             elif time_tag_new is not None:
#                 result_dict["Publish Date"] = time_tag_new["datetime"]
#             else:
#                 result_dict["Publish Date"] = None
#             result_list.append(result_dict)

#         for i in result_list[:5]:
#             print(i, "\n")

#         print("Job Finished")
#         return None

#     def web_scraper(self):
#         try:
#             url = (
#                 f"https://www.linkedin.com/jobs/search/?keywords={self.profession}"
#                 + (f"&location={self.location}" if self.location else "")
#                 + f"&start={25*randint(0,5)}"
#             )
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()
#         except requests.HTTPError as err:
#             print(f"[!!] Something went wrong! {err}")
#             return None
#         # create beautifulsoup
#         soup = BeautifulSoup(response.text, "html.parser")
#         search_results = soup.find(
#             "ul", {"class": "jobs-search__results-list"}
#         )  # under <section class="two-pane-serp-page__results-list">

#         result_list = []
#         progress_bar = 0
#         for result in search_results.find_all("li"):
#             print(f"Searching jobs offset:{progress_bar}")
#             progress_bar += 1

#             result_dict = {}
#             # RE match Job ID
#             url = result.find("a", {"class": "base-card__full-link"})["href"]
#             job_description_dict = JdCrawler(url).web_scraper()  # get job description
#             time.sleep(randint(0, 5) * 0.1)
#             match = re.search(r"(\d+)\?", url)
#             # Check if there is a match
#             if match:
#                 # print(match.group(1)) # 3529282119
#                 result_dict["Job ID"] = match.group(1)
#             else:
#                 # Print an error message
#                 print("No match found")
#                 result_dict["Job ID"] = None
#             # Writing data to a dictionary
#             result_dict["Job Title"] = result.find(
#                 "h3", {"class": "base-search-card__title"}
#             ).text.strip()
#             result_dict["Company Name"] = result.find(
#                 "h4", {"class": "base-search-card__subtitle"}
#             ).text.strip()
#             result_dict["Location"] = result.find(
#                 "span", {"class": "job-search-card__location"}
#             ).text.strip()
#             # Salary
#             salary_info = result.find("span", {"class": "job-search-card__salary-info"})
#             result_dict["Salary"] = (
#                 re.sub(re.compile(r"\s+"), "", salary_info.text)
#                 if salary_info is not None
#                 else None
#             )
#             # Publish Date
#             time_tag = result.find("time", {"class": "job-search-card__listdate"})
#             time_tag_new = result.find(
#                 "time", {"class": "job-search-card__listdate--new"}
#             )
#             if time_tag is not None:
#                 result_dict["Publish Date"] = time_tag["datetime"]
#             elif time_tag_new is not None:
#                 result_dict["Publish Date"] = time_tag_new["datetime"]
#             else:
#                 result_dict["Publish Date"] = None

#             result_list.append(dict(result_dict, **job_description_dict))

#         for i in result_list[:5]:
#             print(i, "\n")

#         # with open("data.json", "w") as f:
#         #     json.dump(result_list, f)
#         print("Job Finished")
#         return None


class Scraper:
    """The base scraper for LinkedIn search results"""

    def __init__(self):
        pass

    def cook_soup(self, url: str, destination: str) -> None:
        """Save the source code of the webpage to a file"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
        soup = BeautifulSoup(response.text, "html.parser")

        with open(destination, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"Source code saved to {destination}")

    def search_results_parsing(self, html: str) -> list:
        """Parse search results from response.text | return a list of job info dict"""
        # create beautifulsoup
        soup = BeautifulSoup(html, "html.parser")

        result_list = []
        for result in soup.find_all("li"):
            result_dict = {}
            # RE match Job ID
            url = result.find("h3", {"class": "base-search-card__title"}).find_previous(
                "a"
            )["href"]
            match = re.search(r"(\d+)\?", url)
            # Check if there is a match
            if match:
                # print(match.group(1)) # 3529282119
                result_dict["Job ID"] = match.group(1)
                result_dict["Job URL"] = url
            else:
                # Print an error message
                print("No match found")
                result_dict["Job ID"] = None
                result_dict["Job URL"] = None
            # Writing data to a dictionary
            result_dict["Job Title"] = result.find(
                "h3", {"class": "base-search-card__title"}
            ).text.strip()
            result_dict["Company Name"] = result.find(
                "h4", {"class": "base-search-card__subtitle"}
            ).text.strip()
            result_dict["Location"] = result.find(
                "span", {"class": "job-search-card__location"}
            ).text.strip()
            # Salary
            salary_info = result.find("span", {"class": "job-search-card__salary-info"})
            result_dict["Salary"] = (
                re.sub(re.compile(r"\s+"), "", salary_info.text)
                if salary_info is not None
                else None
            )
            # Publish Date
            time_tag = result.find("time", {"class": "job-search-card__listdate"})
            time_tag_new = result.find(
                "time", {"class": "job-search-card__listdate--new"}
            )
            if time_tag is not None:
                result_dict["Publish Date"] = time_tag["datetime"]
            elif time_tag_new is not None:
                result_dict["Publish Date"] = time_tag_new["datetime"]
            else:
                result_dict["Publish Date"] = None

            result_list.append(result_dict)

        return result_list

    def jd_parsing(self, html: str) -> dict:
        """
        Parse the jd page from response.text, and return a jd dict
        {
            "Seniority level": value,
            "Employment type": Full-time,
            "Job function": IT,
            "Industries": "Technology, Information and Internet"
        }
        """
        soup = BeautifulSoup(html, "html.parser")

        job_description = soup.find("div", {"class": "description__text"}).text.strip()
        criteria_list = soup.find("ul", {"class": "description__job-criteria-list"})

        result_dict = {}
        for criteria in criteria_list.find_all("li"):
            subheader = criteria.find(
                "h3", {"class": "description__job-criteria-subheader"}
            ).text.strip().lower()
            value = criteria.find(
                "span", {"class": "description__job-criteria-text"}
            ).text.strip()
            result_dict[subheader] = value
        result_dict["job description"] = job_description[: job_description.find("\n")]
        return result_dict

    def jd_json(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("script").attrs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        required=False,
        default="New York",
        help='Job search location. (e.g "New York")',
    )
    parser.add_argument(
        "-p",
        "--profession",
        type=str,
        required=False,
        default="Data Engineer",
        help='Job Title. (e.g "Data Engineer")',
    )
    args = parser.parse_args()
    location = args.location
    profession = args.profession
    print(f"Searching for: Location: {location}, Profession: {profession}")

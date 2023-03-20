import csv
import os
import argparse
import re
import json
import requests
import colorama
from bs4 import BeautifulSoup
from random import randint
import time
import read_data


class Test:
    def __init__(self, location="New York", profession="Data Engineer"):
        self.location = location
        self.profession = profession

    def web_scraper_dep(self):
        """从 base-search-card__info 获取基本信息, 但是Job ID 在上一个层级无法获取到"""
        try:
            response = requests.get(
                f"https://www.linkedin.com/jobs/search/?keywords={self.location}",
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        result_list = []
        for result in soup.find_all("div", {"class": "base-search-card__info"}):
            result_dict = {}
            result_dict["Job Title"] = result.find(
                "h3", {"class": "base-search-card__title"}
            ).text.strip()
            result_dict["Location"] = result.find(
                "span", {"class": "job-search-card__location"}
            ).text.strip()
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

        for i in result_list[:5]:
            print(i, "\n")

        print("Job Finished")
        return None

    def web_scraper_dep_2(self):
        try:
            response = requests.get(
                f"https://www.linkedin.com/jobs/search/?keywords={self.location}",
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find("ul", {"class": "jobs-search__results-list"})
        result_list = []
        for result in search_results.find_all("li"):
            result_dict = {}
            # RE match Job ID
            url = result.find("a", {"class": "base-card__full-link"})["href"]
            match = re.search(r"(\d+)\?", url)
            # Check if there is a match
            if match:
                # print(match.group(1)) # 3529282119
                result_dict["Job ID"] = match.group(1)
            else:
                # Print an error message
                print("No match found")
                result_dict["Job ID"] = None

            result_dict["Job Title"] = result.find(
                "h3", {"class": "base-search-card__title"}
            ).text.strip()
            result_dict["Location"] = result.find(
                "span", {"class": "job-search-card__location"}
            ).text.strip()
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

        for i in result_list[:5]:
            print(i, "\n")

        print("Job Finished")
        return None

    def web_scraper(self):
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={self.profession}&location={self.location}&start={25*randint(0,5)}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find(
            "ul", {"class": "jobs-search__results-list"}
        )  # under <section class="two-pane-serp-page__results-list">
        result_list = []
        progress_bar = 0
        for result in search_results.find_all("li"):
            print(f"Searching jobs offset:{progress_bar}")
            progress_bar += 1

            result_dict = {}
            # RE match Job ID
            url = result.find("a", {"class": "base-card__full-link"})["href"]
            job_description_dict = JdCrawler(url).web_scraper()  # get job description
            time.sleep(randint(0, 3))
            match = re.search(r"(\d+)\?", url)
            # Check if there is a match
            if match:
                # print(match.group(1)) # 3529282119
                result_dict["Job ID"] = match.group(1)
            else:
                # Print an error message
                print("No match found")
                result_dict["Job ID"] = None
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

            result_list.append(dict(result_dict, **job_description_dict))

        for i in result_list[:5]:
            print(i, "\n")

        with open("data.json", "w") as f:
            json.dump(result_list, f)
        print("Job Finished")
        return None


class JdCrawler:
    def __init__(self, job_url: str):
        self.job_url = job_url

    def web_scraper(self) -> dict:
        if self.job_url is None:
            return {"Job Description": None}
        try:
            response = requests.get(self.job_url, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, "html.parser")
        job_description = soup.find("div", {"class": "description__text"}).text.strip()
        criteria_list = soup.find("ul", {"class": "description__job-criteria-list"})

        result_dict = {}
        for criteria in criteria_list.find_all("li"):
            subheader = criteria.find(
                "h3", {"class": "description__job-criteria-subheader"}
            ).text.strip()
            value = criteria.find(
                "span", {"class": "description__job-criteria-text"}
            ).text.strip()
            result_dict[subheader] = value
        result_dict["job_description"] = job_description[: job_description.find("\n")]
        return result_dict


class Scrape_Place:
    def __init__(self, location):
        self.location = location

    def web_parsing_location(self):
        try:
            response = requests.get(
                f"https://www.linkedin.com/jobs/search/?keywords={self.location}",
                # f'https://www.linkedin.com/jobs/jobs-in-{self.location}?trk=homepage-basic_intent-module-jobs&position=1&pageNum=0',
                timeout=10,
            )
            response.raise_for_status()

            # create beautifulsoup
            soup = BeautifulSoup(response.text, "html.parser")

            return extract_job_links(soup)
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong! {err}")


class Scrape_Profession:
    def __init__(self, profession, city):
        self.profession = profession
        self.city = city

    def profession_current_location(self):
        try:
            req = requests.get(
                f"https://www.linkedin.com/jobs/search?keywords={self.profession}&location={self.city}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
            )
            req.raise_for_status()

            # create Soup
            page_soup = soup(req.text, "html.parser")
            return extract_job_links(page_soup)
        except requests.HTTPError as err:
            print(
                colorama.Fore.RED,
                f"[!!] Something went wrong! {err}",
                colorama.Style.RESET_ALL,
            )


class Profession_Location:
    def __init__(self, profession, place):
        self.profession = profession
        self.place = place

    def profession_location(self):
        try:
            req = requests.get(
                f"https://www.linkedin.com/jobs/search?keywords={self.profession}&location={self.place}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
            )
            req.raise_for_status()

            # create Soup
            page_soup = soup(req.text, "html.parser")
            return extract_job_links(page_soup)
        except requests.HTTPError as err:
            print(
                colorama.Fore.RED,
                f"[!!] Something went wrong! {err}",
                colorama.Style.RESET_ALL,
            )


def scrape_write(links):
    try:
        if "-" in job:
            formatting = [x.capitalize() for x in job.split("-")]
            my_job = " ".join(formatting)
        else:
            my_job = job.capitalize()

        print(
            colorama.Fore.YELLOW,
            f"[!] There are {len(links)} available {my_job} jobs in {place.capitalize()}.\n",
            colorama.Style.RESET_ALL,
        )

        csv_filename = f"jobs_in_{place}.csv"
        with open(os.path.join(folder_name, csv_filename), "w", encoding="utf-8") as f:
            headers = [
                "Source",
                "Organization",
                "Job Title",
                "Location",
                "Posted",
                "Applicants Hired",
                "Seniority Level",
                "Employment Type",
                "Job Function",
                "Industries",
            ]
            write = csv.writer(f, dialect="excel")
            write.writerow(headers)

            for job_link in links:
                page_req = requests.get(job_link)
                page_req.raise_for_status()

                # Parse HTML
                job_soup = soup(page_req.text, "html.parser")
                my_data = [job_link]

                # Topcard scraping
                for content in job_soup.findAll(
                    "div", {"class": "topcard__content-left"}
                )[0:]:
                    # Scraping Organization Names
                    orgs = {
                        "Default-Org": [
                            org.text
                            for org in content.findAll(
                                "a",
                                {
                                    "class": "topcard__org-name-link topcard__flavor--black-link"
                                },
                            )
                        ],
                        "Flavor-Org": [
                            org.text
                            for org in content.findAll(
                                "span", {"class": "topcard__flavor"}
                            )
                        ],
                    }

                    if orgs["Default-Org"] == []:
                        org = orgs["Flavor-Org"][0]
                        my_data.append(org)
                    else:
                        for org in orgs["Default-Org"]:
                            my_data.append(org)

                    # Scraping Job Title
                    for title in content.findAll("h1", {"class": "topcard__title"})[0:]:
                        print(
                            colorama.Fore.GREEN,
                            f"[*] {title.text}",
                            colorama.Style.RESET_ALL,
                            colorama.Fore.YELLOW,
                            f"- {org}",
                            colorama.Style.RESET_ALL,
                        )
                        my_data.append(title.text.replace(",", "."))

                    for location in content.findAll(
                        "span", {"class": "topcard__flavor topcard__flavor--bullet"}
                    )[0:]:
                        my_data.append(location.text.replace(",", "."))

                    # Scraping Job Time Posted
                    posts = {
                        "Old": [
                            posted.text
                            for posted in content.findAll(
                                "span",
                                {
                                    "class": "topcard__flavor--metadata posted-time-ago__text"
                                },
                            )
                        ],
                        "New": [
                            posted.text
                            for posted in content.findAll(
                                "span",
                                {
                                    "class": "topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new"
                                },
                            )
                        ],
                    }

                    if posts["New"] == []:
                        for text in posts["Old"]:
                            my_data.append(text)
                    else:
                        for text in posts["New"]:
                            my_data.append(text)

                    # Scraping Number of Applicants Hired
                    applicants = {
                        "More-Than": [
                            applicant.text
                            for applicant in content.findAll(
                                "figcaption", {"class": "num-applicants__caption"}
                            )
                        ],
                        "Current": [
                            applicant.text
                            for applicant in content.findAll(
                                "span",
                                {
                                    "class": "topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption"
                                },
                            )
                        ],
                    }

                    if applicants["Current"] == []:
                        for applicant in applicants["More-Than"]:
                            my_data.append(f"{get_nums(applicant)}+ Applicants")
                    else:
                        for applicant in applicants["Current"]:
                            my_data.append(f"{get_nums(applicant)} Applicants")

                # Criteria scraping
                for criteria in job_soup.findAll(
                    "span", {"class": "job-criteria__text job-criteria__text--criteria"}
                )[:4]:
                    my_data.append(criteria.text)

                write.writerows([my_data])

            print(
                colorama.Fore.YELLOW,
                f"\n\n[!] Written all information in: {csv_filename}",
                colorama.Style.RESET_ALL,
            )
        # Reads scraped data
        read_data.read_scraped(folder_name, csv_filename)
    except requests.HTTPError as err:
        print(
            colorama.Fore.RED,
            f"[!!] Something went wrong! {err}",
            colorama.Style.RESET_ALL,
        )


def get_nums(string):
    a_list = string.split()
    for num in a_list:
        if num.isdigit():
            return num


def extract_job_links(cursor):
    print("Extracting job links")
    job_links = []

    for res_card in cursor.findAll("ul", {"class": "scaffold-layout__list-container"}):
        print(res_card)
        job_links.append(res_card)

    return job_links
    # return scrape_write(job_links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--location", type=str, required=False, default="New York"
    )
    parser.add_argument(
        "-p", "--profession", type=str, required=False, default="Data Engineer"
    )
    args = parser.parse_args()
    location = args.location
    profession = args.profession
    print(f"Searching for: Location: {location}, Profession: {profession}")

    Test(location, profession).web_scraper()

    # JdCrawler(
    #     "https://www.linkedin.com/jobs/view/data-engineer-analytics-generalist-at-instagram-3512575738"
    # ).web_scraper()

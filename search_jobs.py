import csv
import os
import argparse
import json
import re
import requests
import colorama
from bs4 import BeautifulSoup
import read_data

class Test:

    def __init__(self, location):
        self.location = location

    def web_scraper_dep(self):
        """从 base-search-card__info 获取基本信息, 但是Job ID 在上一个层级无法获取到"""
        try:
            response = requests.get(
                f'https://www.linkedin.com/jobs/search/?keywords={self.location}',
                timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f'[!!] Something went wrong! {err}')
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, 'html.parser')
        result_list = []
        for result in soup.find_all('div', {'class': 'base-search-card__info'}):
            result_dict = {}
            result_dict["Job Title"] = result.find('h3', {'class': 'base-search-card__title'}).text.strip()
            result_dict["Location"] = result.find('span', {'class': 'job-search-card__location'}).text.strip()
            time_tag = result.find('time', {'class': 'job-search-card__listdate'})
            time_tag_new = result.find('time', {'class': 'job-search-card__listdate--new'})
            if time_tag is not None:
                result_dict["Publish Date"] = time_tag["datetime"]
            elif time_tag_new is not None:
                result_dict["Publish Date"] = time_tag_new["datetime"]
            else:
                result_dict["Publish Date"] = None
            result_list.append(result_dict)

        for i in result_list[:5]:
            print(i,"\n")

        print("Job Finished")
        return None

    def web_scraper(self):
        try:
            response = requests.get(
                f'https://www.linkedin.com/jobs/search/?keywords={self.location}',
                timeout=10)
            response.raise_for_status()
        except requests.HTTPError as err:
            print(f'[!!] Something went wrong! {err}')
            return None
        # create beautifulsoup
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find('ul', {'class': 'jobs-search__results-list'})
        result_list = []
        for result in search_results.find_all('li'):
            result_dict = {}
            # RE match Job ID
            url = result.find('a', {'class': 'base-card__full-link'})["href"]
            match = re.search(r"(\d+)\?", url)
            # Check if there is a match
            if match:
                # print(match.group(1)) # 3529282119
                result_dict["Job ID"] = match.group(1)
            else:
                # Print an error message
                print("No match found")
                result_dict["Job ID"] = None
            
            result_dict["Job Title"] = result.find('h3', {'class': 'base-search-card__title'}).text.strip()
            result_dict["Location"] = result.find('span', {'class': 'job-search-card__location'}).text.strip()
            time_tag = result.find('time', {'class': 'job-search-card__listdate'})
            time_tag_new = result.find('time', {'class': 'job-search-card__listdate--new'})
            if time_tag is not None:
                result_dict["Publish Date"] = time_tag["datetime"]
            elif time_tag_new is not None:
                result_dict["Publish Date"] = time_tag_new["datetime"]
            else:
                result_dict["Publish Date"] = None
            result_list.append(result_dict)

        for i in result_list[:5]:
            print(i,"\n")

        print("Job Finished")
        return None

class Scrape_Place:

    def __init__(self, location):
        self.location = location


    def web_parsing_location(self):
        try:
            response = requests.get(
                f'https://www.linkedin.com/jobs/search/?keywords={self.location}',
                # f'https://www.linkedin.com/jobs/jobs-in-{self.location}?trk=homepage-basic_intent-module-jobs&position=1&pageNum=0',
                timeout=10)
            response.raise_for_status()

            # create beautifulsoup
            soup = BeautifulSoup(response.text, 'html.parser')

            return extract_job_links(soup)
        except requests.HTTPError as err:
            print(f'[!!] Something went wrong! {err}')



class Scrape_Profession:

    def __init__(self, profession, city):
        self.profession = profession
        self.city = city
        

    def profession_current_location(self):
        try:
            req = requests.get(
                f'https://www.linkedin.com/jobs/search?keywords={self.profession}&location={self.city}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
            )
            req.raise_for_status()

            # create Soup
            page_soup = soup(req.text, 'html.parser')
            return extract_job_links(page_soup)
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                  f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)


class Profession_Location:

    def __init__(self, profession, place):
        self.profession = profession
        self.place = place


    def profession_location(self):
        try:
            req = requests.get(
                f'https://www.linkedin.com/jobs/search?keywords={self.profession}&location={self.place}&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
            )
            req.raise_for_status()

            # create Soup
            page_soup = soup(req.text, 'html.parser')
            return extract_job_links(page_soup)
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                  f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)



def scrape_write(links):
    try:
        if '-' in job:
            formatting = [x.capitalize() for x in job.split('-')]
            my_job = ' '.join(formatting)
        else:
            my_job = job.capitalize()

        print(colorama.Fore.YELLOW,
              f'[!] There are {len(links)} available {my_job} jobs in {place.capitalize()}.\n',
              colorama.Style.RESET_ALL)

        csv_filename = f'jobs_in_{place}.csv'
        with open(os.path.join(folder_name, csv_filename), 'w', encoding='utf-8') as f:
            headers = ['Source', 'Organization', 'Job Title', 'Location', 'Posted', 'Applicants Hired', 'Seniority Level',
                       'Employment Type', 'Job Function', 'Industries']
            write = csv.writer(f, dialect='excel')
            write.writerow(headers)

            for job_link in links:
                page_req = requests.get(job_link)
                page_req.raise_for_status()

                # Parse HTML
                job_soup = soup(page_req.text, 'html.parser')
                my_data = [job_link]

                # Topcard scraping                
                for content in job_soup.findAll('div', {'class': 'topcard__content-left'})[0:]:
                    # Scraping Organization Names
                    orgs = {'Default-Org': [org.text for org in content.findAll('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'})],
                            'Flavor-Org': [org.text for org in content.findAll('span', {'class': 'topcard__flavor'})]}

                    if orgs['Default-Org'] == []:
                        org = orgs['Flavor-Org'][0]
                        my_data.append(org)
                    else:
                        for org in orgs['Default-Org']:
                            my_data.append(org)

                    # Scraping Job Title
                    for title in content.findAll('h1', {'class': 'topcard__title'})[0:]:
                        print(colorama.Fore.GREEN,
                              f'[*] {title.text}',
                              colorama.Style.RESET_ALL, colorama.Fore.YELLOW, f'- {org}', colorama.Style.RESET_ALL)
                        my_data.append(title.text.replace(',', '.'))

                    for location in content.findAll('span', {'class': 'topcard__flavor topcard__flavor--bullet'})[0:]:
                        my_data.append(location.text.replace(',', '.'))

                    # Scraping Job Time Posted
                    posts = {'Old': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text'})],
                             'New': [posted.text for posted in content.findAll('span', {'class': 'topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new'})]}

                    if posts['New'] == []:
                        for text in posts['Old']:
                            my_data.append(text)
                    else:
                        for text in posts['New']:
                            my_data.append(text)

                    # Scraping Number of Applicants Hired
                    applicants = {'More-Than': [applicant.text for applicant in content.findAll('figcaption', {'class': 'num-applicants__caption'})],
                                  'Current': [applicant.text for applicant in content.findAll('span', {'class': 'topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption'})]}

                    if applicants['Current'] == []:
                        for applicant in applicants['More-Than']:
                            my_data.append(
                                f'{get_nums(applicant)}+ Applicants')
                    else:
                        for applicant in applicants['Current']:
                            my_data.append(f'{get_nums(applicant)} Applicants')

                # Criteria scraping
                for criteria in job_soup.findAll('span', {'class': 'job-criteria__text job-criteria__text--criteria'})[:4]:
                    my_data.append(criteria.text)

                write.writerows([my_data])
            
            print(colorama.Fore.YELLOW,
                f'\n\n[!] Written all information in: {csv_filename}',
                colorama.Style.RESET_ALL)
        # Reads scraped data
        read_data.read_scraped(folder_name, csv_filename)
    except requests.HTTPError as err:
        print(colorama.Fore.RED,
              f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)


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


if __name__ == '__main__':
    # colorama.init()
    Test("New York").web_scraper()
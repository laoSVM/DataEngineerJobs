import argparse
import csv
import requests
from random import randint
import time
from search_jobs import Scraper
from data_el_pipeline import *


def scrape_jobs(
    location="New York", profession="Data Engineer", start=0, end=1000
):
    """test function"""
    job_postings = []
    while start < end:
        time.sleep(randint(0, 5) * 1)
        print(f"Testing {start}")

        try:
            url = (
                f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/?keywords={profession}"
                + (f"&location={location}" if location else "")
                + f"&start={start}"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            result = Scraper().search_results_parsing(response.text)
            job_postings.extend(result)

            start += 25
        except requests.HTTPError as err:
            print(f"[!!] Something went wrong at {start}! {err}")
            break

    return job_postings

def unit_test(location="New York", profession="Data Engineer", end=100):
    jobs = scrape_jobs(location=location, profession=profession, end=end)
    jobs = pd.DataFrame(jobs)
    df = search_result_cleaning(jobs, args.profession)
    return df.head(1)

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
    # location = args.location
    # profession = args.profession
    print(f"Searching for: Location: {args.location}, Profession: {args.profession}")
    # jobs = scrape_jobs(location=args.location, profession=args.profession, end=50)
    # jobs = pd.DataFrame(jobs)
    # df = search_result_cleaning(jobs, args.profession)
    # load_data(
    #     user = "root",
    #     password = "root",
    #     host = "localhost",
    #     port = "5432",
    #     db = "jobs_database",
    #     table_name = "job_search_results",
    #     df = df
    #     )
    df = unit_test(args.location, args.profession, end=25)
    # print(df)

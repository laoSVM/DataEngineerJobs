import argparse
import csv
import requests
from random import randint
import time
from search_jobs import Scraper


def test(
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


def write_to_file(job_postings, destination: str):
    """write to csv file"""
    with open(destination, "w") as f:
        fieldnames = job_postings[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for row in job_postings:
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Find Nearby or Faraway Jobs",
    )

    parser.add_argument(
        "-p",
        "--place",
        default="New York",
        nargs="+",
        metavar="PLACES",
        action="store",
        help="Enter country/city/state. One or more places to look jobs from.",
    )

    parser.add_argument(
        "-j",
        "--jobfunction",
        default="Data Engineer",
        nargs="+",
        metavar="jobfunction",
        action="store",
        help="Searches Job Specification in your area. (e.g software-engineer)",
    )

    parser.add_argument(
        "-jp",
        "--jobplace",
        nargs=2,
        metavar=("job", "place"),
        action="store",
        help="Searches The Specified Job in the Specified Place. (e.g teacher iowa)",
    )
    args = parser.parse_args()

    if args.place:
        place = [args.place]
        print(place)

    if args.jobfunction:
        with requests.get("https://ipinfo.io/", timeout=10) as response:
            place = response.json()["city"].replace('"', "")
            response.raise_for_status()

        job = [args.jobfunction]
        print(job, "\n", place)

    if args.jobplace:
        jp = [args.jobplace]
        job, place = jp[0], jp[1]
        print(job, "/n", place)

    job_postings = test(location=place, profession=job, start=0, end=1000)
    write_to_file(job_postings, "jobs.csv")

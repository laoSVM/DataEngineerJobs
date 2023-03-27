import pandas
import time
import requests
import json
from random import randint
import luigi
from sqlalchemy import create_engine
from sqlalchemy import inspect, text
from luigi.contrib.postgres import PostgresTarget
from search_jobs import Scraper

class ExtractData(luigi.Task):
    """
    Download Linkedin data
    """
    start = luigi.IntParameter()
    end = luigi.IntParameter()
    location = luigi.Parameter()
    profession = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("Linkedin Source/data.json")

    def run(self):
        job_postings = []
        while self.start < self.end:
            time.sleep(randint(0, 5) * 1)
            # print(f"Testing {start}")
            try:
                url = (
                    f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/?keywords={self.profession}"
                    + (f"&location={self.location}" if self.location else "")
                    + f"&start={self.start}"
                )
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                result = Scraper().search_results_parsing(response.text)
                job_postings.extend(result)

                self.start += 25
            except requests.HTTPError as err:
                print(f"[!!] Something went wrong at {self.start}! {err}")
                break

        with self.output().open("w") as output_file:
            json.dump(job_postings, output_file)


if __name__ == "__main__":
    task_a = ExtractData(start=0, end=100, location="New York", profession="Data Engineer")
    task_a.run()
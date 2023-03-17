import os
import argparse
import json
import requests

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Find Nearby or Faraway Jobs")

    parser.add_argument("-p", "--place",
                        nargs='+', metavar='PLACES',
                        action="store",
                        help="Enter country/city/state. One or more places to look jobs from."
                    )

    parser.add_argument("-j", '--jobfunction',
                        nargs='+',
                        metavar='jobfunction',
                        action='store',
                        help='Searches Job Specification in your area. (e.g software-engineer)'
                    )

    parser.add_argument("-jp", '--jobplace',
                        nargs=2,
                        metavar=('job', 'place'),
                        action='store',
                        help="Searches The Specified Job in the Specified Place. (e.g teacher iowa)"
                    )
    args = parser.parse_args()

    if args.place:
        place = [args.place]

        print(place)


    if args.jobfunction:
        with requests.get('https://ipinfo.io/', timeout=10) as response:
            source = response.text
            response.raise_for_status()

        data = json.loads(source)
        place = json.dumps(data['city']).replace('"', '')
        job = [args.jobfunction]

        print(job, '/n', place)


    if args.jobplace:
        jp = [args.jobplace]
        job, place = jp[0], jp[1]
        print(job, '/n', place)

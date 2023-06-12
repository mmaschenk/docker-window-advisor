#!/usr/bin/env python

import os
import time
from argparse import ArgumentParser

from elasticsearch import Elasticsearch
from dotenv import load_dotenv


load_dotenv()

es_url = os.getenv("ES_URL")
es_user = os.getenv("ES_USER")
es_password = os.getenv("ES_PASSWORD")


es = Elasticsearch( es_url, http_auth=(es_user, es_password), sniff_on_start=True)

#searchRes = es.search(index="rfc8428", query= {"match_all": {}})

#print(searchRes)

def getbetween(es, lowerrange, higherrange, index='rfc8428', name="Ambientweather-F007TH:170:1:temperature"):
    result = es.search(index=index, size=100, query = {
        "bool": {
            "must": [
                {
                    "match_phrase": {
                        "n": name
                    }
                },
                {
                    "range": {
                        "t": {
                            "gte": lowerrange
                        }
                    }
                }
            ]
        }}, sort = [ { "t": {"order": "asc"}}])
    return result

def main():
    parser = ArgumentParser(
        prog='assess_temperature',
        description='Assess temperature development and give warnings'
    )
    parser.add_argument('-i', '--interval', default=7200, help='Time interval to analyze in seconds (default is 2 hours)')
    parser.add_argument('-b', '--base', default=int(time.time()), help='Base time (in seconds since epoch) to analyze for (defaults is now)')
    parser.add_argument('--indoor', default=os.getenv('INDOOR_SENSORNAME'))
    parser.add_argument('--outdoor', default=os.getenv('OUTDOOR_SENSORNAME'))
    args = parser.parse_args()
    print(args)

    print(args.base)

    return
    res = getbetween(es, args.base - args.interval, args.base, names = [ parser.indoor, parser.outdoor ])

    print(res)

    for hit in res['hits']['hits']:
        print(hit)

if __name__ == "__main__":
    main()

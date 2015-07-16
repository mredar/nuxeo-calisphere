#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import argparse
import logging
import json
from s3stash.nxstashref_file import NuxeoStashFile

def main(argv=None):
    ''' stash a single file of calisphere type 'file' on s3 '''
    parser = argparse.ArgumentParser(description='Stash Nuxeo file in S3.')
    parser.add_argument('path', help="Nuxeo document path")
    parser.add_argument('--bucket', default='ucldc-nuxeo-ref-media', help="S3 bucket name")
    parser.add_argument('--region', default='us-west-2', help="AWS region") 
    parser.add_argument('--pynuxrc', default='~/.pynuxrc', help="rc file for use by pynux")
    parser.add_argument('--replace', action="store_true", help="replace file on s3 if it already exists")
    if argv is None:
        argv = parser.parse_args()

    filename = argv.path.split('/')[-1]
    logfile = "logs/{}.log".format(filename)
    print "LOG:\t{}".format(logfile)
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s (%(name)s) [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)

    nxstash = NuxeoStashFile(argv.path, argv.bucket, argv.region, argv.pynuxrc, argv.replace)
    report = nxstash.nxstashref()

    # output report to json file
    reportfile = "reports/{}.json".format(filename)
    with open(reportfile, 'w') as f:
        json.dump(report, f, sort_keys=True, indent=4)

    # parse report to give basic stats
    print "REPORT:\t{}".format(reportfile)
    print "SUMMARY:"
    print "stashed:\t{}".format(report['stashed']) 

    print "\nDone."

if __name__ == "__main__":
    sys.exit(main())

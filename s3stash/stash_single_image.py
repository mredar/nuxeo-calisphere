#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os
import argparse
import logging
import json
from s3stash.nxstashref_image import NuxeoStashImage


def main(argv=None):

    parser = argparse.ArgumentParser(
        description='Produce jp2 version of Nuxeo image file and stash in S3.')
    parser.add_argument('path', help="Nuxeo document path")
    parser.add_argument(
        '--bucket',
        default='ucldc-private-files/jp2000',
        help="S3 bucket name")
    parser.add_argument('--region', default='us-west-2', help='AWS region')
    parser.add_argument(
        '--pynuxrc', default='~/.pynuxrc', help="rc file for use by pynux")
    parser.add_argument(
        '--replace',
        action="store_true",
        help="replace file on s3 if it already exists")
    if argv is None:
        argv = parser.parse_args()

    # logging
    # FIXME would like to name log with nuxeo UID
    filename = os.path.basename(argv.path)
    logfile = "logs/{}.log".format(filename)
    print "LOG:\t{}".format(logfile)
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s (%(name)s) [%(levelname)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)

    # convert and stash jp2
    nxstash = NuxeoStashImage(unicode(argv.path, "utf-8"), argv.bucket, argv.region,
                              argv.pynuxrc, argv.replace)
    report = nxstash.nxstashref()

    # output report to json file
    reportfile = "reports/{}.json".format(filename)
    with open(reportfile, 'w') as f:
        json.dump(report, f, sort_keys=True, indent=4)

    # parse report to give basic stats
    print "REPORT:\t{}".format(reportfile)
    print "SUMMARY:"
    if 'already_s3_stashed' in report.keys():
        print "already stashed:\t{}".format(report['already_s3_stashed'])
    print "converted:\t{}".format(report['converted'])
    print "stashed:\t{}".format(report['stashed'])

    print "\nDone."


if __name__ == "__main__":
    sys.exit(main())

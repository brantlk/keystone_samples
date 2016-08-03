# Validates a token.

import argparse

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost/identity')
    parser.add_argument('token')
    args = parser.parse_args()

    r = requests.get(
        '%s/v3/auth/tokens' % args.url,
        headers={'X-Auth-Token': args.token, 'X-Subject-Token': args.token})
    r.raise_for_status()
    print("Token data: %s" % r.json())


main()

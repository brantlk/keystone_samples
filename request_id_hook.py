# This sample shows how to set a hook on the session to get the request ID.
# Requires: keystoneauth1, python-keystoneclient


import argparse

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client


def log_request(r, *args, **kwargs):
    request_id = r.headers.get('x-openstack-request-id')
    print('%s %s %s %s' % (r.status_code, r.url, r.elapsed, request_id))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth-url', default='http://localhost/identity')
    parser.add_argument('--password')
    args = parser.parse_args()

    auth = v3.Password(auth_url='%s/v3' % args.auth_url,
                       username='admin',
                       password=args.password,
                       project_name='admin',
                       user_domain_name='Default',
                       project_domain_name='Default')
    ksa_session = session.Session(auth=auth)
    ksa_session.session.hooks = {'response': log_request}
    ks = client.Client(session=ksa_session)
    ks.users.list()


main()

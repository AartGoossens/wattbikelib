import json

import vcr

from params import (OVERWRITE_EXISTING_CASSETTES, RECORD_CASSETTES,
                    USE_CASSETTES)

RESPONSE_BODY_REPLACEMENTS = (
    ('username', 'USERNAME'),
    ('password', 'PASSWORD'),
    ('email', 'EMAIL'),
    ('sessionToken', 'r:abbcdefghikjlmnopqrstuvwxyz012345'))


def body_scrub(body):  # Pun intended...
    if not body:
        return body
    body_dict = json.loads(body)
    body_dict = json.loads(body)
    for r in RESPONSE_BODY_REPLACEMENTS:
        if r[0] in body_dict:
            body_dict[r[0]] = r[1]
    return json.dumps(body_dict).encode()


def scrub_response(response):
    response['body']['string'] = body_scrub(response['body']['string'])
    return response


def scrub_request(request):
    if not USE_CASSETTES:
        return None
    request.body = body_scrub(request.body)
    return request


def determine_record_mode():
    if not RECORD_CASSETTES:
        return 'none'
    elif OVERWRITE_EXISTING_CASSETTES:
        return 'all'
    else:
        return 'once'


custom_vcr = vcr.VCR(
    before_record_request=scrub_request,
    before_record_response=scrub_response,
    decode_compressed_response=True,
    cassette_library_dir='fixtures/vcr_cassettes',
    record_mode=determine_record_mode(),
    filter_headers=[('_SessionToken', 'SESSION_TOKEN')])

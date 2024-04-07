from io import StringIO

from tap.parser import Parser

TAP = """
TAP version 14
# plan: feditest-default
# session: feditest-default/0
    1..4
    ok 1 - webfinger.test_server_4_2__4_do_not_accept_malformed_resource_parameters
    ok 2 - webfinger.test_server_4_2__5_status_404_for_nonexisting_resources
    ok 3 - webfinger.test_server_4_2__8_server_serves_correct_content_type
    ok 4 - webfinger.test_server_4_3_server_only_returns_jrd_in_response_to_https_requests # SKIP https not supported
ok 1
1..1
"""


TAP2 = """
TAP version 14
# test plan: feditest-default
1..4
# session: feditest-default/0
ok 1 - webfinger.test_server_4_2__4_do_not_accept_malformed_resource_parameters
ok 2 - webfinger.test_server_4_2__5_status_404_for_nonexisting_resources
ok 3 - webfinger.test_server_4_2__8_server_serves_correct_content_type
not ok 4 - webfinger.test_server_4_3_server_only_returns_jrd_in_response_to_https_requests
  ---
  exception: |
    Expected: a string starting with 'https://'
         but: was 'http://localhost:9999/.well-known/webfinger?resource=acct%3Aactor%40localhost%3A9999'
  ...
"""

def test_tap():
    parser = Parser()
    result = list(parser.parse(StringIO(TAP2.strip())))
    print(result)

if __name__ == "__main__":
    test_tap()
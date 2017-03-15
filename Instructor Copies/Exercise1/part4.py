import helpers
def post_pi_value(value, web_id, base_url):
    request_type = "POST"
    resource = base_url + "/streams/" + web_id + "/value"
    body = {"Value": value}
    response = helpers.make_request(request_type, resource, body)
    return response

# Don't modify anything down here - this will automatically test your code.
import automated_tests
if __name__ == "__main__":
    automated_tests.test_part4()

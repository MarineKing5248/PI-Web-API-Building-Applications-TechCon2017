import helpers
def update_af_attribute(value, base_url, web_id):
    request_type = "PUT"
    resource = base_url + "/attributes/" + web_id + "/value"
    body = {"Value": value}
    response = helpers.make_request(request_type, resource, body)
    return response

# Don't modify anything down here - this will automatically test your code.
import automated_tests
if __name__ == "__main__":
    automated_tests.test_part3()

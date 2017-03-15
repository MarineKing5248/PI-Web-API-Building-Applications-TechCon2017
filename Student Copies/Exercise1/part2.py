import helpers
def create_af_element(name, description, base_url, parent_web_id):
    request_type = "POST"
    resource = # Enter the resource identifier here
    body = {
        "Name": name,
        "Description": description,
        "TemplateName": "RaspberryPi"
    }
    response = helpers.make_request(request_type, resource, body)
    return response

# Don't modify anything down here - this will automatically test your code.
import automated_tests
if __name__ == "__main__":
    automated_tests.test_part2()

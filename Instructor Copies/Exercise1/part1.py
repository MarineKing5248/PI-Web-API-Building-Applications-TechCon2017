import helpers
def create_pipoint(name, base_url, dataserver_web_id):
    request_type = "POST"
    resource = base_url + "/dataservers/" + dataserver_web_id + "/points"
    body = {
        "Name": name,
        "PointClass": "classic",
        "PointType": "Float32"
    }
    response = helpers.make_request(request_type, resource, body)
    return response

# Don't modify anything down here - this will automatically test your code.
import automated_tests
if __name__ == "__main__":
    automated_tests.test_part1()

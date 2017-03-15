import collections
import json
import resources
import requests
import sys
import urllib
import warnings

def make_request(request_type, resource, body):
    warnings.simplefilter("ignore")
    return requests.request(
        request_type,
        resource,
        json=body,
        headers={'Content-Type': 'application/json'},
        verify=False)

def get_web_id(response):
    warnings.simplefilter("ignore")
    get_response = requests.request(
        'GET',
        response.headers['Location'],
        verify=False)
    return json.loads(get_response.text)['WebId']
        
def delete_pipoint(web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'DELETE',
        resources.base_url + '/points/' + web_id,
        verify=False)
    return response

def delete_af_element(web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'DELETE',
        resources.base_url + '/elements/' + web_id,
        verify=False)
    return response

def get_dataserver_name(web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'GET',
        resources.base_url + '/dataservers/' + web_id,
        verify=False)
    return json.loads(response.text)['Name']

def create_pipoint(name):
    warnings.simplefilter("ignore")
    response = requests.request(
        "POST",
        resources.base_url
            + '/dataservers/'
            + resources.dataserver_web_id
            +'/points',
        json={
            'Name': name,
            'PointClass': 'classic',
            'PointType': 'Float32'},
        headers={'Content-Type': 'application/json'},
        verify=False)
    if response.status_code != 201:
        print(response.text)
        print('!!! helpers.create_pipoint critical failure - ask for instructor')
        raise SystemExit()
    return response

def create_af_element(name, description, parent_web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        "POST",
        resources.base_url
            + '/elements/'
            + parent_web_id
            + '/elements',
        json={
            'Name': name,
            'Description': description},
        headers={'Content-Type': 'application/json'},
        verify=False)
    if response.status_code != 201:
        print(response.text)
        print('!!! helpers.create_af_element critical failure - ask for instructor')
        raise SystemExit()
    return response

def delete_af_attribute(web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'DELETE',
        resources.base_url + '/attributes/' + web_id,
        verify=False)
    return response

def get_af_attribute(web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'GET',
        resources.base_url + '/attributes/' + web_id,
        verify=False)
    return response

def create_af_attribute(
        attribute_name,
        attribute_description,
        base_url,
        parent_element_web_id,
        initial_value=None):
    warnings.simplefilter("ignore")
    response = requests.request(
        'POST',
        base_url + '/elements/' + parent_element_web_id + '/attributes',
        json={
            'Name': attribute_name,
            'Description': attribute_description,
            'Type': 'Double'},
        headers={'Content-Type': 'application/json'},
        verify=False)

    if initial_value:
        update_af_attribute_value(
            initial_value,
            get_web_id(response),
            base_url)

    return response

def update_af_attribute_value(value, web_id, base_url):
    warnings.simplefilter("ignore")
    response = requests.request(
        'PUT',
        base_url + '/attributes/' + web_id + '/value',
        json={'Value': value},
        headers={'Content-Type': 'application/json'},
        verify=False)
    return response
    
def create_pipoint_referenced_af_attribute(
        attribute_name,
        attribute_description,
        base_url,
        parent_element_web_id,
        pipoint_name,
        data_archive_path):
    warnings.simplefilter("ignore")
    response = requests.request(
        'POST',
        base_url + '/elements/' + parent_element_web_id + '/attributes',
        json={
            'Name': attribute_name,
            'Description': attribute_description,
            'DataReferencePlugIn': 'PI Point',
            'ConfigString': '\\\\' + data_archive_path + '\\' + pipoint_name},
        headers={'Content-Type': 'application/json'},
        verify=False)
    return response

def get_attribute_field(web_id, accessor):
    warnings.simplefilter("ignore")
    
    return accessor(
        json.loads(
            requests.request(
                'GET',
                json.loads(
                    get_af_attribute(
                        web_id).text)['Links']['Value'],
                verify=False).text))

def check_attribute_value(response, expected_value, accessor):
    warnings.simplefilter("ignore")

    actual_value = get_attribute_field(get_web_id(response), accessor)
    
    return actual_value == expected_value

def get_attribute_web_id_by_name(name, base_url, parent_web_id):
    warnings.simplefilter("ignore")

    url = base_url + '/elements/' + parent_web_id + '/attributes/'
    element_response = requests.request(
        'GET',
        url,
        verify=False)

    for attribute in json.loads(element_response.text)['Items']:
        if attribute['Name'] == name:
            return attribute['WebId']

    return None

def get_coordinate_locations(element_response):
    parent_web_id = get_web_id(element_response)
    Point = collections.namedtuple('Point', ['x_web_id', 'y_web_id'])
    x_web_id = get_attribute_web_id_by_name(
        'XCoord',
        resources.base_url,
        parent_web_id)
    y_web_id = get_attribute_web_id_by_name(
        'YCoord',
        resources.base_url,
        parent_web_id)
    return Point(x_web_id, y_web_id)

def wrap(attempt, args):
    success = None
    try:
        attempt(*args)
        success = True
    except Exception as e:
        print(str(e))
        success = False

    return success

def get_pipoint_web_id_by_name(name, dataserver_web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'GET',
        resources.base_url
            + '/dataservers/'
            + dataserver_web_id
            + '/points?nameFilter='
            + urllib.parse.quote(name),
        verify=False)
    
    result = None
    try:
        result = json.loads(response.text)['Items'][0]['WebId']
    except Exception:
        pass
        
    return result

def get_af_element_web_id_by_name(name, parent_af_element_web_id):
    warnings.simplefilter("ignore")
    response = requests.request(
        'GET',
        resources.base_url
            + '/elements/'
            + parent_af_element_web_id
            + '/elements?nameFilter='
            + urllib.parse.quote(name),
        verify=False)

    result = None
    try:
        result = json.loads(response.text)['Items'][0]['WebId']
    except Exception:
        pass

    return result

def perform_part5_cleanup(name, permit_cleanup):
    if permit_cleanup:
        try:
            try:
                pipoint_web_id = get_pipoint_web_id_by_name(
                    name,
                    resources.dataserver_web_id)
                delete_pipoint(pipoint_web_id)
                print('Deleted PI Point')
            except Exception:
                pass

            try:
                af_element_web_id = get_af_element_web_id_by_name(
                    name,
                    resources.parent_af_element_web_id)
                delete_af_element(af_element_web_id)
                print('Deleted AF Element')
            except Exception:
                pass

            print('Cleanup done')
        except Exception as e:
            print('Cleanup errored out: ' + str(e))
    sys.exit(0)

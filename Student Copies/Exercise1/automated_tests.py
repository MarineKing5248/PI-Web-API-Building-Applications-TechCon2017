



# This file contains code which automatically tests your methods for you.
# Don't modify this during the lab - feel free to play with it later.



import helpers
import resources
import uuid
def request_rig(
        function,
        funcArgs,
        validation,
        cleanup,
        str_initial,
        str_success):
    if ((not isinstance(str_initial, str))
            and (not isinstance(str_success, str))):
        raise TypeError('str_initial and str_success must be strings')

    response = None
    try:
        print(str_initial)

        print('Sending request...')
        response_error = None
        validation_error = None
        response_received = None
        try:
            response = function(*funcArgs)
            response_received = True
        except Exception as e:
            response_error = e
            response_received = False

        validation_success = True
        try:
            validation_success = validation(response)
        except Exception as e:
            validation_error = e
            validation_success = False

        if response_error != None or response_received != True:
            print('An error occurred sending your request.')
            print('Make sure your code matches the workbook.')
            print('Response was received: ' + str(response_received))
            print('The error message was:')
            print('\t' + str(response_error))
        elif not validation_success:
            print('Request was sent, but did not succeed:')
            print('\tStatus code was: ' + str(response.status_code))
            print('\tResponse\'s body was: ' + response.text)
            print('Make sure your code matches the workbook.')
        elif validation_success:
            print(str_success)
            try:
                cleanup(response)
            except Exception as e:
                print('Cleanup in request_rig failed - continuing anyway.')
                print('Error was: ' + str(e))
        else:
            print('Unexpected fallthrough in automated_tests.request_rig')
        
        return response
    except Exception as parent_error:
        print('Failure in automated_tests.request_rig: ' + str(parent_error))
        print('Performing panic cleanup and exiting')
        try:
            cleanup(response)
        except Exception as child_error:
            print('Cleanup failed: ' + str(child_error))

    return None

def test_part1():
    import part1
    
    pipoint_name=str(uuid.uuid4())
    request_rig(
        part1.create_pipoint,
            (pipoint_name,
             resources.base_url,
             resources.dataserver_web_id),
        lambda x: x and x.status_code == 201,
        lambda x: helpers.delete_pipoint(helpers.get_web_id(x)),
        'Creating a PI Point with a random name...',
        'Successfully created PI Point! Your function works!')

def test_part2():
    import part2
    
    afelement_name=str(uuid.uuid4())
    afelement_desc=str(uuid.uuid4())
    request_rig(
        part2.create_af_element,
            (afelement_name,
             afelement_desc,
             resources.base_url,
             resources.parent_af_element_web_id),
        lambda x: x and x.status_code == 201,
        lambda x: helpers.delete_af_element(helpers.get_web_id(x)),
        'Creating an AF Element with a random name and description...',
        'Successfully created AF Element! Your function works!')

def test_part3():
    import part3
    
    afelement_name=str(uuid.uuid4())
    afelement_desc=str(uuid.uuid4())
    attribute_name=str(uuid.uuid4())
    attribute_desc=str(uuid.uuid4())

    afelement_response=helpers.create_af_element(
        afelement_name,
        afelement_desc,
        resources.parent_af_element_web_id)

    initial_value=generate_value()
    expected_value=initial_value
    while expected_value == initial_value:
        expected_value=generate_value()

    attribute_response=helpers.create_af_attribute(
        attribute_name,
        attribute_desc,
        resources.base_url,
        resources.parent_af_element_web_id,
        initial_value)

    request_rig_success = helpers.wrap(
        request_rig,
            (part3.update_af_attribute,
                (expected_value,
                 resources.base_url,
                 helpers.get_web_id(attribute_response)),
            lambda x: helpers.check_attribute_value(
                attribute_response,
                expected_value,
                lambda y: y['Value']),
            lambda x: x,
            'Creating a random attribute and PUTing a random value to it...',
            'Successfully PUTed value! Your function works!'))
    if request_rig_success != True:
        print('request_rig failure: ' + str(request_rig_success))

    helpers.wrap(helpers.delete_af_attribute, (helpers.get_web_id(attribute_response),))
    helpers.wrap(helpers.delete_af_element, (helpers.get_web_id(afelement_response),))

def test_part4():
    import json
    import part4
    
    pipoint_name=str(uuid.uuid4())
    afelement_name=str(uuid.uuid4())
    afelement_desc=str(uuid.uuid4())
    attribute_name=str(uuid.uuid4())
    attribute_desc=str(uuid.uuid4())

    pipoint_response=helpers.create_pipoint(pipoint_name)
    afelement_response=helpers.create_af_element(
        afelement_name,
        afelement_desc,
        resources.parent_af_element_web_id)
    attribute_response=helpers.create_pipoint_referenced_af_attribute(
        attribute_name,
        attribute_desc,
        resources.base_url,
        helpers.get_web_id(afelement_response),
        pipoint_name,
        helpers.get_dataserver_name(resources.dataserver_web_id))

    generated_value=generate_value()

    request_rig_success = helpers.wrap(
        request_rig,
            (part4.post_pi_value,
                (generated_value, 
                helpers.get_web_id(attribute_response),
                resources.base_url),
            lambda x: helpers.check_attribute_value(
                attribute_response,
                generated_value,
                lambda y: y['Value']),
            lambda x: x,
            'Creating a random attribute and POSTing a random value to it...',
            'Successfully POSTed value! Your function works!'))
    if request_rig_success != True:
        print('request_rig failure: ' + str(request_rig_success))
        
    helpers.wrap(helpers.delete_af_attribute, (helpers.get_web_id(attribute_response),))
    helpers.wrap(helpers.delete_af_element, (helpers.get_web_id(afelement_response),))
    helpers.wrap(helpers.delete_pipoint, (helpers.get_web_id(pipoint_response),))

def generate_value():
    # Perform logical and for rightmost 23 bits to guarantee float32 size
    # 30 breaks - ask stephen?
    return uuid.uuid4().int & (1<<23)-1

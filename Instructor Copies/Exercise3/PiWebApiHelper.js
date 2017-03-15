// The list of attributes our display maintains and displays. Used in all exercises. 
var af_elements = [];

// Exercise 3B
// Function to create the body of the POST request.
function MakeBatchPostBody(firstRequest, secondRequest)
{
	// Construct a key value collection (dictionary) with the supplied requests.
	var dict = {
		"1" : firstRequest, 
		"2" : secondRequest
	}
	
	// Convert the dictionary object to a string to go into the POST content body. 
	return JSON.stringify(dict);
}

// Exercise 3B
// Function to send a batch request with a supplied batch URL and POST request body.
function MakeBatchRequest(url, requestBody)
{
	af_elements = [];
	
	$.ajax({
		url: url,
		type:'POST',
		data: requestBody,
		dataType: 'json',
		contentType: "application/json",
		success:function(response){

			var firstRequestResponse = response[1];
			var secondRequestResponse = response[2];
			
			// Parse the results of the first request to populate our elements array.
			$.each(firstRequestResponse.Content.Items, function(index, value) {	
								
				// Create our element object for data storage.
				var af_element = { Name: value.Name, WebId: value.WebId }

				// Add it to the list of maintained elements for our display.
				af_elements.push(af_element);
			});
			
			// Parse the results of the second request to populate the values of our elements.
			$.each(secondRequestResponse.Content.Items, function(index, value) {
				af_elements[index].Value = value.Content.Items[0].Value.Value;
				af_elements[index].Xcoord = value.Content.Items[1].Value.Value;
				af_elements[index].Ycoord = value.Content.Items[2].Value.Value;
			});
			
			// Update the display with new values. 
			PopulateDisplay();
		}
	});	
}

// Exercise 3C
// Creates  web scoket connection for a specified af_element URL 
function CreateWebSocketConnection(WebSocketUrl){
	var webSocket = new WebSocket(WebSocketUrl);
	
	// Callback method triggered on web socket connection opening.
	webSocket.onopen = function(event)
	{
		console.log("Connection opened.");
		try
		{
			// Update the display with current values when we open a WebSocket connection. 
			PopulateDisplay();
		}
		catch(e){
			
		}
	};

	// Callback method triggered on web socket connection error.
	webSocket.onerror = function(event)
	{
		console.log("Connection aborted.");
	};

	// Callback method triggered on web socket connection closing.
	webSocket.onclose = function(event)
	{
		console.log("Connection closed.");
	};

	// Callback method triggered on web socket connection message received. 
	// On receiving value changes for an element, parse response and update our internal element storage.
	webSocket.onmessage = function(event)
	{
		var responseObject = JSON.parse(event.data);
		var name = responseObject.Items[0].Name;
		if(name === "Temperature")
		{
			// Get the name of the element from the response body. 
			var elementUpdated = responseObject.Items[0].Path.substring(responseObject.Items[0].Path.lastIndexOf('\\') + 1).split("|")[0];
			
			// Get the new sensor value from the response body.
			var newSensorValue = responseObject.Items[0].Items[0].Value;
			
			// Find the element that was updated in our internal list this file maintains, and update its current value to the new value. 
			function findElements(updatedElement){
				return function (currentElement) {
					return currentElement.Name === updatedElement;
				}
			}
			var af_element = af_elements.find(findElements(elementUpdated));
			af_element.Value = newSensorValue;
			
			// Update the display with the new values. 
			PopulateDisplay();
		}
	};
}

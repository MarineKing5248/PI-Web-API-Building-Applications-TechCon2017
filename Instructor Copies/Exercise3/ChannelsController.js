$( document ).ready(function() {
	  		
	// URL of Instructors instance of PI Web API and the WebId of the parent element we have created child elements on. 
	var BaseWebAPIUrl = "192.168.0.99/piwebapi";
	var AFParentElementWebId = "E0RgRPVjeKO0qkC4YCWdocjwu7mDbBgA5xGEFgAVXQL3CgSU5TVFJVQ1RPUlxDT05GSUdVUkFUSU9OXFVDMjAxNw";

	// Make a GET request for the list of child elements on the parent element. 
	var ChildElementsUrl = "https://" + BaseWebAPIUrl + "/elements/" + AFParentElementWebId + "/elements";
	$.getJSON(ChildElementsUrl, null, function(response){
		$.each( response.Items, function( index, value ) {
			
			// Create our element object for data storage.
			var af_element = { Name: value.Name, WebId: value.WebId }

			// Add it to the list of maintained attributes for our display.
			af_elements.push(af_element);
			
			// Call the PopulateAttributeValues method to retrieve the element's latest attribute values.
			PopulateAttributeValues(af_element);
			
			// Enter Exercise 3C step 3 code below this line.
			var WebSocketUrl = "wss://" + BaseWebAPIUrl + "/streamsets/" + af_element.WebId + "/channel";
			CreateWebSocketConnection(WebSocketUrl);
		});
	})
											
	// Method to populate the attributes values for our elements and then call the PopulateDisplay function.
	function PopulateAttributeValues(af_element) {		
		// Make a GET request for the latest attribute values of an element. 
		var ValueURL = "https://" + BaseWebAPIUrl + "/streamsets/" + af_element.WebId + "/value";		
		$.getJSON(ValueURL, null, function(response){
			af_element.Value = response.Items[0].Value.Value;
			af_element.Xcoord = response.Items[1].Value.Value;
			af_element.Ycoord = response.Items[2].Value.Value;
		});			
	}	
});

$( document ).ready(function() {

	// URL of Instructors instance of PI Web API and the WebId of the parent element we have created child elements on. 
	var BaseWebAPIUrl = "https://192.168.0.99/piwebapi";
	var AFParentElementWebId = "E0RgRPVjeKO0qkC4YCWdocjwu7mDbBgA5xGEFgAVXQL3CgSU5TVFJVQ1RPUlxDT05GSUdVUkFUSU9OXFVDMjAxNw";
	
	function PopulateElements()
	{		
		// Enter Exercise 3A step 3 code below this line.
		// Construct the URL for the request to retrieve the list of child elements on the parent element. 
		var ChildElementsUrl = BaseWebAPIUrl + "/elements/" + AFParentElementWebId + "/elements";
		
		// Make a GET request at the specified URL, receiving the response in JSON.
		$.getJSON(ChildElementsUrl, null, function(response){
			af_elements = []
			$.each( response.Items, function( index, value ) {
				
				// Create our element object for data storage by retrieving data from the response body.
				var af_element = { Name: value.Name, WebId: value.WebId }

				// Add the element to the list of maintained elements for our display.
				af_elements.push(af_element);
				
				// Call the PopulateAttributeValues method to retrieve the element's latest attribute values.
				PopulateAttributeValues(af_element);
			});	
		});
	}	

	// Method to populate the attributes values for a elements and updating application storage
	function PopulateAttributeValues(af_element) {		

		// Enter Exercise 3A step 4 code below this line. 
		// Construct the URL for the request to retrieve the latest attribute values of an element. 
		var ValueUrl = BaseWebAPIUrl + "/streamsets/" + af_element.WebId + "/value";
		
		// Make a GET request at the specified URL, receiving the response in JSON.
		$.getJSON(ValueUrl, null, function(response){
			
			af_element.Value = response.Items[0].Value.Value;
			af_element.Xcoord = response.Items[1].Value.Value;
			af_element.Ycoord = response.Items[2].Value.Value;		
		});
	}	
	
	// Method to continously check for value changes every 2.5 seconds, saves scroll position for different size screens. 
	function Poll()
	{			
		setInterval(function(){
			PopulateElements();
			PopulateDisplay();
		}, 2500);
	}
	
	// Exercise 3A step 5 code below this line. 
	Poll();
});
	   

	

$( document ).ready(function() {

	// URL of Instructors instance of PI Web API and the WebId of the parent element we have created child elements on. 
	var BaseWebAPIUrl = "https://192.168.0.99/piwebapi";
	var AFParentElementWebId = "E0RgRPVjeKO0qkC4YCWdocjwu7mDbBgA5xGEFgAVXQL3CgSU5TVFJVQ1RPUlxDT05GSUdVUkFUSU9OXFVDMjAxNw";
	
	// Enter Exercise 3B step 3 code below this line.
	var BatchUrl = BaseWebAPIUrl + "/batch";
	var ChildElementsUrl = BaseWebAPIUrl + "/elements/" + AFParentElementWebId + "/elements";

	// First request retrieves all the child elements representing Raspberry Pis.
	var firstRequestObject = {
		Method: "GET",
		Resource: ChildElementsUrl
	};

	// Second request retrieves the current values of all the attributes on the elements returned by the parent request.
	var secondRequestObject = {
		Method: "GET",
		RequestTemplate: {
			Resource: "$.1.Content.Items[*].Links.Value"
		},
		Headers:{
			"Cache-Control" : "no-cache"
		},
		ParentIds: ["1"]
	}
	
	// Initialize our batch dictionary for the body of the POST request
	var BatchPostBody = MakeBatchPostBody(firstRequestObject, secondRequestObject);

	// Make batch request every 2.5 seconds
	setInterval(function(){		
		MakeBatchRequest(BatchUrl, BatchPostBody);
	}, 2500);
});

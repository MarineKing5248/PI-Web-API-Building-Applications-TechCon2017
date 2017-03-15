// The list of series data that the heat map chart contains.
var chartSeries; 

// The progress bar and the current bars progress.
var bar;
var barProgress;

// When the page loads, create the chart and progress bar.
$( document ).ready(function() {
	
	bar = new ProgressBar.Line(progressBar, {
	  strokeWidth: 4,
	  easing: 'easeInOut',
	  duration: 1400,
	  color: '#446789',
	  trailColor: '#eee',
	  trailWidth: 1,
	  svgStyle: {width: '100%', height: '100%'}
	});

	barProgress = .1;
	bar.animate(barProgress);  // Number from 0.0 to 1.0
	
	chart = new Highcharts.Chart({

		chart: {
			renderTo: 'heatMap',
			type: 'heatmap',
			marginTop: 40,
			marginBottom: 40,
			backgroundColor: "#cfcfcf",
			events:{
				// On chart load store the series itself globally so we can change its data later.
				load: function(){
					chartSeries = this.series[0];
				}
			}
		},

		title: {
			text: "Heat Map"
		},

		xAxis: {
			categories: [], 
			tickInterval:1,
			tickmarkPlacement: 'between',
			gridLineWidth: 1
		},

		yAxis: {
			categories: [],
			title: null,
			tickInterval:1,
			tickmarkPlacement: 'between',
			gridLineWidth: 1
		},

		colorAxis: {
			min: 0,
			minColor: '#e5e5ff',
			maxColor: '#ff0000'
		},

		legend: {
			align: 'right',
			layout: 'vertical',
			margin: 0,
			verticalAlign: 'top',
			y: 25,
			symbolHeight: 320
		},

		tooltip: {
			formatter: function () {
				try
				{
					// Function to get the name of the Raspberry Pi Element for the tooltip on hovering.
					var cachedX = this.point.x;
					var cachedY = this.point.y;
					
					var result = af_elements.filter(function( obj ) {
						return obj.Xcoord === cachedX && obj.Ycoord === cachedY;
					});

					return '<b>' + result[0].Name + '</b>';	
				}
				catch(e)
				{
					console.log(e);
				}
			}
		},

		series: [{
			borderWidth: 0,
			data : [],
			dataLabels: {
				enabled: true,
				color: 'black',
				style: {
					textShadow: 'none',
					textOutline: 'none'
				},
			}
		}]
	});
	
	// Hide heat map until we get our initial data. 
	$('#heatMap').css("visibility", "hidden");

});

// Method to update our heat map chart using the sensor values we retrieve. Used in all exercises. 
function PopulateDisplay()
{	
	var x = -1;
	var y = -1;
	var dataArray = [];
	
	var barIncrementInterval;
	if(af_elements.length > 0)
	{
		barIncrementInterval = .8 / af_elements.length;
	}
	
	$.each( af_elements, function( index, value ) {
		barProgress += barIncrementInterval;
		
		if(value.Xcoord > x){
			x = value.Xcord;
		}
		
		if(value.Ycoord > y){
			y = value.Ycoord; 
		}
				
		var data = [value.Xcoord, value.Ycoord, value.Value];
		dataArray.push(data);
		
		bar.animate(barProgress);
	});	
	
	
	// Update heat map with the updated sensor values. 
	chartSeries.setData(dataArray, true, true);
	
	bar.animate(1);
	
	// Heatmap setData function has a rendering delay. 
	setTimeout(function(){
		$('#progressBar').hide("100");
		$('#heatMap').css("visibility", "visible");
	}, 1000);
}	 
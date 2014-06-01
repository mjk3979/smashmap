$(document).ready(function()
{
	var mymap = undefined;
	function initialize() {
		var mapOptions = {
		  center: new google.maps.LatLng(35.696, 262.616),
		  zoom: 4
		};
		mymap = new google.maps.Map(document.getElementById("map-canvas"),
			mapOptions);
		fetchEvents(function()
		{
			geocodeEvents(placeEvent);
		});
	}
	google.maps.event.addDomListener(window, 'load', initialize);

	var events = null;

	function fetchEvents(callback)
	{
		$.ajax({
			  url: '/getEvents'
			, type: 'GET'
			, success: function(data)
			{
				events = data.events;
				if (callback !== undefined)
					callback();
			}
			, error: function()
			{
				console.log('AJAX ERROR');
			}
		});
	}

	function placeEvent(e)
	{
		if (e.coords === undefined)
			return;

		var content = $('<div></div>');
		var table = $('<table></table>');
		function makeRow(label, content, link)
		{
			var row = $('<tr></tr>');
			row.append($('<td></td>').text(label));
			if (link == undefined)
				row.append($('<td></td>').text(content));
			else
			{
				var a = $('<a></a>');
				a.attr('href', link);
				a.text(content);
				var td = $('<td></td>');
				td.append(a);
				row.append(td);
			}
			table.append(row);
		}
		makeRow('Event Name', e.name, e.link);
		makeRow('Start Date', e.start);
		makeRow('End Date', e.end);
		makeRow('Location', e.location);

		content.append(table);


		var infowindow = new google.maps.InfoWindow({
		  content: content.html()
		});

		var marker = new google.maps.Marker({
			  position: e.coords
			, map: mymap
			, title: e.name
		});

		google.maps.event.addListener(marker, 'click', function() {
			infowindow.open(mymap,marker);
		});
	}

	function geocodeEvents(callback)
	{
		$.each(events, function(_, e)
		{
			console.log(e);
			$.ajax({
				  url: 'http://maps.googleapis.com/maps/api/geocode/json'
				, type: 'GET'
				, data: {address: e.location}
				, success: function(data)
				{
					if (data
						&& data.results
						&& data.results[0]
						&& data.results[0].geometry
						&& data.results[0].geometry.location
					)
					{
						e.coords = data.results[0].geometry.location;
						callback(e);
					}
				}
				, error: function()
				{
				}
			});
		});

	}
});

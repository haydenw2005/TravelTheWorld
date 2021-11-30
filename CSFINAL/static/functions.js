function addToDict() {
 	for (const [key, value] of Object.entries(wishlist)) {
  	console.log(key, value, value[0], value[1]);
		geojson["features"].push({'type': 'Feature', 'geometry': {
			'type': 'Point',
			'coordinates': [value[1], value[0]]
		},
		'properties': {
			'title': key,
			'description': 'This is on your list!'
		}});
	}
	addToMap()
}
//From w3 js tutorial
//https://www.w3schools.com/howto/howto_js_filter_lists.asp
function searchBar() {
  var filter = document.getElementById('bar').value.toUpperCase();
  var ul = document.getElementById("myUL");
  var li = ul.getElementsByTagName('li');
  for (var i = 0; i < li.length; i++) {
    var a = li[i].getElementsByTagName("a")[0];
    var txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}
//code taken from mapbox api tutorial
//https://docs.mapbox.com/help/tutorials/custom-markers-gl-js/
mapboxgl.accessToken = 'pk.eyJ1IjoiaGF5ZGVuc3doaXRlIiwiYSI6ImNrdnVlZHd1aDJnenUybm1vY294dWd1dHEifQ.mdc8TfrMvuyyjsIRwKd-0A';
let geojson = {
	'type': 'FeatureCollection',
	'features': [
	]
};
const map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/haydenswhite/ckvueyyaa2x3415msm16ouc8c',
	center: [-1.83762741088867,33.179770125276974],
	zoom: 1.12
});
function addToMap() {
	for (const feature of geojson.features) {
		const el = document.createElement('div');
		el.className = 'marker';
		new mapboxgl.Marker(el).setLngLat(feature.geometry.coordinates).setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h3>${feature.properties.title}</h3><p>${feature.properties.description}</p>`)).addTo(map);
	}
}
window.onload = addToDict;

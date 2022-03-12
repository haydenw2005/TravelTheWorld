//If button button element clicked, get api

$("button").click(function() {
  var country = $(this).val();
  let api_url = "https://restcountries.com/v3.1/name/" + country;
  getapi(api_url, country, true);
});

//fetches api
async function getapi(url, country, seeData) {
    const response = await fetch(url);
    var data = await response.json();
    if (seeData == true) {
      showData(data, country);
    } else {
      addToDatabase(data, country);
    }
}

//displays data ins earch menu
function showData(data, country) {
  var elements = document.getElementById('countryInfo').children;
  for (i = 0; i < elements.length; i++) {
    elements[i].removeAttribute("hidden");
  }
  document.getElementById("searchMenuHeader").innerHTML = country;
  document.getElementById("bar").style.display = "none";
  document.getElementById("myUL").style.display = "none";
  document.getElementById("official").innerHTML = "Official name: " + data[0]["name"]["official"];
  document.getElementById("capital").innerHTML = "Capital: " + data[0]["capital"][0];
  document.getElementById("region").innerHTML = "Region: " + data[0]["region"];
  document.getElementById("subregion").innerHTML = "Subregion: " + data[0]["subregion"]
  document.getElementById("population").innerHTML = "Population: " + data[0]["population"];
  document.getElementById("timezone").innerHTML = "Timezone: " + data[0]["timezones"][0];
  document.getElementById("flag").src = data[0]["flags"]["png"];
}

//hides the search data --- undos the function above
var searchExitButton = document.querySelector("#searchExitButton");
searchExitButton.addEventListener("click", hideSearchData, false);
function hideSearchData(e) {
  var elements = document.getElementById('countryInfo').children;
  for (i = 0; i < elements.length; i++) {
    elements[i].setAttribute("hidden", true);
  }
  document.getElementById("searchMenuHeader").innerHTML = "Search a Country";
  document.getElementById("bar").style.display = "block";
  document.getElementById("myUL").style.display = "block";
}

//hides setting data
var settingsExitButton = document.querySelector("#settingsExitButton");
settingsExitButton.addEventListener("click", hideSettingData, false);

function hideSettingData(e) {
  document.getElementById("hiddenMessage").style.display = "none";
  var elements = document.getElementsByClassName("deleteCountryItem");
  for (i = 0; i < elements.length; i++) {
    elements[i].style.display = "none";
  }
  document.getElementById("settingHeader").innerHTML = "Settings";
  document.getElementById("logoutLink").style.display = "block";
  document.getElementById("deleteCountriesHeader").style.display = "block";
  document.getElementById("deleteButton").style.display = "none";
  document.getElementById("settingsExitButton").style.display = "none";
}

//when add button clicked, make addToDatabase call
var addButton = document.querySelector("#addButton");
addButton.addEventListener("click", callToDbProcess, false);

function callToDbProcess() {
  var countryName = document.getElementById("searchMenuHeader").innerText;
  let api_url = "https://restcountries.com/v3.1/name/" + countryName;
  getapi(api_url, countryName, false);

}

//adds item to database
function addToDatabase(data, countryName) {
  let countryDbInfo = {
    "name": countryName,
    "lat": data[0]["latlng"][0],
    "long": data[0]["latlng"][1],
  }
  const xhttp = new XMLHttpRequest();
  xhttp.open('POST', `pin/${JSON.stringify(countryDbInfo)}`);
  xhttp.onload = () => {
    updateMap();
  }
  xhttp.send();
}

//open delete country menu
var deleteCountriesHeader = document.querySelector("#deleteCountriesHeader");
deleteCountriesHeader.addEventListener("click", deleteCountries, false);

function deleteCountries(e) {
  document.getElementById("settingHeader").innerHTML = "Delete Countries";
  document.getElementById("logoutLink").style.display = "none";
  document.getElementById("deleteCountriesHeader").style.display = "none";
  let i = 0;
  var listItems = document.getElementsByClassName("deleteCountryItem");
  for (const feature of geojson.features) {
    console.log(feature.properties.title);
    i++;
    for (i = 0; i < listItems.length; i++) {
      if (listItems[i].innerHTML == feature.properties.title) {
        listItems[i].style.display = "block";
      }
    }
  }
  if (i == 0){
    document.getElementById("hiddenMessage").style.display = "block";
  }
  document.getElementById("settingsExitButton").style.display = "block";
  document.getElementById("deleteButton").style.display = "block";
}

//applies cred crossout class to countries in delete menu
$(".deleteCountryItem").click(function() {
  if ($(this).hasClass("crossedOut")) {
    $(this).removeClass("crossedOut");
  } else {
    $(this).addClass("crossedOut");
  }
  var deleteButton = document.querySelector("#deleteButton");

  deleteButton.addEventListener("click", sendDeleteRequest, false);
});

//call backend function to delete items
function sendDeleteRequest(e) {
  if ($('.crossedOut').length >= 1) {
    var deletedCountriesDict = []
    for (i = 0; i < $('.crossedOut').length; i++) {
      deletedCountriesDict.push({'name': document.getElementsByClassName("crossedOut")[i].innerText});
    }


    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', `delete/${JSON.stringify(deletedCountriesDict)}`);
    xhttp.onload = () => {
      hideSettingData(e);
      updateMap();
    }
    xhttp.send();

  }
}

//open and closes tutorial
var dropdown = document.querySelector("#map_dropdown");
var informationMenu = document.querySelector("#informationMenu");
let isInfoOpen = false;

dropdown.addEventListener("click", changeInfoMenu, false);

function changeInfoMenu(e) {
  if (isInfoOpen == false) {
    informationMenu.classList.add("show");
    document.body.style.overflow = "hidden";
    isInfoOpen = true;
  }

  else {
    informationMenu.classList.remove("show");
    e.stopPropagation();
    document.body.style.overflow = "auto";
    isInfoOpen = false;
  }
}

//open and closes search menu
var searchButton = document.querySelector("#searchButton");
var searchMenu = document.querySelector("#searchMenu");
let isSearchOpen = false;
let isSettingsOpen = false;

searchButton.addEventListener("click", changeSearchMenu, false);

function changeSearchMenu(e) {
  if (isSearchOpen == false) {
    if (isSettingsOpen == true) {
      changeSettingMenu(e);
    }
    searchMenu.classList.add("show");
    document.body.style.overflow = "hidden";
    isSearchOpen = true;
  }

  else {
    searchMenu.classList.remove("show");
    e.stopPropagation();
    document.body.style.overflow = "auto";
    isSearchOpen = false;
    hideSearchData(e);
  }
}

//open and closes setting menu
var settingButton = document.querySelector("#settingButton");
var settingMenu = document.querySelector("#settingMenu");

settingButton.addEventListener("click", changeSettingMenu, false);

function changeSettingMenu(e) {
  if (isSettingsOpen == false) {
    if (isSearchOpen == true) {
      changeSearchMenu(e);
    }
    settingMenu.classList.add("show");
    document.body.style.overflow = "hidden";
    isSettingsOpen = true;
  }

  else {
    settingMenu.classList.remove("show");
    e.stopPropagation();
    document.body.style.overflow = "auto";
    isSettingsOpen = false;
    hideSettingData(e);
  }
}

//updates map, call addToDict and addToMap
function updateMap() {
  addToDict(wishlist)
  const xhttp = new XMLHttpRequest();
  xhttp.open('POST', 'getDbCountries');
  xhttp.onload = () => {
    const wishlist = JSON.parse(xhttp.responseText);
    addToDict(wishlist);
    addToMap();
  }
  xhttp.send();
}

//Adds items to country dictionary
function addToDict(wishlist) {
  geojson["features"] = []
  for (const [key, value] of Object.entries(wishlist)) {
    geojson["features"].push({'type': 'Feature', 'geometry': {
      'type': 'Point',
      'coordinates': [value[1], value[0]]
    },
    'properties': {
      'title': key,
      'description': 'This is on your list!'
    }});
  }
  addToMap();
}

//Search bar filter code
function searchBar() {
  var filter = document.getElementById('bar').value.toUpperCase();
  var ul = document.getElementById("myUL");
  var li = ul.getElementsByTagName('li');
  for (var i = 0; i < li.length; i++) {
    var button = li[i].getElementsByTagName("button")[0];
    var txtValue = button.textContent || button.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

//code for map and map box markers
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

//adds markers to map
function addToMap() {
  var listItems = document.getElementsByClassName("marker");
  for (i = 0; i < listItems.length; i++) {
    listItems[i].remove();
  }
	for (const feature of geojson.features) {
		const el = document.createElement('div');
		el.className = 'marker';
		new mapboxgl.Marker(el).setLngLat(feature.geometry.coordinates).setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h1>${feature.properties.title}</h1><p>${feature.properties.description}</p>`)).addTo(map);
	}
}
window.onload = updateMap;

//Makes it so you cant press enter on search bar
$("search").on("keydown", "form", function(event) {
    return event.key != "Enter";
});

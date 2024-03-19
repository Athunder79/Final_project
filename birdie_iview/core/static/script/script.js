addEventListener('DOMContentLoaded', function () {

  let location = document.getElementById("location");
  let map = document.getElementById("toggle-map");

  // check if the element exists before adding the event listener
  if (location != null){location.addEventListener("click", getLocation);}
  if (map != null){map.addEventListener("click", showMap);}
})


// Get the latitude and longitude from browser
function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition,showError);
    }
  else{result.innerHTML="Geolocation is not supported by this browser.";}
  }

// add the latitude and longitude to the form and post
function showPosition(position)
  {
  lat=position.coords.latitude;
  lon=position.coords.longitude;
  document.getElementById("id_latitude").value= lat;
  document.getElementById("id_longitude").value= lon;
  document.getElementById('shotForm').submit()
  }

function showError(error)
  {
  switch(error.code)
    {
    case error.PERMISSION_DENIED:
      document.getElementById("result").innerHTML="Please allow geolocation ."
      break;
    case error.ERR_INTERNET_DISCONNECTED:
      document.getElementById("result").innerHTML="You have no internet Connection."
      break;
    case error.TIMEOUT:
      document.getElementById("result").innerHTML="The request to get user location timed out."
      break;
    }
  }

// show or hide the map
function showMap(){
  document.getElementById("map-container").classList.toggle("hide")
  if (document.getElementById("show-map").innerHTML == "Hide Map"){
    document.getElementById("show-map").innerHTML = "Show Map"
  } else {
    document.getElementById("show-map").innerHTML = "Hide Map"
  }

}

addEventListener('DOMContentLoaded', function () {

  let location = document.getElementById("location");

  // check if the element exists before adding the event listener
  if (location != null)
  location.addEventListener("click", getLocation);
})


let x = document.getElementById("result");

function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition,showError);
    }
  else{x.innerHTML="Geolocation is not supported by this browser.";}
  }


  function showPosition(position)
  {
  lat=position.coords.latitude;
  lon=position.coords.longitude;
  id_latitude.value= lat;
  id_longitude.value= lon;

  }

  function showError(error)
  {
  switch(error.code)
    {
    case error.PERMISSION_DENIED:
      x.innerHTML="User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML="Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML="The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML="An unknown error occurred."
      break;
    }
  }
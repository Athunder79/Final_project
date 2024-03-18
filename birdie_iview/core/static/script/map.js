$(document).ready(function(){
    $.ajax({
        url: mapShotsUrl,
        method: 'GET',
        success: function (data) {
            console.log(data);
            initMap(data);
        }
    });
});

function initMap(data) {
   const map = new google.maps.Map(document.getElementById('map'), {
      zoom: 18,
      mapTypeId: 'satellite',
      center: {lat: 53.3911059, lng: -6.2085319}

   });
   const markers = data?.map((i) => {
        const marker = new google.maps.Marker({
            position: { lat: parseFloat(i.latitude), lng: parseFloat(i.longitude)},
            map: map,
        })
    });

 }
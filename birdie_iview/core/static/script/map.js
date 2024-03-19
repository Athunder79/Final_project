
$(document).ready(function () {
    $.ajax({
        url: mapShotsUrl,
        method: 'GET',
        success: function (data) {
            console.log(data);
            getUserLocation(data, roundId);
        }
    });
});

function getUserLocation(data, roundId) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            initMap(data, userLocation, roundId);
        },

            function () {
                handleLocationError(true);
            });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false);
    }
}

function initMap(data, userLocation, roundId) {
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 18,
        mapTypeId: 'satellite',
        center: userLocation // Center the map at the user's location
    });

    // Marker for the user's current location
    const userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        title: 'You are here'
    });

    // Filter to nly include shots from the current round
    if (data){
    const currentRoundShots = data.filter(function(shot) {
        return shot.round_id === roundId;
    });

    // Markers for shots on the golf course
    const markers = currentRoundShots.map(shot => {
        return new google.maps.Marker({
            position: { lat: parseFloat(shot.latitude), lng: parseFloat(shot.longitude) },
            map: map,
            title: 'shot',
        });
    });
 console.log(currentRoundShots);
}
}

function handleLocationError(browserHasGeolocation) {
    let errorMessage = '';
    if (browserHasGeolocation) {
        errorMessage = 'Error: The Geolocation service failed.';
    } else {
        errorMessage = 'Error: Your browser does not support geolocation.';
    }
    console.error(errorMessage);
}
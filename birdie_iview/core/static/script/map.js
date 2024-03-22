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
        center: userLocation // Center of the map
    });

    // Marker for the user's current location
    const userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        title: 'You are here'
    });

    // Filter to only include shots from the current round
    if (data) {
        const currentRoundShots = data.filter(function (shot) {
            return shot.round_id === roundId;
        });

        // Markers for shots on the golf course
        currentRoundShots.forEach(shot => {
            const marker = new google.maps.Marker({
                position: { lat: parseFloat(shot.latitude), lng: parseFloat(shot.longitude) },
                map: map,
                title: 'Shot ' + shot.shot_num_per_hole + ' Hole ' + shot.hole_num + ' Distance ' + shot.shot_distance + ' Metres',
            });


            // Info window for each marker
            const infowindow = new google.maps.InfoWindow({
                content: `
                    <div>
                        <h3>Hole ${shot.hole_num}</h3>
                        <p><strong>Shot:</strong> ${shot.shot_num_per_hole}</p>
                        <p><strong>Club:</strong> ${shot.club__club_name}</p>
                        <p><strong>Distance:</strong> ${shot.shot_distance} Metres</p>
                    </div>
                `
            });

            // Open info window when marker is clicked
            marker.addListener('click', function () {
                infowindow.open(map, marker);
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

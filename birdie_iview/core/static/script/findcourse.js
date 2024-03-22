function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12
    });

    // Retrieve user's current location and center the map
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            let userLocation = {
                lat: position.coords.latitude,function initMap() {
                    let map = new google.maps.Map(document.getElementById('map'), {
                        zoom: 12
                    });function initMap() {
                        let map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 12
                        });

                        // Retrieve user's current location and center the map
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(function(position) {
                                let userLocation = {
                                    lat: position.coords.latitude,
                                    lng: position.coords.longitude
                                };
                                map.setCenter(userLocation);
                            }, function() {
                                handleLocationError(true, map.getCenter());
                            });
                        } else {
                            // Browser doesn't support Geolocation
                            handleLocationError(false, map.getCenter());
                        }

                        // pins for golf courses
                        let golfCourses = [
                            {% for course in golf_courses %}
                            {
                                name: "{{ course.name }}",
                                location: {lat: {{ course.latitude }}, lng: {{ course.longitude }}}
                            },
                            {% endfor %}
                        ];

                        golfCourses.forEach(function(course) {
                            let marker = new google.maps.Marker({
                                position: course.location,
                                map: map,
                                title: course.name
                            });
                        });
                    }

                    function handleLocationError(browserHasGeolocation, center) {
                        // Handle errors here
                    }


                    // Retrieve user's current location and center the map
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(function(position) {
                            let userLocation = {
                                lat: position.coords.latitude,
                                lng: position.coords.longitude
                            };
                            map.setCenter(userLocation);
                        }, function() {
                            handleLocationError(true, map.getCenter());
                        });
                    } else {
                        // Browser doesn't support Geolocation
                        handleLocationError(false, map.getCenter());
                    }

                    // pins for golf courses
                    let golfCourses = [
                        {% for course in golf_courses %}
                        {
                            name: "{{ course.name }}",
                            location: {lat: {{ course.latitude }}, lng: {{ course.longitude }}}
                        },
                        {% endfor %}
                    ];

                    golfCourses.forEach(function(course) {
                        let marker = new google.maps.Marker({
                            position: course.location,
                            map: map,
                            title: course.name
                        });
                    });
                }

                function handleLocationError(browserHasGeolocation, center) {
                    // Handle errors here
                }

                lng: position.coords.longitude
            };
            map.setCenter(userLocation);
        }, function() {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }

    // Add markers for golf courses
    let golfCourses = JSON.parse(document.getElementById('golf-courses-data').textContent);

    golfCourses.forEach(function(course) {
        let marker = new google.maps.Marker({
            position: course.location,
            map: map,
            title: course.name
        });
    });
}

function handleLocationError(browserHasGeolocation, center) {
    // Handle errors here
}

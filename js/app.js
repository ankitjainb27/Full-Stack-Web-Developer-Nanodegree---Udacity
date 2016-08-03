String.prototype.contains = function (other) {
    return this.indexOf(other) !== -1;
};

var defaultIcon = makeMarkerIcon('0091ff');
var highlightedIcon = makeMarkerIcon('FFFF24');

function makeMarkerIcon(markerColor) {
    var markerImage = new google.maps.MarkerImage(
        'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|' + markerColor +
        '|40|_|%E2%80%A2',
        new google.maps.Size(21, 34),
        new google.maps.Point(0, 0),
        new google.maps.Point(10, 34),
        new google.maps.Size(21, 34));
    return markerImage;
}

var Foursquare = function (restaurant, map) {
    var self = this;
    self.name = ko.observable(restaurant.name);
    self.location = restaurant.location;
    self.lat = self.location.lat;
    self.lng = self.location.lng;
    //map_location returns a computed observable of latitude and longitude
    self.map_location = ko.computed(function () {
        if (self.lat === 0 || self.lon === 0) {
            return null;
        } else {
            return new google.maps.LatLng(self.lat, self.lng);
        }
    });
    self.formattedAddress = ko.observable(self.location.formattedAddress);
    self.formattedPhone = ko.observable(restaurant.contact.formattedPhone);
    self.marker = (function (restaurant) {
        var marker;

        if (restaurant.map_location()) {
            marker = new google.maps.Marker({
                position: restaurant.map_location(),
                map: map,
                icon: defaultIcon
            });
        }
        return marker;
    })(self);
    self.id = ko.observable(restaurant.id);
    self.url = ko.observable(restaurant.url);
    self.formattedInfoWindowData = function () {
        return '<div class="info-window-content">' + '<a href="' + self.url() + '">' +
            '<span class="info-window-header">' + self.name() + '</span>' +
            '</a><p>' + self.formattedAddress() + '<br>' + self.formattedPhone() + '</p>' +
            '</div>';
    };
};

function initMap() {
    // Create a styles array to use with the map.
    var styles = [
        {
            featureType: 'water',
            stylers: [
                {color: '#19a0d8'}
            ]
        }, {
            featureType: 'administrative',
            elementType: 'labels.text.stroke',
            stylers: [
                {color: '#ffffff'},
                {weight: 6}
            ]
        }, {
            featureType: 'administrative',
            elementType: 'labels.text.fill',
            stylers: [
                {color: '#e85113'}
            ]
        }, {
            featureType: 'road.highway',
            elementType: 'geometry.stroke',
            stylers: [
                {color: '#efe9e4'},
                {lightness: -40}
            ]
        }, {
            featureType: 'transit.station',
            stylers: [
                {weight: 9},
                {hue: '#e85113'}
            ]
        }, {
            featureType: 'road.highway',
            elementType: 'labels.icon',
            stylers: [
                {visibility: 'off'}
            ]
        }, {
            featureType: 'water',
            elementType: 'labels.text.stroke',
            stylers: [
                {lightness: 100}
            ]
        }, {
            featureType: 'water',
            elementType: 'labels.text.fill',
            stylers: [
                {lightness: -100}
            ]
        }, {
            featureType: 'poi',
            elementType: 'geometry',
            stylers: [
                {visibility: 'on'},
                {color: '#f0e4d3'}
            ]
        }, {
            featureType: 'road.highway',
            elementType: 'geometry.fill',
            stylers: [
                {color: '#efe9e4'},
                {lightness: -25}
            ]
        }
    ];

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.725, lng: -74},
        zoom: 13,
        styles: styles,
        mapTypeControl: false
    });

    return map;
}

var AppViewModel = function () {
    var self = this;

    function initialize() {
        map = initMap();
        fetchSushiRestaurants();
    }

    if (typeof google !== 'object' || typeof google.maps !== 'object') {
        $('#search-summary').text("Could not load Google Maps API");
    }

    var map;
    var infoWindow = new google.maps.InfoWindow();
    self.sushiRestuarantList = ko.observableArray([]);
    self.numSushiRestaurant = ko.observable(0);
    self.query = ko.observable('');

    self.search = function () {
    };

    self.FilteredSushiRestuarantList= ko.computed(function () {
        self.sushiRestuarantList().forEach(function (restaurant) {
            restaurant.marker.setMap(null);
        });

        var results = ko.utils.arrayFilter(self.sushiRestuarantList(), function (restaurant) {
            return restaurant.name().toLowerCase().contains(self.query().toLowerCase());
        });

        results.forEach(function (restaurant) {
            restaurant.marker.setMap(map);
        });

        self.numSushiRestaurant(results.length);
        return results;
    });

    self.selectRestaurant = function (restaurant) {
        infoWindow.setContent(restaurant.formattedInfoWindowData());

        infoWindow.open(map, restaurant.marker);

        map.panTo(restaurant.marker.position);

        restaurant.marker.setAnimation(google.maps.Animation.BOUNCE);
        restaurant.marker.setIcon(highlightedIcon);
        self.sushiRestuarantList().forEach(function (old_restaurant) {
            if (restaurant != old_restaurant) {
                old_restaurant.marker.setAnimation(null);
                old_restaurant.marker.setIcon(defaultIcon);
            }
        });
    };
    function fetchSushiRestaurants() {
        var data;

        $.ajax({
            url: 'https://api.foursquare.com/v2/venues/search',
            dataType: 'json',
            data: 'client_id=TVCLSUOTWTNYYYNQXJLM2CM5LGMUQPNO0RAPW1O5WLMPWCQH%20&client_secret=SCRGCS4SBR5J1IDRRWTKBAUIM31YB4TUKMMRVRJOW13DC1PW%20&v=20130815%20&ll=40.7,-74%20&query=sushi',
            async: false,
        }).done(function (response) {
            data = response.response.venues;
            data.forEach(function (restaurant) {
                foursquare = new Foursquare(restaurant, map)
                self.sushiRestuarantList.push(foursquare);
            });
            self.sushiRestuarantList().forEach(function (restaurant) {
                if (restaurant.map_location()) {
                    google.maps.event.addListener(restaurant.marker, 'click', function () {
                        self.selectRestaurant(restaurant);
                    });
                }
            });
        }).fail(function (response, status, error) {
            $('#search-summary').text('Sushi Restaurants could not load...');
        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
};

ko.applyBindings(new AppViewModel());

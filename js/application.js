String.prototype.contains = function (other) {
    return this.indexOf(other) !== -1;
};

var Foursquare = function (meetup, map) {
    var self = this;
    self.name = ko.observable(meetup.name);
    self.location = meetup.location;
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
    self.formattedPhone = ko.observable(meetup.contact.formattedPhone);
    self.marker = (function (corner) {
        var marker;

        if (corner.map_location()) {
            marker = new google.maps.Marker({
                position: corner.map_location(),
                map: map
            });
        }

        return marker;
    })(self);
    self.id = ko.observable(meetup.id);
    self.url = ko.observable(meetup.url);
    self.formattedMeetupList = function () {
        return '<div class="info-window-content">' + '<a href="' + self.url() + '">' +
            '<span class="info-window-header">' + self.name() + '</span>' +
            '</a><p>' + self.formattedAddress() +'<br>'+ self.formattedPhone() + '</p>' +
            '</div>';
    };
};

var GoogleMap = function (center, element) {
    var mapOptions = {
        zoom: 13,
        center: center,
        mapTypeControlOptions: {
            mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'usroadatlas']
        },
        mapTypeControl: false,
        panControl: false,
        streetViewControl: false,
        zoomControl: false
    };

    map = new google.maps.Map(element, mapOptions);

    return map;
};

var AppViewModel = function () {
    var self = this;

    function initialize() {
        map = GoogleMap(center, mapCanvas);
        fetchMeetups();
    }

    if (typeof google !== 'object' || typeof google.maps !== 'object') {
        $('#search-summary').text("Could not load Google Maps API");
    }

    var map,
        mapCanvas = $('#map')[0],
        center = new google.maps.LatLng(40.725, -74); // New York

    var infoWindow = new google.maps.InfoWindow();

    self.meetupList = ko.observableArray([]);

    self.numCorners = ko.observable(0);

    self.query = ko.observable('');
    self.search = function () {
        // present to avoid page reload
    };
    self.filteredCornerList = ko.computed(function () {
        self.meetupList().forEach(function (corner) {
            corner.marker.setMap(null);
        });

        //To filter results based on search
        var results = ko.utils.arrayFilter(self.meetupList(), function (corner) {
            return corner.name().toLowerCase().contains(self.query().toLowerCase());
        });

        results.forEach(function (corner) {
            corner.marker.setMap(map);
        });

        self.numCorners(results.length);
        return results;
    });

    self.selectCorner = function (corner) {
        infoWindow.setContent(corner.formattedMeetupList());

        infoWindow.open(map, corner.marker);

        map.panTo(corner.marker.position);

        corner.marker.setAnimation(google.maps.Animation.BOUNCE);
        self.meetupList().forEach(function (old_corner) {
            if (corner != old_corner) {
                old_corner.marker.setAnimation(null);
            }
        });
    };
    function fetchMeetups() {
        var data;

        $.ajax({
            url: 'https://api.foursquare.com/v2/venues/search',
            dataType: 'json',
            data: 'client_id=TVCLSUOTWTNYYYNQXJLM2CM5LGMUQPNO0RAPW1O5WLMPWCQH%20&client_secret=SCRGCS4SBR5J1IDRRWTKBAUIM31YB4TUKMMRVRJOW13DC1PW%20&v=20130815%20&ll=40.7,-74%20&query=sushi',
            async: false,
        }).done(function (response) {
            data = response.response.venues;
            data.forEach(function (meetup) {
                foursquare = new Foursquare(meetup, map)
                self.meetupList.push(foursquare);
            });
            self.meetupList().forEach(function (meetup) {
                if (meetup.map_location()) {
                    google.maps.event.addListener(meetup.marker, 'click', function () {
                        self.selectCorner(meetup);
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

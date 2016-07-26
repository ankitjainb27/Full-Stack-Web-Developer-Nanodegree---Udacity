var meetupApiUrl = 'http://api.meetup.com/2/open_events?status=upcoming&radius=5&category=34&and_text=False&limited_events=False&text=coding+programming+ruby+python+javascript+html&desc=False&offset=0&photo-host=public&format=json&lat=41.878114&page=100&lon=-87.629798&sig_id=178346822&sig=1a186723262b63d4b2deee474b8d95bc0ec2ec9f';

String.prototype.contains = function (other) {
    return this.indexOf(other) !== -1;
};

var Corner = function (venueObject, map) {
    var self = this;

    self.lat = venueObject.lat;
    self.lon = venueObject.lon;
    self.location = ko.computed(function () {
        if (self.lat === 0 || self.lon === 0) {
            return null;
        } else {
            return new google.maps.LatLng(self.lat, self.lon);
        }
    });

    self.id = venueObject.id;
    self.name = ko.observable(venueObject.name);
    self.address = ko.observable(venueObject.address_1);

    self.meetups = ko.observableArray([]);

    self.marker = (function (corner) {
        var marker;

        if (corner.location()) {
            marker = new google.maps.Marker({
                position: corner.location(),
                map: map,
            });
        }

        return marker;
    })(self);

    self.formattedMeetupList = function () {
        meetupSubstring = '<ul class="info-window-list">';
        self.meetups().forEach(function (meetup) {
            meetupSubstring += '<li>' + '<a href="' + meetup.url() + '">' +
                meetup.name() +
                '</a>' + ' on ' + meetup.date() + '</li>';
        });
        meetupSubstring += '</ul>';
        return '<div class="info-window-content">' +
            '<span class="info-window-header">' + self.name() + '</span>' +
            '<p>' + self.address() + '</p>' +
            meetupSubstring +
            '</div>';
    };
};

/* Represents a Meetup event.
 * @constructor
 * @param {object} meetup - JSON-like meetup from the Meetup open_venue API
 */
var Meetup = function (meetup) {
    var self = this;

    // attach venue object
    self.venueObject = meetup.venue;

    // returns if the meetup has a venue that is listed
    self.hasVenue = ko.computed(function () {
        if (self.venueObject) {
            return true;
        } else {
            return false;
        }
    });

    self.id = ko.observable(meetup.id);
    self.name = ko.observable(meetup.name);
    self.group = ko.observable(meetup.group.name);

    // converts date in milliseconds to a human-friendly string, e.g. 1/2/2015
    self.date = ko.computed(function () {
        var milliseconds = meetup.time;
        var date = new Date(milliseconds);
        return date.toLocaleDateString();
    });
    self.url = ko.observable(meetup.event_url);
};

/* Represents a Google Map object */
var GoogleMap = function (center, element) {
    var mapOptions = {
        zoom: 14,
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
        fetchMeetups(meetupApiUrl);
    }

    if (typeof google !== 'object' || typeof google.maps !== 'object') {
        $('#search-summary').text("Could not load Google Maps API");
    }

    var map,
        mapCanvas = $('#map')[0],
        center = new google.maps.LatLng(41.8886, -87.6310); // Chicago

    var infoWindow = new google.maps.InfoWindow();

    self.meetupList = ko.observableArray([]);

    self.cornerList = ko.observableArray([]);

    self.numCorners = ko.observable(0);

    self.query = ko.observable('');

    self.search = function () {
        // empty function for future functionality, keep present to avoid page reload
    };

    self.filteredCornerList = ko.computed(function () {
        self.cornerList().forEach(function (corner) {
            corner.marker.setMap(null);
        });

        var results = ko.utils.arrayFilter(self.cornerList(), function (corner) {
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

        corner.marker.setAnimation(google.maps.Animation.DROP);
        self.cornerList().forEach(function (old_corner) {
            if (corner != old_corner) {
                old_corner.marker.setAnimation(null);
            }
        });
    };

    function fetchMeetups(url) {
        var data;

        // execute JSON-P request
        $.ajax({
            type: "GET",
            url: url,
            timeout: 5000,
            contentType: "application/json",
            dataType: "jsonp",
            cache: false,

            // when done
        }).done(function (response) {
            // pull `results` array from JSON
            data = response.results;

            data.forEach(function (meetup) {
                self.meetupList.push(new Meetup(meetup));
            });

            extractCorners();

            // if failed
        }).fail(function (response, status, error) {
            $('#search-summary').text('Meetup data could not load...');
        });
    }

    /* Parses through the meetupList and extracts Corner objects */
    function extractCorners() {
        // loop through meetup list
        self.meetupList().forEach(function (meetup) {
            // check if meetup object has a valid venue id
            if (meetup.hasVenue()) {
                var corner;
                var id = meetup.venueObject.id;

                // if exists
                if (hasCornerId(id)) {
                    // push the meetup object onto the corner's meetups
                    corner = getCornerById(id);
                    corner.meetups.push(meetup);

                    // if does not exist
                } else {
                    // instantiate a new corner object
                    corner = new Corner(meetup.venueObject, map);

                    // check if has valid location
                    if (corner.location()) {
                        // push it to the corner list
                        self.cornerList.push(corner);

                        // and push the meetup object onto that new corner object
                        corner.meetups.push(meetup);

                        // add a marker callback
                        google.maps.event.addListener(corner.marker, 'click', function () {
                            self.selectCorner(corner);
                        });
                    }
                }
            }
        });
    }

    function hasCornerId(id) {
        var result = false;
        self.cornerList().forEach(function (corner) {
            if (corner.id.toString() === id.toString()) {
                result = true;
            }
        });
        return result;
    }

    function getCornerById(id) {
        var foundCorner = null;
        if (hasCornerId(id)) {
            self.cornerList().forEach(function (corner) {
                if (corner.id.toString() === id.toString()) {
                    foundCorner = corner;
                }
            });
        }
        return foundCorner;
    }

    google.maps.event.addDomListener(window, 'load', initialize);
};

ko.applyBindings(new AppViewModel());

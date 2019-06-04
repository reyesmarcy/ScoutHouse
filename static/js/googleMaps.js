"use strict";

/**
 * This function will be called once the Google Maps API is finished loading.
 *
 * It adds a Google Map to the DOM with markers for each Hackbright campus.
 * Clicking on a marker will open an information window.
 */
function initMap() {
  const sfBayCoords = { lat: 37.601773, lng: -122.202870 };

  const map = new google.maps.Map(document.getElementById('map'), {
    center: sfBayCoords,
    zoom: 11
  });

  const icon = {
    url: '/static/img/marker.svg',
    scaledSize: new google.maps.Size(30, 30)
  };
  const sfMarker = addMarker(icon, sfBayCoords, 'SF Bay', map);
  sfMarker.addListener('click', () => alert('Hi!'));

  const locations = [
    {
      name: 'Hackbright Academy',
      coords: { lat: 37.7887459, lng: -122.4115852 }
    },
    {
      name: 'Powell Street Station',
      coords: { lat: 37.7844605, lng: -122.4079702 }
    },
    {
      name: 'Montgomery Station',
      coords: { lat: 37.7894094, lng: -122.4013037 }
    },
  ];

  // Loop over hackbrightLocations to make lots of markers
  const markers = locations.map(location => {
    return addMarker(icon, location.coords, location.name, map);
  });


  // Loop over markers list to attach click handlers
  markers.forEach(marker => {
    addInfoWindowToMarker(marker, map);
  });


/**
 * Utility/helper functions
 */

/**
 * addMarker() adds a marker with the given icon, position, and title to the
 * given map.
 *
 * TODO: add links to docs
 *
 * Parameters
 *   icon - an object defined using Google's Icon interface
 *   position - an object with lat, lng properties
 *   title - a title for the marker
 *   map - a Map object
 *
 * Return
 *   A Google Maps Marker object
 */
function addMarker(icon, position, title, map) {
  const marker = new google.maps.Marker({ position, map, title, icon });

  return marker;
}

/**
 * addInfoWindowToMarker() attaches the given infoWindow to the given marker.
 * It also attaches a click event handler to the marker.
 *
 * When the user clicks on a marker, it closes the previous infoWindow and opens
 * the infoWindow with the content for that marker.
 *
 * Parameters
 *   infoWindow - an InfoWindow object
 *   content - a string, the content displayed in the InfoWindow
 *   marker - a Marker object
 *   map - a Map object
 */
function addInfoWindowToMarker(marker, map) {
  const content = `<h1>${marker.title}</h1>
      <p>Located at</p>
      <ul>
        <li><b>Lat:</b> ${marker.position.lat()}</li>
        <li><b>Lng:</b> ${marker.position.lng()}</li>
      </ul>`;

  const infoWindow = new google.maps.InfoWindow({ 
    content,
    maxWidth: 200
  });

  marker.addListener('click', () => {
    infoWindow.open(map, marker);
  });
}

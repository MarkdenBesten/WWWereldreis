function loadMapScenario() {
    let map = new Microsoft.Maps.Map(document.getElementById('myMap'), {});
    let center = map.getCenter();
    //var Events = Microsoft.Maps.Events;
    let Location = Microsoft.Maps.Location;
    let Pushpin = Microsoft.Maps.Pushpin;

    let A = new Pushpin(new Location(center.latitude + 0.007, center.longitude - 0.01), {
        text: 'A',
        draggable: true
    });
    let B = new Pushpin(new Location(center.latitude + 0.007, center.longitude + 0.01), {
        text: 'B',
        draggable: true
    });
    let C = new Pushpin(new Location(center.latitude - 0.007, center.longitude + 0.01), {
        text: 'C',
        draggable: true
    });
    let D = new Pushpin(new Location(center.latitude - 0.007, center.longitude - 0.01), {
        text: 'D',
        draggable: true
    });
    map.entities.push([A, B, C, D]);

    document.getElementById("place-here").onclick = function () { placePinsHere() };

    function placePinsHere() {
        center = map.getCenter();
        A.setLocation(new Location(center.latitude + 0.007, center.longitude - 0.01));
        B.setLocation(new Location(center.latitude + 0.007, center.longitude + 0.01));
        C.setLocation(new Location(center.latitude - 0.007, center.longitude + 0.01));
        D.setLocation(new Location(center.latitude - 0.007, center.longitude - 0.01));
        map.entities.push([A, B, C, D]);
    }


    document.getElementById("show-loc").onclick = function () {showLocations()};
    function showLocations() {
        //document.getElementById('printoutPanel').innerHTML = '<b>A: </b>' + A.getLocation() +
         //   '<br><b>B: </b>' + B.getLocation() + '<br><b>C: </b>' + C.getLocation() + '<br>' +
         //   '<b>D: </b>' + D.getLocation() + '<br>';
        document.getElementById("id_Alat").value = A.getLocation().latitude;
        document.getElementById("id_Alon").value = A.getLocation().longitude;
        document.getElementById("id_Blat").value = B.getLocation().latitude;
        document.getElementById("id_Blon").value = B.getLocation().longitude;
        document.getElementById("id_Clat").value = C.getLocation().latitude;
        document.getElementById("id_Clon").value = C.getLocation().longitude;
        document.getElementById("id_Dlat").value = D.getLocation().latitude;
        document.getElementById("id_Dlon").value = D.getLocation().longitude;
    }
}

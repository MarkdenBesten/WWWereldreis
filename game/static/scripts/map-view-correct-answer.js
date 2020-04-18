function loadMapScenario() {
    let map = new Microsoft.Maps.Map(document.getElementById('myMap'), {});
    let Location = Microsoft.Maps.Location;

    let Alat = JSON.parse(document.getElementById("Alat").textContent);
    let Alon = JSON.parse(document.getElementById("Alon").textContent);
    let Blat = JSON.parse(document.getElementById("Blat").textContent);
    let Blon = JSON.parse(document.getElementById("Blon").textContent);
    let Clat = JSON.parse(document.getElementById("Clat").textContent);
    let Clon = JSON.parse(document.getElementById("Clon").textContent);
    let Dlat = JSON.parse(document.getElementById("Dlat").textContent);
    let Dlon = JSON.parse(document.getElementById("Dlon").textContent);

    map.setView({
        center: new Microsoft.Maps.Location(Alat - (Alat - Clat)/2, Alon - (Alon - Blon)/2),
        zoom: 12 //TODO find some way to zoom automatically
    });


    let polygon = new Microsoft.Maps.Polygon([
        new Microsoft.Maps.Location(Alat, Alon),
        new Microsoft.Maps.Location(Blat, Blon),
        new Microsoft.Maps.Location(Clat, Clon),
        new Microsoft.Maps.Location(Dlat, Dlon)], null);
    map.entities.push(polygon);


}
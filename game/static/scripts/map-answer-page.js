function loadMapScenario() {
    let map = new Microsoft.Maps.Map(document.getElementById('myMap'), {});
    let Location = Microsoft.Maps.Location;
    let Pushpin = Microsoft.Maps.Pushpin;
    let layer = new Microsoft.Maps.Layer();

    let Alat = JSON.parse(document.getElementById("Alat").textContent);
    let Alon = JSON.parse(document.getElementById("Alon").textContent);
    let Blat = JSON.parse(document.getElementById("Blat").textContent);
    let Blon = JSON.parse(document.getElementById("Blon").textContent);
    let Clat = JSON.parse(document.getElementById("Clat").textContent);
    let Clon = JSON.parse(document.getElementById("Clon").textContent);
    let Dlat = JSON.parse(document.getElementById("Dlat").textContent);
    let Dlon = JSON.parse(document.getElementById("Dlon").textContent);

    const locdata = [
        new Location(Alat, Alon),
        new Location(Blat, Blon),
        new Location(Clat, Clon),
        new Location(Dlat, Dlon)
    ];

    async function PlacePolygon() {
        let polygon = new Microsoft.Maps.Polygon(locdata, null);
        map.entities.push(polygon);
    }

    async function SetView(locdata) {
        let rect = Microsoft.Maps.LocationRect.fromLocations(locdata);
        map.setView({bounds: rect, padding: 80});
    }

    SetView(locdata);
    PlacePolygon();

    document.getElementById("show-answers").onclick = function () { ShowAnswers() };
    function ShowAnswers() {
        let answers = JSON.parse(document.getElementById("answers").textContent);
        let pin;

        for (i = 0, len = answers.length; i < len; i++) {
            pin = new Pushpin(new Location(answers[i][1], answers[i][2]), {color: 'red', title: answers[i][0]});
            layer.add(pin);
            locdata.push(new Location(answers[i][1], answers[i][2]));
        }
        map.layers.insert(layer);
        SetView(locdata);
    }
}
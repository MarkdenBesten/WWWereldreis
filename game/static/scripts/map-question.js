function loadMapScenario() {
    let map = new Microsoft.Maps.Map(document.getElementById('myMap'), {});
    let center = map.getCenter();
    let Location = Microsoft.Maps.Location;
    let Pushpin = Microsoft.Maps.Pushpin;

    let pin = new Pushpin(new Location(center.latitude, center.longitude), {draggable: true, color: 'blue'});
    map.entities.push(pin);

    document.getElementById("place-here").onclick = function () { placePinHere() };
    function placePinHere() {
        center = map.getCenter();
        pin.setLocation(new Location(center.latitude, center.longitude));
        map.entities.push(pin);
    }

    document.getElementById('give-answer').onclick = function () { giveAnswer() };
    function giveAnswer() {
        document.getElementById('id_latitude').value = pin.getLocation().latitude;
        document.getElementById('id_longitude').value = pin.getLocation().longitude;
        document.getElementById('id_Joker').value = 'Nee';
        document.getElementById('formulier').submit()

    }

    document.getElementById('use-joker').onclick = function () { useJoker() };
    function useJoker() {
        document.getElementById('id_Joker').value = 'Joker';
        document.getElementById('formulier').submit()
    }
}
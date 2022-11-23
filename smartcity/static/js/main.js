/*
File containing some javascript for website

@author: Dominik Vágner
@email: xvagne10@stud.fit.vutbr.cz
*/

$(document).ready(function() {
    if(window.location.pathname === '/new_ticket') {
        const lat = document.getElementById("latitude")
        const long = document.getElementById("longitude")

        let center = SMap.Coords.fromWGS84(15.7774239, 50.0375792);

        let new_ticket_map = new SMap(JAK.gel("new-ticket-map"), center, 13);
        new_ticket_map.addDefaultLayer(SMap.DEF_OPHOTO);
        new_ticket_map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        new_ticket_map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        new_ticket_map.addDefaultLayer(SMap.DEF_TURIST);
        new_ticket_map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        new_ticket_map.addDefaultLayer(SMap.DEF_HISTORIC);
        new_ticket_map.addDefaultLayer(SMap.DEF_BASE).enable();
        new_ticket_map.addDefaultControls();

        let layerSwitch = new SMap.Control.Layer({
            width: 65,
            items: 4,
            page: 4
        });
        layerSwitch.addDefaultLayer(SMap.DEF_BASE);
        layerSwitch.addDefaultLayer(SMap.DEF_OPHOTO);
        layerSwitch.addDefaultLayer(SMap.DEF_TURIST);
        layerSwitch.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        layerSwitch.addDefaultLayer(SMap.DEF_OPHOTO0406);
        layerSwitch.addDefaultLayer(SMap.DEF_OPHOTO0203);
        layerSwitch.addDefaultLayer(SMap.DEF_HISTORIC);
        new_ticket_map.addControl(layerSwitch, {left:"8px", top:"9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
        new_ticket_map.addControl(mouse);

        let new_ticket_layer = new SMap.Layer.Marker();
        new_ticket_map.addLayer(new_ticket_layer).enable();

        let mark = new SMap.Marker(center);
        mark.decorate(SMap.Marker.Feature.Draggable);
        new_ticket_layer.addMarker(mark);

        function start(e) {
            let node = e.target.getContainer();
            node[SMap.LAYER_MARKER].style.cursor = "help";
        }

        function stop(e) {
            let node = e.target.getContainer();
            node[SMap.LAYER_MARKER].style.cursor = "";
            let coords = e.target.getCoords();
            new SMap.Geocoder.Reverse(coords, change_location);
            lat.value = coords.y;
            long.value = coords.x;
        }

        function map_click(e, elm) {
            new_ticket_layer.removeAll()
            let coords = SMap.Coords.fromEvent(e.data.event, new_ticket_map);
            let mark = new SMap.Marker(coords);
            mark.decorate(SMap.Marker.Feature.Draggable);
            new_ticket_layer.addMarker(mark);
            new SMap.Geocoder.Reverse(coords, change_location);
            lat.value = coords.y;
            long.value = coords.x;
        }

        let change_location = function (geocoder) {
            let results = geocoder.getResults();
            const new_ticket_location = document.getElementById("new-ticket-location")
            new_ticket_location.innerText = results.label
        }

        let signals = new_ticket_map.getSignals();
        signals.addListener(window, "marker-drag-stop", stop);
        signals.addListener(window, "marker-drag-start", start);
        signals.addListener(window, "map-click", map_click)
    }


    ///////////////////////////////////////////////////////////////////////////////////////////////
    const btn = document.getElementById("logout_submit")

    btn.addEventListener("click", async (e) => {
        e.preventDefault()
        let url = window.location.origin + "/api/logout"
        const api_response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: "{}",
        });
        console.log(await api_response.json())
        window.location.assign(window.location.origin)
    });
});

function bootstrap_alert_macro(message, type) {
    return `
<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
    `
}
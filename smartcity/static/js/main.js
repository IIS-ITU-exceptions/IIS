/*
File containing some javascript for website

@author: Dominik Vágner
@email: xvagne10@stud.fit.vutbr.cz
*/

$(document).ready(async function () {
    if (window.location.pathname === '/new_ticket') {
        const lat = document.getElementById("latitude");
        const long = document.getElementById("longitude");

        let center = SMap.Coords.fromWGS84(15.7774239, 50.0375792);

        let nt_map = new SMap(JAK.gel("new-ticket-map"), center, 13);
        nt_map.addDefaultLayer(SMap.DEF_OPHOTO);
        nt_map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        nt_map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        nt_map.addDefaultLayer(SMap.DEF_TURIST);
        nt_map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        nt_map.addDefaultLayer(SMap.DEF_HISTORIC);
        nt_map.addDefaultLayer(SMap.DEF_BASE).enable();
        nt_map.addDefaultControls();

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
        nt_map.addControl(layerSwitch, {left: "8px", top: "9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
        nt_map.addControl(mouse);

        let nt_layer = new SMap.Layer.Marker();
        nt_map.addLayer(nt_layer).enable();

        let mark = new SMap.Marker(center);
        mark.decorate(SMap.Marker.Feature.Draggable);
        nt_layer.addMarker(mark);

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
            nt_layer.removeAll()
            let coords = SMap.Coords.fromEvent(e.data.event, nt_map);
            let mark = new SMap.Marker(coords);
            mark.decorate(SMap.Marker.Feature.Draggable);
            nt_layer.addMarker(mark);
            new SMap.Geocoder.Reverse(coords, change_location);
            lat.value = coords.y;
            long.value = coords.x;
        }

        let change_location = function (geocoder) {
            let results = geocoder.getResults();
            const new_ticket_location = document.getElementById("new-ticket-location")
            new_ticket_location.innerText = results.label
        }

        document.getElementById("map-my-location").addEventListener("click", map_my_location)
        function map_my_location() {
            let latitude;
            let longitude;
            const successCallback = (position) => {
                latitude = position.coords.latitude;
                longitude = position.coords.longitude;

                nt_layer.removeAll()
                let coords = SMap.Coords.fromWGS84(longitude, latitude);
                let mark = new SMap.Marker(coords);
                mark.decorate(SMap.Marker.Feature.Draggable);
                nt_layer.addMarker(mark);
                nt_map.setCenter(coords)

                new SMap.Geocoder.Reverse(coords, change_location);
                lat.value = coords.y;
                long.value = coords.x;
            };

            const errorCallback = (error) => {
              console.log(error);
            };

            const id = navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
            navigator.geolocation.clearWatch(id);
        }

        let signals = nt_map.getSignals();
        signals.addListener(window, "marker-drag-stop", stop);
        signals.addListener(window, "marker-drag-start", start);
        signals.addListener(window, "map-click", map_click);
    }

    if (window.location.pathname === '/map_of_tickets') {
        let center = SMap.Coords.fromWGS84(15.7774239, 50.0375792);

        let map = new SMap(JAK.gel("map-of-tickets"), center, 13);
        map.addDefaultLayer(SMap.DEF_OPHOTO);
        map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        map.addDefaultLayer(SMap.DEF_TURIST);
        map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        map.addDefaultLayer(SMap.DEF_HISTORIC);
        map.addDefaultLayer(SMap.DEF_BASE).enable();
        map.addDefaultControls();

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
        map.addControl(layerSwitch, {left: "8px", top: "9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM);
        map.addControl(mouse);

        let marker_layer = new SMap.Layer.Marker();
        map.addLayer(marker_layer).enable();

        const response = await get_tickets();
        let tickets = eval(response);
        tickets.forEach(function(value) {
            let c = new SMap.Card();
            c.setSize(350, 200);
            c.getHeader().innerHTML = "<strong>" + value.name + "</strong>";
            c.getBody().style.margin = "5px 0px";
            c.getBody().style.backgroundColor = "ddd";
            c.getBody().innerHTML = value.description;
            c.getFooter().innerHTML = "<strong>Created at</strong>:   " + value.created_at;

            let coords = SMap.Coords.fromWGS84(value.longitude, value.latitude);

            const dom = document.createElement('div');
            dom.className = 'svg-marker';

            if(value.state === "NEW") {
                dom.style = "fill: #ff0315";
                dom.classList.add("marker-new");
            } else if(value.state === "PLANNED") {
                dom.style = "fill: #1f80ff";
                dom.classList.add("marker-planned");
            } else if(value.state === "WORK_IN_PROGRESS") {
                dom.style = "fill: #ff7c00";
                dom.classList.add("marker-wip");
            } else {
                dom.style = 'fill: #00ae67';
                dom.classList.add("marker-done");
            }

            dom.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                                  <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/>
                             </svg>`;

            let options = {
                url: dom
            };

            let mark = new SMap.Marker(coords, "markerId" + value.id, options);
            mark.decorate(SMap.Marker.Feature.Card, c);
            marker_layer.addMarker(mark);
        });

        let signals = map.getSignals();
    }

    if (window.location.pathname === "/manager_ticket_view") {
        const lat = parseFloat(document.getElementById("latitude").innerText);
        const long = parseFloat(document.getElementById("longitude").innerText);

        let center = SMap.Coords.fromWGS84(long, lat);

        let map = new SMap(JAK.gel("manager-ticket-view-map"), center, 13);
        map.addDefaultLayer(SMap.DEF_OPHOTO);
        map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        map.addDefaultLayer(SMap.DEF_TURIST);
        map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        map.addDefaultLayer(SMap.DEF_HISTORIC);
        map.addDefaultLayer(SMap.DEF_BASE).enable();
        map.addDefaultControls();

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
        map.addControl(layerSwitch, {left: "8px", top: "9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM);
        map.addControl(mouse);

        let map_layer = new SMap.Layer.Marker();
        map.addLayer(map_layer).enable();

        let mark = new SMap.Marker(center);
        map_layer.addMarker(mark);
    }

    if (window.location.pathname === "/ticket_view") {
        const lat = parseFloat(document.getElementById("latitude").innerText);
        const long = parseFloat(document.getElementById("longitude").innerText);

        let center = SMap.Coords.fromWGS84(long, lat);

        let map = new SMap(JAK.gel("ticket-view-map"), center, 13);
        map.addDefaultLayer(SMap.DEF_OPHOTO);
        map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        map.addDefaultLayer(SMap.DEF_TURIST);
        map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        map.addDefaultLayer(SMap.DEF_HISTORIC);
        map.addDefaultLayer(SMap.DEF_BASE).enable();
        map.addDefaultControls();

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
        map.addControl(layerSwitch, {left: "8px", top: "9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM);
        map.addControl(mouse);

        let map_layer = new SMap.Layer.Marker();
        map.addLayer(map_layer).enable();

        let mark = new SMap.Marker(center);
        map_layer.addMarker(mark);
    }

    if (window.location.pathname === "/task_view") {
        const lat = parseFloat(document.getElementById("latitude").innerText);
        const long = parseFloat(document.getElementById("longitude").innerText);

        let center = SMap.Coords.fromWGS84(long, lat);

        let map = new SMap(JAK.gel("task-view-map"), center, 13);
        map.addDefaultLayer(SMap.DEF_OPHOTO);
        map.addDefaultLayer(SMap.DEF_OPHOTO0203);
        map.addDefaultLayer(SMap.DEF_OPHOTO0406);
        map.addDefaultLayer(SMap.DEF_TURIST);
        map.addDefaultLayer(SMap.DEF_TURIST_WINTER);
        map.addDefaultLayer(SMap.DEF_HISTORIC);
        map.addDefaultLayer(SMap.DEF_BASE).enable();
        map.addDefaultControls();

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
        map.addControl(layerSwitch, {left: "8px", top: "9px"});

        let mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM);
        map.addControl(mouse);

        let map_layer = new SMap.Layer.Marker();
        map.addLayer(map_layer).enable();

        let mark = new SMap.Marker(center);
        map_layer.addMarker(mark);
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


async function get_tickets() {
    const response = await fetch(window.location.origin + "/api/get_tickets");
    return await response.json()
}

function bootstrap_alert_macro(message, type) {
    return `
<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
    `
}
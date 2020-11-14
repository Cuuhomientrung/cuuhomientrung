import 'bootstrap';
import $ from 'jquery';
import Choices from 'choices.js'


$(document).ready(() => {
    // This code init ho_dan page only!
    if (!($('#search-button').length || $('#add-hodan').length)) return;

    // Init the choices.js instances :
    let choicesOptions = {
        noResultsText: "Không tìm thấy kết quả"
    };
    new Choices(document.getElementById('select-tinh'), choicesOptions);
    let selectHuyen = new Choices(document.getElementById('select-huyen'), choicesOptions);
    let selectXa = new Choices(document.getElementById('select-xa'), choicesOptions);

    $('#search-button').click(function() {
        let status = parseInt($("#select-status option:selected").val());
        let tinh = parseInt($("#select-tinh option:selected").val());
        let huyen = parseInt($("#select-huyen option:selected").val());
        let xa = parseInt($("#select-xa option:selected").val());
        let new_url = "/hodan/ds_hodan?";
        if (status >= 0) {
            new_url = new_url + "status=" + status + "&"
        }
        if (tinh >= 0) {
            new_url = new_url + "tinh=" + tinh + "&"
        }
        if (huyen >= 0) {
            new_url = new_url + "huyen=" + huyen + "&"
        }
        if (xa >= 0) {
            new_url = new_url + "xa=" + xa + "&"
        }
        document.location.href = new_url;
    });
    $('#select-tinh').on("change", function() {
        let tinh = $("#select-tinh option:selected").val();
        $.get('/get_huyen_api/?tinh=' + tinh, function(data, err) {
            $('#select-huyen').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả huyện");
            $("#select-huyen").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-huyen').append(ele);
            }

            // Update the choices for Huyen :
            // We have to update the choice as corrected array
            let listHuyen = Object.keys(data).map(key => {
                let item = {
                    value: key,
                    label: data[key]
                };

                return item;
            });

            // Then update the choices:
            selectHuyen.clearChoices();
            selectHuyen.setChoices(listHuyen);
        });

    });

    $('#select-huyen').on("change", function() {
        let huyen = $("#select-huyen option:selected").val();
        $.get('/get_xa_api/?huyen=' + huyen, function(data, err) {
            $('#select-xa').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả xã");
            $("#select-xa").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-xa').append(ele);
            }

            // Update the choices for Xa
            // We have to update the choice as corrected array
            let listXa = Object.keys(data).map(key => {
                let item = {
                    value: key,
                    label: data[key]
                };

                return item;
            });

            // Then update the choices:
            selectXa.clearChoices();
            selectXa.setChoices(listXa);
        });

    });
    $('#see-more-note').on("click", function() {
        $('.see-less').hide();
        $('.see-more').show();
    });
    $('#see-less-note').on("click", function() {
        $('.see-less').show();
        $('.see-more').hide();
    });
});

// Tự động lấy toạ độ dựa theo địa chỉ nhập vào

// Tìm kiếm theo quận(huyện)
var map;
$(document).ready(() => {
    if (!$('#add-hodan').length) return;

    mapboxgl.accessToken = 'pk.eyJ1IjoiZHp1bmdkYSIsImEiOiJja2drMDFka2wwMW9zMndxZW9lMXBud3d5In0.oKlf9RF-X-SKkUJUAQ9ndw';
    map = new mapboxgl.Map({
        container: 'map', // Container ID
        style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
        center: [106.393962, 15.925709], // Starting position [lng, lat]
        zoom: 6, // Starting zoom level, 
    });
    // Add zoom and rotation controls to the map.
    map.addControl(new mapboxgl.NavigationControl());
    /*var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
        });
    document.getElementById('geocoder').appendChild(geocoder.onAdd(map));*/
    //$('#id_address').keyup(function(event) {
    // Init the choices.js instances :
    $('#select-xa').on("change",function() {
        var hodan_address = $('#hodan_address').val();
        var hodan_tinh = $('#select-tinh option:selected').text();
        var hodan_huyen = $('#select-huyen option:selected').text();
        var hodan_xa = $('#select-xa option:selected').text();
        var serch_text = hodan_address+"%"+hodan_xa+",%"+hodan_huyen+",%"+hodan_tinh
        serch_text = serch_text.replace(" ","%")
        //var end_point = 'https://api.mapbox.com/geocoding/v5/mapbox.places/serch_text.json?country=VN&limit=1&access_token=pk.eyJ1IjoiZHp1bmdkYSIsImEiOiJja2drMDFka2wwMW9zMndxZW9lMXBud3d5In0.oKlf9RF-X-SKkUJUAQ9ndw'
        //end_point = end_point.replace("serch_text",serch_text)
        //window.alert(end_point);
        $.get('https://maps.googleapis.com/maps/api/geocode/json?', {address: serch_text, key: 'AIzaSyBf5XFkZFZao0gwC6rO_J8MWZBAMPg6v-w'}, function(response) {
            if (response.status === "OK") {
                var location = response.results[0].geometry.location
                //window.alert(location.lat);
                var marker = new mapboxgl.Marker() // Initialize a new marker
                                .setLngLat([location.lng,location.lat]) // Marker [lng, lat] coordinates
                                .addTo(map); // Add the marker to the map
                $('#hodan_geo_lng').val(location.lng)
                $('#hodan_geo_lat').val(location.lat)
                map.flyTo({
                    center: [location.lng,location.lat],
                    speed: 0.5,
                    zoom: 9
                    });
            } else {
                //window.alert(response.status);
                //showAlert("{\"status\":\"error\",\"context\":\"Address not found!\nCustomer: " + cusName + "\nAddress: " + cusAddress + " was not found!\"}");
            }
        });
        /*$.get(end_point, function(data,err) {
            if (!err) {
               
                var location = data.features.geometry.coordinates
                console.log( location );
                var marker = new mapboxgl.Marker() // Initialize a new marker
                                .setLngLat(location) // Marker [lng, lat] coordinates
                                .addTo(map); // Add the marker to the map
            } else {
                console.log( typeof data );
                console.log( err );
            }
        });*/
    });
});

//mapview
var currentMarkers=[];

function removeAllMarkers(){
    if (currentMarkers!==null) {
        for (var i = currentMarkers.length - 1; i >= 0; i--) {
          currentMarkers[i].remove();
        }
    }
}

function hodanchitiet(id){
    //window.alert(id)
    $.get('/xem_hodan/?id='+id, function(jsonResponse) {
        $("#hodan_id").text(jsonResponse.id);
        $("#hodan_name").text(jsonResponse.name);
        $("#hodan_status").text(jsonResponse.status);
        $("#hodan_status").attr('class',"badge  badge-danger")
        $("#hodan_people_number").text(jsonResponse.people_number);
        $("#hodan_do_quan_trong").text(jsonResponse.do_quan_trong);
        $("#hodan_nhucau").text(jsonResponse.hodan_nhucau);
        $("#hodan_note").text(jsonResponse.note);
        $("#hodan_address").text(jsonResponse.address);
        $("#hodan_phone").text(jsonResponse.phone);
        $("#hodan_volunteer").text(jsonResponse.volunteer);
        $("#hodan_cuuho").text(jsonResponse.cuuho);
        $("#hodan_created_time").text(jsonResponse.created_time);
        $("#hodan_update_time").text(jsonResponse.update_time);
        $("#myModal").modal();
    });
}

function addMarkerToMap(jsonResponse){
    $.each(jsonResponse, function(index, value) {
        //window.alert(value.geo_lat_lon.lat)
        var popup = new mapboxgl.Popup().setHTML('<h5>'+ value.name+'</h5><h5>'+value.hodan_nhucau+'</h5><h5>'+value.do_quan_trong+'</h5><br/><input type="hidden" value="'+value.id+'" id="hodanid" name="hodanid" /><button class="btn btn-outline-primary" id="btnhodanchitiet" >Chi tiết</button><button class="btn btn-outline-danger" id="btpopup_close">Đóng</button>')
        var marker = new mapboxgl.Marker({color:value.marker_color}) // Initialize a new marker
                            .setLngLat([value.geo_lat_lon.lng,value.geo_lat_lon.lat]) // Marker [lng, lat] coordinates
                            .setPopup(popup) // add popup
                            .addTo(map); // Add the marker to the map
        popup.on('open', function(){
            $('#btnhodanchitiet').click(function(){
                let hodanid = $('#hodanid').val();
                //window.alert("maker on click")
                hodanchitiet(hodanid)
                popup.remove();
            });
            $('#btpopup_close').click(function(){
                popup.remove();
            });
        });
        currentMarkers.push(marker)
    });
}

$(document).ready(() => {
    if (!$('#search-map-hodan').length) return;

    mapboxgl.accessToken = 'pk.eyJ1IjoiZHp1bmdkYSIsImEiOiJja2drMDFka2wwMW9zMndxZW9lMXBud3d5In0.oKlf9RF-X-SKkUJUAQ9ndw';
    map = new mapboxgl.Map({
        container: 'map', // Container ID
        style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
        center: [106.393962, 15.925709], // Starting position [lng, lat]
        zoom: 6, // Starting zoom level, 
    });
    // Add zoom and rotation controls to the map.
    map.addControl(new mapboxgl.NavigationControl());
    /*var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
        });
    document.getElementById('geocoder').appendChild(geocoder.onAdd(map));*/
    //$('#id_address').keyup(function(event) {
    $.get('/get_init_map_api/', function(jsonResponse) {
        addMarkerToMap(jsonResponse);
    });
    // Init the choices.js instances :
    let choicesOptions = {
        noResultsText: "Không tìm thấy kết quả"
    };
    new Choices(document.getElementById('select-tinh'), choicesOptions);
    let selectHuyen = new Choices(document.getElementById('select-huyen'), choicesOptions);
    let selectXa = new Choices(document.getElementById('select-xa'), choicesOptions);

    $('#select-tinh').on("change", function() {
        let tinh = $("#select-tinh option:selected").val();
        $.get('/get_huyen_api/?tinh=' + tinh, function(data, err) {
            $('#select-huyen').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả huyện");
            $("#select-huyen").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-huyen').append(ele);
            }

            // Update the choices for Huyen :
            // We have to update the choice as corrected array
            let listHuyen = Object.keys(data).map(key => {
                let item = {
                    value: key,
                    label: data[key]
                };

                return item;
            });

            // Then update the choices:
            selectHuyen.clearChoices();
            selectHuyen.setChoices(listHuyen);
        });
        removeAllMarkers()
        $.get('/get_init_map_api/?tinh=' + tinh, function(jsonResponse) {
            addMarkerToMap(jsonResponse);
        });

    });
    $('#select-huyen').on("change", function() {
        let huyen = $("#select-huyen option:selected").val();
        $.get('/get_xa_api/?huyen=' + huyen, function(data, err) {
            $('#select-xa').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả xã");
            $("#select-xa").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-xa').append(ele);
            }

            // Update the choices for Xa
            // We have to update the choice as corrected array
            let listXa = Object.keys(data).map(key => {
                let item = {
                    value: key,
                    label: data[key]
                };

                return item;
            });

            // Then update the choices:
            selectXa.clearChoices();
            selectXa.setChoices(listXa);
        });
        removeAllMarkers()
        $.get('/get_init_map_api/?huyen=' + huyen, function(jsonResponse) {
            addMarkerToMap(jsonResponse);
        });
    });
    $('#select-xa').on("change",function() {
        var hodan_address = $('#hodan_address').val();
        var hodan_tinh = $('#select-tinh option:selected').text();
        var hodan_huyen = $('#select-huyen option:selected').text();
        var hodan_xa = $('#select-xa option:selected').text();
        var serch_text = hodan_address+"%"+hodan_xa+",%"+hodan_huyen+",%"+hodan_tinh
        serch_text = serch_text.replace(" ","%")
        //var end_point = 'https://api.mapbox.com/geocoding/v5/mapbox.places/serch_text.json?country=VN&limit=1&access_token=pk.eyJ1IjoiZHp1bmdkYSIsImEiOiJja2drMDFka2wwMW9zMndxZW9lMXBud3d5In0.oKlf9RF-X-SKkUJUAQ9ndw'
        //end_point = end_point.replace("serch_text",serch_text)
        //window.alert(end_point);
        $.get('https://maps.googleapis.com/maps/api/geocode/json?', {address: serch_text, key: 'AIzaSyBf5XFkZFZao0gwC6rO_J8MWZBAMPg6v-w'}, function(response) {
            if (response.status === "OK") {
                var location = response.results[0].geometry.location
                //window.alert(location.lat);
                var marker = new mapboxgl.Marker() // Initialize a new marker
                                .setLngLat([location.lng,location.lat]) // Marker [lng, lat] coordinates
                                .addTo(map); // Add the marker to the map
                $('#hodan_geo_lng').val(location.lng)
                $('#hodan_geo_lat').val(location.lat)
                map.flyTo({
                    center: [location.lng,location.lat],
                    speed: 0.5,
                    zoom: 9
                    });
            } else {
                //window.alert(response.status);
                //showAlert("{\"status\":\"error\",\"context\":\"Address not found!\nCustomer: " + cusName + "\nAddress: " + cusAddress + " was not found!\"}");
            }
        });
        removeAllMarkers()
        let xa_id = $("#sselect-xa option:selected").val()
        $.get('/get_init_map_api/?xa=' + xa_id, function(jsonResponse) {
            addMarkerToMap(jsonResponse);
        });
    });

    $('#select-status').on("change", function() {
        let status = $("#select-status option:selected").val();
        removeAllMarkers()
        $.get('/get_init_map_api/?status=' + status, function(jsonResponse) {
            addMarkerToMap(jsonResponse);
        });
    });
});


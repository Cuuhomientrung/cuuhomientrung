import 'bootstrap';
import $ from 'jquery';
import Choices from 'choices.js'


$(document).ready(() => {
    // This code init ho_dan page only!
    if (!$('#search-button').length) return;

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
        let new_url = "/ho_dan?";
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

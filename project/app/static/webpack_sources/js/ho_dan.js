import 'bootstrap';
import $ from 'jquery';

$(document).ready(() => {
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
        $.get('/get_huyen_api/?tinh='+tinh, function(data, err) {
            $('#select-huyen').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả huyện");
            $("#select-huyen").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-huyen').append(ele);
            }
		});
    });
    $('#select-huyen').on("change", function() {
        let huyen = $("#select-huyen option:selected").val();
        $.get('/get_xa_api/?huyen='+huyen, function(data, err) {
            $('#select-xa').find('option').remove();
            let ele = $('<option></option>').attr("value", -1).text("Tất cả xã");
            $("#select-xa").append(ele);
            for (let key in data) {
                let ele = $('<option></option>').attr("value", key).text(data[key]);
                $('#select-xa').append(ele);
            }
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

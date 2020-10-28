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
            let list_option = '<option value="-1"> Tất cả huyện </option>';
            for (let key in data) {
                list_option += '<option value="' + key + '"> ' + data[key] + ' </option>';
            }
            $("#select-tinh").children(list_option);
		});


        if (tinh == "-1") {
            $("#select-huyen option").show();
        } else {
            $("#select-huyen option").hide();
            $("#select-huyen option[tinh-id=" + tinh + "]").show();
        }
        $("#select-huyen option[value=-1]").show();
        $("#select-huyen option").removeAttr("selected");
    });
    $('#select-huyen').on("change", function() {
        let huyen = $("#select-huyen option:selected").val();
        if (huyen == "-1") {
            $("#select-xa option").show();
        } else {
            $("#select-xa option").hide();
            $("#select-xa option[huyen-id=" + huyen + "]").show();
        }
        $("#select-xa option[value=-1]").show();
        $("#select-xa option").removeAttr("selected");
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

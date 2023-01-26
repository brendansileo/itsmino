$(document).ready(function() {
    $("#cutoff_choice").change(function() {
        reload();
    });
});

function reload() {
    var cutoff = $("#cutoff_choice").val();
    $.ajax({
        url: '/map/'+cutoff,
        success: function(response) {
            $('#list_container').html(response);
        }
    });
}
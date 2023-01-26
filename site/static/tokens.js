function get_tokens() {
    url = $('#url').val();
    id = url.split('/').pop();
    $.get('http://itsmino.tk:8080/tokens/'+id, function(data) {
        $('#output').text(data);
    });
}
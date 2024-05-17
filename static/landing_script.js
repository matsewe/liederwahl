$(document).ready(function () {
    var s_id = localStorage.getItem('session_id')
    if (s_id === null) {
        s_id = window.crypto.randomUUID();
        localStorage.setItem('session_id', s_id)
    }
    $('.vote-from-existing').attr('href', '?session_id=' + s_id);
});

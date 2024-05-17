document.addEventListener('DOMContentLoaded', function () {
    const eles = document.getElementsByClassName('categories');
    Array.prototype.forEach.call(eles, ele => {


        //ele.style.cursor = 'grab';

        let pos = { top: 0, left: 0, x: 0, y: 0 };

        const mouseDownHandler = function (e) {
            ele.style.cursor = 'grabbing';
            ele.style.userSelect = 'none';

            pos = {
                left: ele.scrollLeft,
                top: ele.scrollTop,
                // Get the current mouse position
                x: e.clientX,
                y: e.clientY,
            };

            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        };

        const mouseMoveHandler = function (e) {
            // How far the mouse has been moved
            const dx = e.clientX - pos.x;
            const dy = e.clientY - pos.y;

            // Scroll the element
            ele.scrollTop = pos.top - dy;
            ele.scrollLeft = pos.left - dx;
        };

        const mouseUpHandler = function () {
            ele.style.cursor = 'grab';
            ele.style.removeProperty('user-select');

            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };

        // Attach the handler
        ele.addEventListener('mousedown', mouseDownHandler);
    });
});

const getQueryParameter = (param) => new URLSearchParams(document.location.search.substring(1)).get(param);

$(document).ready(function () {
    var session_id = getQueryParameter("session_id");

    $(".greeting-id").append(session_id);
    $(".greeting-id").append("Foo");
    $.ajax({
        url: "/songs"
    }).then(function (user_list) {
        $('.greeting-id').append(user_list.total);
        localStorage.setItem("test-storage", user_list.total);
        var users = [];
        $.each(user_list.data, function (key, user) {
            users.push("<li id='" + user.id + "'>" + user.first_name + "</li>");
        });
        $("<ul/>", {
            "class": "my-new-list",
            html: users.join("")
        }).appendTo("body");
    });
});

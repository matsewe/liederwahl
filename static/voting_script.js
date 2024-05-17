function makeScroll() {
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
}

function vote(song_id, vote) {
    var session_id = getQueryParameter("session_id");

    no_button = $("#song-" + song_id).find(".button-no")
    yes_button = $("#song-" + song_id).find(".button-yes")
    neutral_button = $("#song-" + song_id).find(".button-neutral")

    no_button.removeClass("selected")
    yes_button.removeClass("selected")
    neutral_button.removeClass("selected")

    switch (vote) {
        case 0:
            neutral_button.addClass("selected")
            break;
        case 1:
            yes_button.addClass("selected")
            break;
        case -1:
            no_button.addClass("selected")
        default:
            break;
    }

    $.ajax({
        url: "/songs/" + song_id + "/vote?" + $.param({ user_id: session_id, vote: vote }),
        method: "POST"
    })
}

const getQueryParameter = (param) => new URLSearchParams(document.location.search.substring(1)).get(param);

$(document).ready(function () {
    var session_id = getQueryParameter("session_id");

    var songTemplate = $('script[data-template="song"]').text().split(/\$\{(.+?)\}/g);

    function render(props) {
        return function(tok, i) { return (i % 2) ? props[tok] : tok; };
    }

    song_list = {}

    $.ajax({
        url: "/songs",
        data: { user_id: session_id }
    }).then(function (songs) {
        $.each(songs, function (key, song) {

            var mc = song.main_category;

            if (!(mc in song_list)) {
                song_list[mc] = ""
            }

            var cats = ""
            var cat_id = 1
            $.each(song.categories, function (cat_name, is_cat) {
                if (is_cat) {
                    cats = cats + '<span class="cat-' + cat_id + '">' + cat_name + '</span>';
                }
                cat_id += 1
            });

            
            var s = songTemplate.map(render({
                "id" : song.id,
                "title" : song.og_artist + ": " + song.title,
                "cover_image" : "cover.jpg",
                "no_selected" : (song.vote == -1) ? "selected" : "",
                "neutral_selected" : (song.vote == 0) ? "selected" : "",
                "yes_selected" : (song.vote == 1) ? "selected" : "",
                "categories" : cats
            })).join('')

            song_list[mc] += s
        });
        $.each(song_list, function(mc, s) {
            $('body').append("<h1>" + mc + "</h1>");
            $('body').append(s);
        });
    });
});

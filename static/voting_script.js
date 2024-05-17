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

var all_songs = {}

$(document).ready(function () {
    var session_id = getQueryParameter("session_id");

    var songTemplate = $('script[data-template="song"]').text().split(/\$\{(.+?)\}/g);

    function render(props) {
        return function (tok, i) { return (i % 2) ? props[tok] : tok; };
    }



    $.ajax({
        url: "/songs/",
        data: { user_id: session_id }
    }).then(function (songs) {
        song_list = {}

        cat_to_id = {}

        $.each(songs, function (key, song) {

            all_songs[song.id] = song;

            var mc = song.main_category;

            if (!song.is_aca) {
                mc = "Wildcard"
            }
            if (!(mc in song_list)) {
                song_list[mc] = ""
            }

            var cats = ""
            var cat_id = 1
            $.each(song.categories, function (cat_name, is_cat) {
                if (is_cat) {
                    cats = cats + '<span class="cat-' + cat_id + '">' + cat_name + '</span>';
                }
                cat_to_id[cat_name] = cat_id
                cat_id += 1
            });
            cat_to_id["Wildcard"] = cat_id


            artist = "";
            if (song.og_artist) {
                artist += song.og_artist;
                if (song.aca_artist && (song.aca_artist !== song.og_artist)) {
                    artist += " / ";
                    artist += song.aca_artist;
                }
            } else {
                artist = song.aca_artist;
            }

            var s = songTemplate.map(render({
                "id": song.id,
                "title": song.title,
                "artist": artist, //song.og_artist + ": " + song.aca_artist
                "cover_image": song.thumbnail,
                "no_selected": (song.vote == -1) ? "selected" : "",
                "neutral_selected": (song.vote == 0) ? "selected" : "",
                "yes_selected": (song.vote == 1) ? "selected" : "",
                "categories": cats
            })).join('')

            song_list[mc] += s
        });
        $.each(cat_to_id, function (cat_name, cat_id) {
            if (cat_name in song_list) {
                $('#songs').append("<h1 class=\"cat-" + cat_id + "\">" + cat_name + "</h1>");
                $('#songs').append(song_list[cat_name]);
            }
        });

        makeScroll();
    });
});

var is_playing = -1;

var spotify_embed_controller;

window.onSpotifyIframeApiReady = (IFrameAPI) => {
    const element = document.getElementById('spotify-embed');
    const options = {
      width: '640',
      height: '360'
    };
    const callback = (EmbedController) => {
        spotify_embed_controller = EmbedController;
    };
    IFrameAPI.createController(element, options, callback);
  };


function play(id) {
    $("#yt-player").css("display", "none");
    $("#spotify-player").css("display", "none");
    $("#close-player").css("display", "none");
    $("#yt-player").html("");
    spotify_embed_controller.pause();

    if (is_playing == id) {
        is_playing = -1;
    } else {
        is_playing = id;

        song = all_songs[id];
        yt_id = song.yt_url.split('v=')[1]
        spotify_id = song.yt_url.split('/track/')[1]

        if (yt_id) {
            $("#yt-player").css("display", "flex");
            $("#close-player").css("display", "block");
            iframe_code = '<iframe src="https://www.youtube.com/embed/' + yt_id + '?autoplay=1" title="" width="640" height="360" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"  allowFullScreen></iframe>';
            $("#yt-player").html(iframe_code);
        }
        else if (spotify_id) {
            $("#spotify-player").css("display", "flex");
            $("#close-player").css("display", "block");
            spotify_embed_controller.loadUri("spotify:track:" + spotify_id);
            spotify_embed_controller.play();
        }
        else {
            $("#yt-player").css("display", "none");
            $("#spotify-player").css("display", "none");
            $("#yt-player").html("");
            spotify_embed_controller.pause();
            window.open(song.yt_url, '_blank').focus();
        }
    }
}

//<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/2DS7lDZNFM7safSGNm8vd4?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

// https://open.spotify.com/intl-de/track/2DS7lDZNFM7safSGNm8vd4
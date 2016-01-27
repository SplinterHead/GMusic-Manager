function add_initial_stats(songCount,artistCount,albumCount) {
    var content = 'You have ' + songCount + ' songs by ' + artistCount + ' artists over ' + albumCount + ' albums.';
    document.getElementById("count_statistic").innerHTML = content;
}

window.onload = function() {
    add_initial_stats(1,2,3);
}
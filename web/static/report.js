document.addEventListener('DOMContentLoaded', function() {
    var imgTest = new Image();
    var albumCovers = document.getElementsByClassName('albumart');
    for (var albumCover in albumCovers) {
        imgTest.src = albumCover.getAttr('src');
        if (imgTest.width != imgTest.height) {
            albumCover.className = 'albumart irregular'; }
        else if (imgTest.width < '200px') {
            albumCover.className = 'albumart low'; }
        else if (imgTest.width < '500px') {
            albumCover.className = 'albumart medium'; }
        else {
            albumCover.className = 'albumart high'; }
    }
}, false);
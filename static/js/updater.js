setInterval(function() {
    var myImageElement = document.getElementById('image');

    myImageElement.src = 'static/img0.jpg?rand=' + Math.random();    

}, 300);

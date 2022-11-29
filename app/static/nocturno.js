function modo_noche(){
    if(document.body.style.backgroundColor == "white"){
        $('body').css("background-color", "black");
        $('header').css("background-color", "black");
        $('main').css("background-color", "black");
        $('aside').css("background-color", "black");
        $('footer').css("background-color", "black");
        $('h1').css("color", "white");
        $('h3').css("color", "white");
        $('h4').css("color", "white");
        $('th').css("color", "white");
        $('td').css("color", "white");
        $('label').css("color", "white");
    }

    else{
        $('body').css("background-color", "white");
        $('header').css("background-color", "white");
        $('main').css("background-color", "white");
        $('aside').css("background-color", "white");
        $('footer').css("background-color", "white");
        $('h1').css("color", "black");
        $('h3').css("color", "black");
        $('h4').css("color", "black");
        $('th').css("color", "black");
        $('td').css("color", "black");
        $('label').css("color", "black");
    }
}

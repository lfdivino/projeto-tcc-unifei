$("#nav").addClass("js").before('<div id="menu">&#9776;</div>');
$("#menu").click(function(){
    $("#nav").toggle();
});

$(document).ready(function() {
    if(window.innerWidth > 768) {
        $("#nav").removeAttr("style");
        $(".resposta_1").text("Muito Ruim");
        $(".resposta_2").text("Ruim");
        $(".resposta_3").text("Neutro");
        $(".resposta_4").text("Bom");
        $(".resposta_5").text("Muito Bom");
    }
    if(window.innerWidth < 768) {
        $(".resposta_1").text("1");
        $(".resposta_2").text("2");
        $(".resposta_3").text("3");
        $(".resposta_4").text("4");
        $(".resposta_5").text("5");
    }
});

$(window).resize(function(){
    if(window.innerWidth > 768) {
        $("#nav").removeAttr("style");
        $(".resposta_1").text("Muito Ruim");
        $(".resposta_2").text("Ruim");
        $(".resposta_3").text("Neutro");
        $(".resposta_4").text("Bom");
        $(".resposta_5").text("Muito Bom");
    }
    if(window.innerWidth < 768) {
        $(".resposta_1").text("1");
        $(".resposta_2").text("2");
        $(".resposta_3").text("3");
        $(".resposta_4").text("4");
        $(".resposta_5").text("5");
    }
});

$(".btn-respostas").click(function(){
    var col = $(this).parent();
    var row = col.parent();
    var panel_body = row.parent();
    var panel = panel_body.parent();
    var div_pergunta = panel.parent().attr('id');
    respostateste = {
        id_pergunta: div_pergunta,
        resposta: $(this).val(),
        login: $("#login").val(),
        password: $("#password").val()
    };

    $.ajax({
        url: '/api/respostas/',
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(respostateste),
        success:function(result){
            if (result['resposta']){
                $("#" + div_pergunta).remove();
                if ($(".perguntas").length != 0){
                    $(".invisivel:first").removeClass("invisivel");
                } else {
                    $(".sem-perguntas").removeClass("invisivel");
                }

            } else {
                alert(result['resposta']);
            }
        },
        error: function(result){
            alert("Aconteceu um problema ao gravar a resposta");
        }
    });
});
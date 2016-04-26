$("#nav").addClass("js").before('<div id="menu">&#9776;</div>');
$("#menu").click(function(){
    $("#nav").toggle();
});
$(window).resize(function(){
    if(window.innerWidth > 768) {
        $("#nav").removeAttr("style");
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
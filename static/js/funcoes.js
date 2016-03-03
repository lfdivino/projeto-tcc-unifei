$(".btn-block").click(function(){
    var col = $(this).parent();
    var row = col.parent();
    var div_pergunta = row.parent().attr('id');
    respostateste = {
        id_pergunta: div_pergunta,
        resposta: $(this).val()
    };

    $.ajax({
        url: '/respostateste/',
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify(respostateste),
        success:function(result){
            $("#" + div_pergunta).remove();
            $(".invisivel:first").removeClass("invisivel");
        },
        error: function(result){
            alert("Aconteceu um problema ao gravar a resposta");
        }
    });
});
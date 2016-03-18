$(document).ready(function() {
    $.ajax({
        url: '/api/perguntas/',
        type: 'GET',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success:function(result){
            $.each(result, function(i, pergunta) {
                $("#pergunta").append($('<option>', {
                    value: pergunta.id,
                    text: pergunta.pergunta
                }));
            });
        },
        error: function(result){
            alert("Aconteceu um problema ao buscar as respostas do sistema");
        }
    });
});

$("#tipo_exibicao_dados").change(function(){
    if ($(this).val() == "grafico") {
        $("#tipo_grafico").removeClass("invisivel");
    }else{
        $("#tipo_grafico").addClass("invisivel");
        if ($("#pergunta").hasClass("invisivel") == false) {
            $("#pergunta").addClass("invisivel");
        }
    }
});

$("#tipo_grafico").change(function(){
    if ($(this).val() == "grafico_pizza") {
        $("#pergunta").removeClass("invisivel");
    } else {
        $("#pergunta").addClass("invisivel");
    }
});
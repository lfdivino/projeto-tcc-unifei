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

$("#btn_gerar_informacao_visual").click(function(){
    if ($("#pergunta").hasClass("invisivel") == false) {
        gerar_grafico_pizza_pergunta($("#pergunta").val());
        $("#titulo_analise").html("<h2>" + $("#pergunta option:selected").text() + "</h2>");
    }
});

function gerar_grafico_pizza_pergunta(id_pergunta) {
    var respostas_1 = ['1', 0];
    var respostas_2 = ['2', 0];
    var respostas_3 = ['3', 0];
    var respostas_4 = ['4', 0];
    var respostas_5 = ['5', 0];
    $.ajax({
        url: '/api/respostas/' + id_pergunta,
        type: 'GET',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success:function(result){
            $.each(result, function(i, resposta) {
                switch (resposta.resposta) {
                    case 1:
                        respostas_1[1] = respostas_1[1] + 1;
                    break;
                    case 2:
                        respostas_2[1] = respostas_2[1] + 1;
                    break;
                    case 3:
                        respostas_3[1] = respostas_3[1] + 1;
                    break;
                    case 4:
                        respostas_4[1] = respostas_4[1] +1;
                    break;
                    case 5:
                        respostas_5[1] = respostas_5[1] + 1;
                    default:
                        console.log("Desculpe, estamos sem nenhuma resposta.");
                    }
            });
            
            var chart = c3.generate({
                data: {
                    // iris data from R
                    columns: [
                        respostas_1,
                        respostas_2,
                        respostas_3,
                        respostas_4,
                        respostas_5
                    ],
                    type : 'pie',
                    onclick: function (d, i) { console.log("onclick", d, i); },
                    onmouseover: function (d, i) { console.log("onmouseover", d, i); },
                    onmouseout: function (d, i) { console.log("onmouseout", d, i); }
                }
            });
        },
        error: function(result){
            alert("Aconteceu um problema ao buscar as respostas do sistema");
        }
    });
}
//var chart = c3.generate({
//    data: {
//        x : 'x',
//        columns: [
//            ['x', '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01'],
//            ['data1', 30, 200, 100, 400, 150, 250],
//            ['data2', 130, 100, 140, 200, 150, 50],
//            ['data3', 130, -150, 200, 300, -200, 100]
//        ],
//        type: 'bar'
//    },
//    axis: {
//        x: {
//            type: 'category',
//            tick: {
//                rotate: 75,
//                multiline: false
//            },
//            height: 130
//        }
//    },
//    bar: {
//        width: {
//            ratio: 0.5 // this makes bar width 50% of length between ticks
//        }
//        // or
//        //width: 100 // this makes bar width 100px
//    }
//});
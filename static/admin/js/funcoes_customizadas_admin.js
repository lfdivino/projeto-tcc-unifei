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
    } else if ($("#tipo_grafico").val() == "grafico_barras") {
        gerar_grafico_barras_respostas();
        $("#titulo_analise").html("<h2>Grafico de barras relacinando as Perguntas x Respostas</h2>");
    } else if ($("#tipo_exibicao_dados").val() == "tabela") {
        montar_tabela_respostas();
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

function gerar_grafico_barras_respostas() {
    var respostas_1 = ['1'];
    var respostas_2 = ['2'];
    var respostas_3 = ['3'];
    var respostas_4 = ['4'];
    var respostas_5 = ['5'];
    var eixo_x = ['x'];
    $("#pergunta > option").each(function() {
        if (this.value != 0){
            eixo_x.push(this.text);
        }
    });
    for (var i = 1; i <= $("#pergunta option").size(); i++){
        respostas_1.push(0);
        respostas_2.push(0);
        respostas_3.push(0);
        respostas_4.push(0);
        respostas_5.push(0);
    }

    $.ajax({
        url: '/api/respostas/',
        type: 'GET',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success:function(result){
            $.each(result, function(i, resposta) {
                switch (resposta.resposta) {
                    case 1:
                        respostas_1[resposta.id_pergunta] = respostas_1[resposta.id_pergunta] + 1;
                    break;
                    case 2:
                        respostas_2[resposta.id_pergunta] = respostas_2[resposta.id_pergunta] + 1;
                    break;
                    case 3:
                        respostas_3[resposta.id_pergunta] = respostas_3[resposta.id_pergunta] + 1;
                    break;
                    case 4:
                        respostas_4[resposta.id_pergunta] = respostas_4[resposta.id_pergunta] +1;
                    break;
                    case 5:
                        respostas_5[resposta.id_pergunta] = respostas_5[resposta.id_pergunta] + 1;
                    default:
                        console.log("Desculpe, estamos sem nenhuma resposta.");
                    }
            });

            var chart = c3.generate({
                data: {
                    x : 'x',
                    columns: [
                        eixo_x,
                        respostas_1,
                        respostas_2,
                        respostas_3,
                        respostas_4,
                        respostas_5
                    ],
                    type: 'bar'
                },
                axis: {
                    x: {
                        type: 'category',
                        tick: {
                            rotate: 75,
                            multiline: false
                        },
                        height: 130
                    }
                },
                bar: {
                    width: {
                        ratio: 0.5 // this makes bar width 50% of length between ticks
                    }
                    // or
                    //width: 100 // this makes bar width 100px
                }
            });
        },
        error: function(result){
            alert("Aconteceu um problema ao buscar as respostas do sistema");
        }
    });
}

function montar_tabela_respostas() {
    var respostas_1 = ['1'];
    var respostas_2 = ['2'];
    var respostas_3 = ['3'];
    var respostas_4 = ['4'];
    var respostas_5 = ['5'];
    var eixo_x = ['x'];
    $("#pergunta > option").each(function() {
        if (this.value != 0){
            eixo_x.push(this.text);
        }
    });
    for (var i = 1; i <= $("#pergunta option").size(); i++){
        respostas_1.push(0);
        respostas_2.push(0);
        respostas_3.push(0);
        respostas_4.push(0);
        respostas_5.push(0);
    }

    $.ajax({
        url: '/api/respostas/',
        type: 'GET',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success:function(result){
            $.each(result, function(i, resposta) {
                switch (resposta.resposta) {
                    case 1:
                        respostas_1[resposta.id_pergunta] = respostas_1[resposta.id_pergunta] + 1;
                    break;
                    case 2:
                        respostas_2[resposta.id_pergunta] = respostas_2[resposta.id_pergunta] + 1;
                    break;
                    case 3:
                        respostas_3[resposta.id_pergunta] = respostas_3[resposta.id_pergunta] + 1;
                    break;
                    case 4:
                        respostas_4[resposta.id_pergunta] = respostas_4[resposta.id_pergunta] +1;
                    break;
                    case 5:
                        respostas_5[resposta.id_pergunta] = respostas_5[resposta.id_pergunta] + 1;
                    default:
                        console.log("Desculpe, estamos sem nenhuma resposta.");
                    }
            });

                var tabela = "<div class='tabela'>";
                tabela += "<div class='linha-tabela'>";
                    tabela += "<div class='col-md-pergunta'>Pergunta</div>";
                    tabela += "<div class='col-md-1'>Resposta 1</div>";
                    tabela += "<div class='col-md-1'>Porcentagem</div>";
                    tabela += "<div class='col-md-1'>Resposta 2</div>";
                    tabela += "<div class='col-md-1'>Porcentagem</div>";
                    tabela += "<div class='col-md-1'>Resposta 3</div>";
                    tabela += "<div class='col-md-1'>Porcentagem</div>";
                    tabela += "<div class='col-md-1'>Resposta 4</div>";
                    tabela += "<div class='col-md-1'>Porcentagem</div>";
                    tabela += "<div class='col-md-1'>Resposta 5</div>";
                    tabela += "<div class='col-md-1'>Porcentagem</div>";
                    tabela += "<div class='col-md-1'>Total</div>";
                tabela += "</div>";

                for (var i = 1; i < eixo_x.length; i++){
                    var total = respostas_1[i] + respostas_2[i] + respostas_3[i] + respostas_4[i] + respostas_5[i];
                    tabela += "<div class='linha-tabela'>";
                    tabela += "<div class='col-md-pergunta'>" + eixo_x[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + respostas_1[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + ((respostas_1[i]/total)*100).toFixed(2) + "%</div>";
                    tabela += "<div class='col-md-1'>" + respostas_2[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + ((respostas_2[i]/total)*100).toFixed(2) + "%</div>";
                    tabela += "<div class='col-md-1'>" + respostas_3[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + ((respostas_3[i]/total)*100).toFixed(2) + "%</div>";
                    tabela += "<div class='col-md-1'>" + respostas_4[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + ((respostas_4[i]/total)*100).toFixed(2) + "%</div>";
                    tabela += "<div class='col-md-1'>" + respostas_5[i] + "</div>";
                    tabela += "<div class='col-md-1'>" + ((respostas_5[i]/total)*100).toFixed(2) + "%</div>";
                    tabela += "<div class='col-md-1'>" + total + "</div>";
                    tabela += "</div>";
                }

                tabela += "</div>";

                $(".dados-processados").html(tabela);
        },
        error: function(result){
            alert("Aconteceu um problema ao buscar as respostas do sistema");
        }
    });
}
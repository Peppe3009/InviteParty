function addPr(indice) {
    nomeEvento = $('#nomeEvento'+indice).text();
    nomeEvento = nomeEvento.split("|");
    nomeEvento = nomeEvento[1].trimStart();
    giornoEvento = $('#giornoEvento'+indice).text();
    giornoEvento = giornoEvento.split("|");
    giornoEvento = giornoEvento[1].trimStart();
    $.ajax({
        url : '/updatePr',
        type : 'GET',
        data : {nomeEvento : nomeEvento, giornoEvento : giornoEvento},
        success: function (response) {
            if (response['status'] == 200){
                Materialize.toast("Complimenti sei diventato PR per " + nomeEvento, 2500, 'green');
                $('#item'+indice).hide();
            }else{
                Materialize.toast("Ops! Qualcosa è andato storto" , 2500, 'red');
            }
        }
    })
}
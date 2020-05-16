function prenota(indice) {
        nomeEvento = $('#nomeEvento'+indice).text();
        nomeEvento = nomeEvento.trimStart();
        nomeLocale = $('#nomeLocale'+indice).text();
        nomeLocale = nomeLocale.split("|");
        nomeLocale = nomeLocale[1].trimStart();
        giornoEvento = $('#giornoEvento'+indice).text();
        giornoEvento = giornoEvento.split("|");
        giornoEvento = giornoEvento[1].trimStart();
        oraEvento = $('#oraEvento'+indice).text();
        oraEvento = oraEvento.split("|");
        oraEvento = oraEvento[1].trimStart();
        $.ajax({
            url:"/add_prenotation",
            type: 'GET',
            data: {nomeEvento : nomeEvento, nomeLocale : nomeLocale, giornoEvento: giornoEvento, oraEvento : oraEvento},
            success: function (response) {
                if(response.status === 200){
                    Materialize.toast("Prenotazione Effettuata. E' stato generato un Qr Code della prenotazione", 2500, 'green');
                    $('#card'+indice).hide();
                }else{
                    Materialize.toast("Errore", 2000, 'red');
                }
            }
        });
    }
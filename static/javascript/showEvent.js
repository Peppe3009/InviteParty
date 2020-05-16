
function showEvent() {
    $('#collezione').empty();
    var locale = $('#nomeLocale').val();

    $.ajax({
        url: "/getEvent",
        type: 'GET',
        data : {nomeLocale : locale},
        success : function (response) {
            console.log(response);
            if (response.length > 0){
                $('#collezione').show();
                for(var i = 0; i < response.length; i++){
                    var element = document.createElement('li');
                    element.setAttribute("class", "collection-item");
                    var content = `
                         <p class="flow-text" style="font-size: medium"><b>Nome Evento</b> |  ${response[i].nomeEvento}</p><br>
                         <p class="flow-text" style="font-size: medium"><b>Giorno Evento</b> |  ${response[i].giornoEvento}</p><br>
                         <p class="flow-text" style="font-size: medium"><b>Ora Inizio Evento</b> |  ${response[i].oraEvento}</p><br>
                         <p class="flow-text" style="font-size: medium"><b>Numero Invitati</b> |  ${response[i].numeroInvitati}</p><br>
                         <p class="flow-text" style="font-size: medium"><b>Tipo Evento</b> |  ${response[i].tipoEvento}</p><br>
                        `;
                    element.innerHTML = content;
                    $('#collezione').append(element);
                }
            }else{
                $('#collezione').hide();
            }

        }
    })
}
function getData(){
    var nomeLocale = $('#nomeLocale').val();
    $.ajax({
        url: '/getData',
        type: 'GET',
        data:{nomeLocale: nomeLocale},
        success : function (response) {
            var eventi = [];
            var prenotazioni = [];
            for(var i = 0; i < response[0].length; i++){
                eventi.push(response[0][i].nomeEvento);
                prenotazioni.push(response[1][i]);
            }
            var contesto = $('#myChart');
            new Chart(contesto, {
                type: 'line',
                data: {
                    labels: eventi,
                    datasets: [{
                        label: 'Numero di prenotazioni',
                        data: prenotazioni,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 1
                            }
                        }]
                    }
                }
            })
        }
    });
}
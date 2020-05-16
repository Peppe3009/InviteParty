function scarica() {
    var doc = new jsPDF();
    doc.text("Lista prenotazioni " + $('#nomeEvento').val(), 10, 10);
    doc.autoTable({html : '#nomi', styles: { halign: 'center' }});
    doc.save('ListaInvitati' + $('#nomeEvento').val()+'.pdf');
}
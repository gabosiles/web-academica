(function () {
  var items = Array.from(document.querySelectorAll('.revista-card'));
  var modal = $('#revistaModal');
  var frame = document.getElementById('revistaFrame');
  var current = 0;

  function openAt(index){
    if(index < 0 || index >= items.length) return;
    current = index;
    var url = items[current].dataset.embed;
    frame.src = url;              // carga el flip-book
    modal.modal('show');
  }

  function closeModal(){
    frame.src = '';               // limpia para detener carga/audio
  }

  // Clic en tarjeta completa abre preview
  items.forEach(function(card, i){
    card.addEventListener('click', function(e){
      // si el click fue en un botón "Leer ahora", no abrir modal
      if(e.target.closest('a.btn-danger')) return;
      openAt(i);
    });
  });

  // Botones “Vista previa”
  document.querySelectorAll('.btn-preview').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var idx = items.findIndex(x => x.dataset.embed === btn.dataset.embed);
      openAt(idx >= 0 ? idx : 0);
    });
  });

  // Navegación dentro del modal
  document.getElementById('prevRev').addEventListener('click', function(){
    openAt((current - 1 + items.length) % items.length);
  });
  document.getElementById('nextRev').addEventListener('click', function(){
    openAt((current + 1) % items.length);
  });

  // Cerrar limpia iframe
  modal.on('hidden.bs.modal', closeModal);

  // Atajos de teclado mientras el modal está visible
  document.addEventListener('keydown', function(ev){
    if(!modal.hasClass('show')) return;
    if(ev.key === 'ArrowLeft') document.getElementById('prevRev').click();
    if(ev.key === 'ArrowRight') document.getElementById('nextRev').click();
  });
})();
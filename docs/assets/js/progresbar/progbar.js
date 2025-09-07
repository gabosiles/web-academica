  const main = document.querySelector(".container.pt-4.pb-4");
  const persona = document.getElementById("persona-easter");
  let startY = 0;
  let isPulling = false;

  window.addEventListener("touchstart", function(e) {
    if (window.scrollY === 0) {
      startY = e.touches[0].clientY;
      isPulling = true;
    }
  });

  window.addEventListener("touchmove", function(e) {
    if (!isPulling) return;

    let currentY = e.touches[0].clientY;
    let diff = currentY - startY;

    if (diff > 0) {
      // Desplaza el MAIN hacia abajo
      main.style.transform = `translateY(${diff}px)`;

      // Mueve la persona al mismo tiempo, como pegada al borde superior
      let offset = Math.min(diff, 150);
      persona.style.top = `${-150 + offset}px`;
    }
  });

  window.addEventListener("touchend", function() {
    if (isPulling) {
      // Regresa todo a su estado normal
      main.style.transition = "transform 0.3s ease";
      persona.style.transition = "top 0.3s ease";

      main.style.transform = "translateY(0)";
      persona.style.top = "-150px";

      setTimeout(() => {
        main.style.transition = "";
        persona.style.transition = "";
      }, 300);
    }
    isPulling = false;
  });
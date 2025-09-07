const slider = document.getElementById("gs-slider");
  const leftBtn = document.querySelector(".gs-left");
  const rightBtn = document.querySelector(".gs-right");

  // detectar ancho real de una tarjeta
  const card = document.querySelector(".gs-card");
  const cardStyle = window.getComputedStyle(card);
  const cardWidth = card.offsetWidth + parseInt(cardStyle.marginRight);

  leftBtn.addEventListener("click", () => {
    slider.scrollBy({ left: -cardWidth, behavior: "smooth" });
  });

  rightBtn.addEventListener("click", () => {
    slider.scrollBy({ left: cardWidth, behavior: "smooth" });
  });
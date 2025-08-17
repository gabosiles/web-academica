let imagenes = [];
let indiceActual = 0;

// 🔹 Tomamos todas las imágenes de la galería
const thumbs = document.querySelectorAll(".galeria img");
thumbs.forEach((img, index) => {
  // Guardamos en el arreglo
  imagenes.push({
    src: img.src,
    texto: img.dataset.texto // usamos el alt como descripción
  });

  // Asignamos click automáticamente
  img.addEventListener("click", () => abrirLightbox(index));
});

function abrirLightbox(indice) {
  indiceActual = indice;
  const lightbox = document.getElementById("lightbox");
  const contenido = document.querySelector(".lightbox-content");

  lightbox.style.display = "flex";
  contenido.style.background = "#222"; // cambiar color dinámicamente
  contenido.style.color = "white";      // cambiar color del texto
  mostrarImagen();
}


function mostrarImagen() {
  document.getElementById("lightbox-img").src = imagenes[indiceActual].src;
  document.getElementById("lightbox-texto").innerHTML = imagenes[indiceActual].texto;
}

function cambiarImagen(direccion) {
  indiceActual += direccion;
  if (indiceActual < 0) indiceActual = imagenes.length - 1;
  if (indiceActual >= imagenes.length) indiceActual = 0;
  mostrarImagen();
}

function cerrarLightbox() {
  document.getElementById("lightbox").style.display = "none";
}

function cerrarSiFondo(event) {
  if (event.target.id === "lightbox") {
    cerrarLightbox();
  }
}


// 🔹 Navegación con teclas ← → y cierre con Esc
document.addEventListener("keydown", function(e) {
  if (document.getElementById("lightbox").style.display === "flex") {
    if (e.key === "ArrowRight") cambiarImagen(1);
    if (e.key === "ArrowLeft") cambiarImagen(-1);
    if (e.key === "Escape") cerrarLightbox();
  }
});

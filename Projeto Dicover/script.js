function togglemode() {
  const body = document.querySelector("body");

  //   if (body.classList.contains("light")) {
  //     body.classList.remove("light");
  //   } else {
  //     body.classList.add("light");
  //   }

  body.classList.toggle("light");

  // pegar a tag img e depois substituir a imagem quando em light mode ou escuro.

  const img = document.querySelector("#profile img");
  console.log("img", img);
  if (body.classList.contains("light")) {
    // se tiver light mode
    img.setAttribute("src", "./assets/avatar-light.png");
  } else {
    // sem light mode
    img.setAttribute("src", "./assets/avatar.png");
  }
}

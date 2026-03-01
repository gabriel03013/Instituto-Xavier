const comportamentoModal = () => {
  const modal = document.getElementById("editar-notas-modal");

  if (modal.style.display === "") {
    modal.style.display = "flex";
    console.log("abriu");
  } else {
    modal.style.display = "";
  }
};

[
  document.querySelectorAll("tr"),
  document.querySelectorAll(".btn-edit"),
].forEach((e) => {
  e.forEach((t) => {
    t.addEventListener("click", comportamentoModal);
  });
});

document
  .getElementById("fechar-modal")
  .addEventListener("click", comportamentoModal);


// ! TODO -> Média preview conforme digitação
const span = document.getElementById("media-final-preview") 

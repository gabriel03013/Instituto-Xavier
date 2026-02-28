const modalEditar = document.querySelector(".observacoes-modal:not(.modal-adicionar)");
const modalAdicionar = document.querySelector(".modal-adicionar");

const abrirModal = (modal) => {
  modal.style.display = "flex";
};

const fecharModal = (modal) => {
  modal.style.display = "none";
};

document.querySelectorAll("tbody tr").forEach((linha) => {
  linha.addEventListener("click", (e) => {
    if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
      abrirModal(modalEditar);
    }
  });
});

document
  .getElementById("adicionar-observação")
  .addEventListener("click", () => {
    abrirModal(modalAdicionar);
  });

document.querySelectorAll(".fechar-modal").forEach((botao) => {
  botao.addEventListener("click", () => {
    const modal = botao.closest(".observacoes-modal");
    fecharModal(modal);
  });
});

document.querySelectorAll("#cancelar-alteracoes").forEach((botao) => {
  botao.addEventListener("click", (e) => {
    e.preventDefault();
    const modal = botao.closest(".observacoes-modal");
    fecharModal(modal);
  });
});
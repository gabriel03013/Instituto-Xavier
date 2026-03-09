const modalEditar = document.querySelector(
  ".admin-modal:not(.modal-adicionar)",
);
const modalAdicionar = document.querySelector(".modal-adicionar");

const abrirModal = (modal) => {
  if (modal) modal.style.display = "flex";
};

const fecharModal = (modal) => {
  if (modal) modal.style.display = "none";
};

document.querySelectorAll("tbody tr").forEach((linha) => {
  linha.addEventListener("click", (e) => {
    if (e.target.closest(".btn-excluir")) return;
    if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
      abrirModal(modalEditar);
    }
  });
});

const btnAdicionar = document.getElementById("admin-adicionar");
if (btnAdicionar) {
  btnAdicionar.addEventListener("click", () => {
    abrirModal(modalAdicionar);
  });
}

document.querySelectorAll(".fechar-modal").forEach((botao) => {
  botao.addEventListener("click", () => {
    const modal = botao.closest(".admin-modal");
    fecharModal(modal);
  });
});

document.querySelectorAll(".cancelar-alteracoes").forEach((botao) => {
  botao.addEventListener("click", (e) => {
    e.preventDefault();
    const modal = botao.closest(".admin-modal");
    fecharModal(modal);
  });
});

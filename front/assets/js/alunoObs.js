import { api } from "./utils.js";

let todasAsObservacoes = [];

document.addEventListener("DOMContentLoaded", async () => {
  const id = localStorage.getItem("userId");
  const modal = document.querySelector(".observacoes-modal");

  await carregarObservacoes(id);

  const searchInput = document.querySelector(".aluno-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsObservacoes.filter((obs) => {
        return (
          obs.professor.toLowerCase().includes(termo) ||
          obs.materia.toLowerCase().includes(termo) ||
          obs.observacao.toLowerCase().includes(termo)
        );
      });
      renderizarTabela(filtradas);
    });
  }

  document.querySelectorAll(".fechar-modal").forEach((button) => {
    button.addEventListener("click", () => {
      modal.style.display = "none";
    });
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

async function carregarObservacoes(id) {
  todasAsObservacoes = await api(`observacao/aluno/${id}`);
  renderizarTabela(todasAsObservacoes);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector("tbody");
  tbody.innerHTML = "";

  lista.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.professor}</td>
      <td>${item.materia}</td>
      <td>${item.observacao.substring(0, 10)}${item.observacao.length > 10 ? "..." : ""}</td>
    `;
    tr.addEventListener("click", () => abrirModal(item));
    tbody.appendChild(tr);
  });
}

function abrirModal(item) {
  const modal = document.querySelector(".observacoes-modal");
  document.getElementById("modal-professor").textContent = item.professor;
  document.getElementById("modal-materia").textContent = item.materia;
  document.getElementById("modal-texto").textContent = item.observacao;
  modal.style.display = "flex";
}

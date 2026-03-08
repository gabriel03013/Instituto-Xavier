import { api } from "./utils.js";

let todasAsTurmas = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTurmas();

  const searchInput = document.querySelector(".admin-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsTurmas.filter((t) => {
        const nomeTurma = `${t.serie}º ANO ${t.turma}`.toLowerCase();
        return nomeTurma.includes(termo);
      });
      renderizarTurmas(filtradas);
    });
  }
});

async function carregarTurmas() {
  todasAsTurmas = await api("turma/", "GET");
  renderizarTurmas(todasAsTurmas);
}

function renderizarTurmas(lista) {
  const container = document.getElementById("admin-turmas");
  if (!container) return;
  container.innerHTML = "";

  lista.forEach((t) => {
    const div = document.createElement("div");
    div.className = "admin-turma-div";
    div.onclick = () => {
      window.location.href = `alunos.html?turma=${t.id}`;
    };
    div.innerHTML = `
      <h2>${t.serie}º ANO ${t.turma}</h2>
      <p>${t.alunos ? t.alunos.length : 0} alunos</p>
    `;
    container.appendChild(div);
  });
}

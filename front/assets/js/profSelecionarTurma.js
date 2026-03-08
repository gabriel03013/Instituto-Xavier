import { api } from "./utils.js";

const urlParams = new URLSearchParams(window.location.search);
const tipo = urlParams.get("tipo");
let destinoFinal = "";

if (tipo === "obs") {
  destinoFinal = "observacoes.html";
  const obsEl = document.getElementById("obs");
  if (obsEl) obsEl.classList.add("aba-professor-ativa");
} else if (tipo === "notas") {
  destinoFinal = "notas.html";
  const notasEl = document.getElementById("notas");
  if (notasEl) notasEl.classList.add("aba-professor-ativa");
}

let todasAsTurmas = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTurmas();

  const searchInput = document.querySelector(".search-bar input");
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
  todasAsTurmas = await api("turma", "GET");
  renderizarTurmas(todasAsTurmas);
}

function renderizarTurmas(lista) {
  const container = document.getElementById("turmas");
  if (!container) return;
  container.innerHTML = "";

  lista.forEach((turma) => {
    const div = document.createElement("div");
    div.classList.add("turma-div");
    div.dataset.turma = turma.id;
    div.innerHTML = `
      <h2>${turma.serie}º ANO ${turma.turma}</h2>
      <p>${turma.alunos ? turma.alunos.length : 0} alunos</p>
    `;

    div.addEventListener("click", () => {
      window.location.href = `./${destinoFinal}?turma=${turma.id}`;
    });

    container.appendChild(div);
  });
}

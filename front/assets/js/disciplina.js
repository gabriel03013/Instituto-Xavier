import { api } from "./utils.js";

let todasAsMaterias = [];

document.addEventListener("DOMContentLoaded", async () => {
  const userId = localStorage.getItem("userId");
  const aluno = await api(`mutant/info?id_mutante=${userId}`);

  document.getElementById("nome-aluno").textContent = aluno.nome;
  document.getElementById("turma-aluno").textContent = aluno.turma;

  await carregarMaterias(userId);

  const searchInput = document.querySelector(".aluno-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsMaterias.filter((m) => {
        return (
          m.materia.toLowerCase().includes(termo) ||
          m.professor.toLowerCase().includes(termo)
        );
      });
      renderizarCards(filtradas);
    });
  }
});

async function carregarMaterias(userId) {
  todasAsMaterias = await api(`mutant/my_subjects?id_mutante=${userId}`);
  renderizarCards(todasAsMaterias);
}

function renderizarCards(lista) {
  const container = document.querySelector(".container");
  container.innerHTML = "";

  lista.forEach((materia, index) => {
    const card = document.createElement("div");
    card.classList.add("card");
    const accentClass = index % 2 === 0 ? "dark" : "light";
    card.innerHTML = `
      <div class="card-accent ${accentClass}"></div>
      <img src="../assets/images/image 9.svg" class="avatar">
      <div class="card-text">
          <h2>${materia.materia}</h2>
          <span>${materia.professor}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

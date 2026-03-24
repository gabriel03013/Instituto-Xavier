import { api } from "./utils.js";

const materiaId = localStorage.getItem("materia_id");
let todosOsQuizzes = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarQuizzes();
  configurarBusca();
});

async function carregarQuizzes() {
  try {
    const response = await fetch("../../assets/data/quizzes.json");
    const quizzes = await response.json();

    todosOsQuizzes = quizzes.filter(
      (q) => !materiaId || q.materia_id == materiaId,
    );

    renderizarQuizzes(todosOsQuizzes);
  } catch (erro) {
    console.error("Erro ao carregar quizzes:", erro);
  }
}

function renderizarQuizzes(quizzes) {
  const lista = document.getElementById("quiz-list");
  lista.innerHTML = "";

  if (quizzes.length === 0) {
    lista.innerHTML =
      '<tr><td colspan="2" style="text-align: center; padding: 3rem; color: #888;">Nenhum quiz encontrado.</td></tr>';
    return;
  }

  quizzes.forEach((quiz) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${quiz.titulo}</td>
      <td class="td-action">
        <button class="btn-lancar" data-id="${quiz.id}">
          <i class="fa-solid fa-paper-plane"></i>   Lançar
        </button>
      </td>
    `;

    tr.querySelector(".btn-lancar").addEventListener("click", () =>
      lancarQuiz(quiz.id),
    );
    lista.appendChild(tr);
  });
}

function configurarBusca() {
  const inputBusca = document.getElementById("search-quiz");
  if (!inputBusca) return;

  inputBusca.addEventListener("input", (e) => {
    const termo = e.target.value.toLowerCase();
    const filtrados = todosOsQuizzes.filter((q) =>
      q.titulo.toLowerCase().includes(termo),
    );
    renderizarQuizzes(filtrados);
  });
}

async function lancarQuiz(quizId) {
  if (!materiaId) {
    console.error("Matéria do professor não identificada.");
    return;
  }

  try {
    const btn = document.querySelector(`button[data-id="${quizId}"]`);
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Lançando...';

    await api(
      `mutante_materia/materia/${materiaId}/lancar_quiz/${quizId}`,
      "POST",
    );

    btn.innerHTML = '<i class="fa-solid fa-check"></i> Lançado';
    btn.style.background = "#94a3b8";
    btn.style.cursor = "default";
    btn.style.boxShadow = "2px 2px 0px #000";
  } catch (erro) {
    console.error("Erro ao lançar quiz:", erro);
    const btn = document.querySelector(`button[data-id="${quizId}"]`);
    btn.disabled = false;
    btn.innerHTML =
      '<i class="fa-solid fa-paper-plane"></i> Lançar para todos os alunos';
  }
}

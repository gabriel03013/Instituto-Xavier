import { api } from "./utils.js";

const params = new URLSearchParams(window.location.search);
const materiaId = Number(params.get("materia_id"));
const materiaNome = params.get("materia") || "Disciplina";
const userId = localStorage.getItem("userId");

document.getElementById("breadcrumb-materia").textContent = materiaNome;
document.getElementById("titulo-materia").textContent =
  `Avaliações — ${materiaNome}`;

const grid = document.getElementById("quiz-grid");
const vazio = document.getElementById("quiz-vazio");
const statPendentes = document.getElementById("stat-pendentes");
const statConcluidas = document.getElementById("stat-concluidas");
const statMedia = document.getElementById("stat-media");

let todosOsQuizzes = [];

async function carregarQuizzes() {
  try {
    const resQuizzes = await fetch("../../assets/data/quizzes.json");
    const metadadosQuizzes = await resQuizzes.json();

    const registros = await api(`mutante_materia/mutante/${userId}`, "GET");
    const registroMateria = registros.find((r) => r.materia_id === materiaId);

    if (!registroMateria || !registroMateria.quiz) {
      todosOsQuizzes = [];
    } else {
      let lancados = registroMateria.quiz;
      if (typeof lancados === "string") {
        try {
          lancados = JSON.parse(lancados);
        } catch (e) {
          console.error("Erro ao analisar JSON do quiz:", e);
          lancados = [];
        }
      }

      todosOsQuizzes = lancados
        .map((lancado) => {
          const meta = metadadosQuizzes.find((q) => q.id === lancado.id);
          if (!meta) return null;
          return {
            ...meta,
            status: lancado.status,
            nota: lancado.nota,
          };
        })
        .filter((q) => q !== null);
    }

    atualizarStats();
    renderizarGrid("todos");
    configurarFiltros();
  } catch (erro) {
    console.error("Erro ao carregar avaliações:", erro);
    vazio.style.display = "flex";
    grid.style.display = "none";
  }
}

function atualizarStats() {
  const pendentes = todosOsQuizzes.filter((q) => q.status === "pendente");
  const concluidos = todosOsQuizzes.filter(
    (q) => q.status === "concluido" || q.status === "concluida",
  );
  const notas = concluidos.map((q) => q.nota).filter((n) => n !== null);
  const media = notas.length
    ? (notas.reduce((a, b) => a + b, 0) / notas.length).toFixed(1)
    : null;

  statPendentes.textContent = pendentes.length;
  statConcluidas.textContent = concluidos.length;
  statMedia.textContent = media !== null ? media : "—";
}

function renderizarGrid(filtro) {
  const lista =
    filtro === "todos"
      ? todosOsQuizzes
      : todosOsQuizzes.filter((q) => {
          if (filtro === "concluido")
            return q.status === "concluido" || q.status === "concluida";
          return q.status === filtro;
        });

  grid.innerHTML = "";

  if (lista.length === 0) {
    vazio.style.display = "flex";
    grid.style.display = "none";
    return;
  }

  vazio.style.display = "none";
  grid.style.display = "grid";

  lista.forEach((quiz) => {
    const total = quiz.perguntas
      ? quiz.perguntas.length
      : (quiz.total_questoes ?? "—");
    const isPendente = quiz.status === "pendente";
    const statusClass = isPendente ? "pendente" : "concluido";

    const card = document.createElement("div");
    card.className = "quiz-card";
    card.innerHTML = `
      <div class="quiz-card-status-bar ${statusClass}"></div>
      <div class="quiz-card-top">
        <h3 class="quiz-card-titulo">${quiz.titulo}</h3>
        <span class="quiz-card-badge ${statusClass}">${isPendente ? "Pendente" : "Concluído"}</span>
      </div>
      <div class="quiz-card-info">
        <span><i class="fa-solid fa-circle-question"></i> ${total} questões</span>
      </div>
      ${
        !isPendente
          ? `<div class="quiz-card-nota ${quiz.nota >= 6 ? "nota-aprovado" : "nota-reprovado"}">
              <i class="fa-solid fa-star"></i>
              <span>Nota: </span><strong>${quiz.nota?.toFixed(1) ?? "—"}</strong>
            </div>`
          : ""
      }
      <button class="quiz-card-btn ${statusClass}" ${isPendente ? "" : "disabled"}>
        ${isPendente ? '<i class="fa-solid fa-play"></i> Iniciar Quiz' : '<i class="fa-solid fa-lock"></i> Já respondido'}
      </button>
    `;

    if (isPendente) {
      card.querySelector("button").addEventListener("click", () => {
        const url = new URLSearchParams({
          quiz_id: quiz.id,
          materia_id: materiaId,
          materia: materiaNome,
        });
        window.location.href = `quiz.html?${url.toString()}`;
      });
    }

    grid.appendChild(card);
  });
}

function configurarFiltros() {
  const btns = document.querySelectorAll(".filtro-btn");

  const contadores = {
    todos: todosOsQuizzes.length,
    pendente: todosOsQuizzes.filter((q) => q.status === "pendente").length,
    concluido: todosOsQuizzes.filter(
      (q) => q.status === "concluido" || q.status === "concluida",
    ).length,
  };

  btns.forEach((btn) => {
    const filtro = btn.dataset.filtro;
    btn.querySelector(".filtro-contador").textContent = contadores[filtro] ?? 0;

    btn.addEventListener("click", () => {
      btns.forEach((b) => b.classList.remove("ativo"));
      btn.classList.add("ativo");
      renderizarGrid(filtro);
    });
  });
}

carregarQuizzes();

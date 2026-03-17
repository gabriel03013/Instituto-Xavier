import { api } from "./utils.js";

const params = new URLSearchParams(window.location.search);
const quizId = Number(params.get("quiz_id"));
const materiaId = Number(params.get("materia_id"));
const materiaNome = params.get("materia") || "Disciplina";
const userId = localStorage.getItem("userId");

const runner = document.getElementById("quiz-runner");
const resultado = document.getElementById("quiz-resultado");

const elTitulo = document.getElementById("quiz-runner-titulo");
const elMateria = document.getElementById("quiz-runner-materia");
const elNumero = document.getElementById("quiz-questao-numero");
const elEnunciado = document.getElementById("quiz-enunciado");
const elAlternativas = document.getElementById("quiz-alternativas");
const elProgressoTexto = document.getElementById("quiz-progresso-texto");
const elProgressoFill = document.getElementById("quiz-progress-fill");
const elDots = document.getElementById("quiz-dots");
const btnAnterior = document.getElementById("btn-anterior");
const btnProximo = document.getElementById("btn-proximo");
const btnVoltar = document.getElementById("btn-voltar");

let quiz = null;
let questaoAtual = 0;
let respostas = [];

async function carregarQuiz() {
  const res = await fetch("../../assets/data/quizzes.json");
  const todos = await res.json();

  quiz = todos.find((q) => q.id === quizId);

  if (!quiz) {
    alert("Avaliação não encontrada.");
    window.location.href = `avaliacoes.html?materia_id=${materiaId}&materia=${materiaNome}`;
    return;
  }

  respostas = new Array(quiz.perguntas.length).fill(null);

  elTitulo.textContent = quiz.titulo;
  elMateria.textContent = materiaNome;

  renderizarDots();
  renderizarQuestao();
}

function renderizarQuestao() {
  const q = quiz.perguntas[questaoAtual];
  const total = quiz.perguntas.length;
  const letras = ["A", "B", "C", "D", "E"];

  elNumero.textContent = `Questão ${questaoAtual + 1}`;
  elEnunciado.textContent = q.enunciado;
  elProgressoTexto.textContent = `Questão ${questaoAtual + 1} de ${total}`;
  elProgressoFill.style.width = `${((questaoAtual + 1) / total) * 100}%`;

  elAlternativas.innerHTML = "";
  q.alternativas.forEach((alt, i) => {
    const div = document.createElement("div");
    div.className = `quiz-alternativa${respostas[questaoAtual] === i ? " selecionada" : ""}`;
    div.innerHTML = `
      <span class="quiz-alternativa-letra">${letras[i]}</span>
      <span>${alt}</span>
    `;
    div.addEventListener("click", () => selecionarAlternativa(i));
    elAlternativas.appendChild(div);
  });

  btnAnterior.disabled = questaoAtual === 0;

  const isUltima = questaoAtual === total - 1;
  btnProximo.innerHTML = isUltima
    ? 'Finalizar <i class="fa-solid fa-check"></i>'
    : 'Próxima <i class="fa-solid fa-chevron-right"></i>';
  btnProximo.className = `btn-quiz-nav btn-quiz-proximo${isUltima ? " btn-quiz-finalizar" : ""}`;

  atualizarDots();
}

function selecionarAlternativa(indice) {
  respostas[questaoAtual] = indice;
  renderizarQuestao();
}

function renderizarDots() {
  elDots.innerHTML = "";
  quiz.perguntas.forEach((_, i) => {
    const dot = document.createElement("div");
    dot.className = "quiz-dot";
    dot.title = `Questão ${i + 1}`;
    dot.addEventListener("click", () => {
      questaoAtual = i;
      renderizarQuestao();
    });
    elDots.appendChild(dot);
  });
}

function atualizarDots() {
  const dots = elDots.querySelectorAll(".quiz-dot");
  dots.forEach((dot, i) => {
    dot.classList.remove("respondida", "atual");
    if (i === questaoAtual) dot.classList.add("atual");
    else if (respostas[i] !== null) dot.classList.add("respondida");
  });
}

function calcularResultado() {
  let acertos = 0;
  quiz.perguntas.forEach((q, i) => {
    if (respostas[i] === q.correta) acertos++;
  });
  return acertos;
}

async function mostrarResultado() {
  const total = quiz.perguntas.length;
  const acertos = calcularResultado();
  const erros = total - acertos;
  const porcentagem = Math.round((acertos / total) * 100);
  const notaCalculada = (acertos / total) * 10;
  const aprovado = porcentagem >= 60;

  runner.style.display = "none";
  resultado.style.display = "flex";

  const icone = document.getElementById("resultado-icone");
  icone.className = `resultado-icone ${aprovado ? "aprovado" : "reprovado"}`;
  icone.innerHTML = `<i class="fa-solid ${aprovado ? "fa-trophy" : "fa-face-sad-tear"}"></i>`;

  document.getElementById("resultado-titulo").textContent = aprovado
    ? "Parabéns!"
    : "Não foi dessa vez...";
  document.getElementById("resultado-subtitulo").textContent = aprovado
    ? "Você foi muito bem na avaliação!"
    : "Continue estudando e tente novamente.";

  document.getElementById("resultado-porcentagem").textContent =
    `${porcentagem}%`;
  document.getElementById("resultado-acertos").textContent = acertos;
  document.getElementById("resultado-erros").textContent = erros;
  document.getElementById("resultado-total").textContent = total;
  document.getElementById("resultado-nota").textContent =
    notaCalculada.toFixed(1);

  // Salvar resultado no backend
  try {
    const registros = await api(`mutante_materia/mutante/${userId}`, "GET");
    const registro = registros.find((r) => r.materia_id === materiaId);

    if (registro) {
      let quizzes = registro.quiz;
      if (typeof quizzes === "string") {
        try {
          quizzes = JSON.parse(quizzes || "[]");
        } catch (e) {
          quizzes = [];
        }
      } else if (!quizzes) {
        quizzes = [];
      }

      const index = quizzes.findIndex((q) => q.id === quizId);

      if (index !== -1) {
        quizzes[index].status = "concluida";
        quizzes[index].nota = notaCalculada;

        // Como o backend agora trata a coluna como JSON, enviamos o objeto direto
        await api(`mutante_materia/${userId}/${materiaId}`, "PATCH", {
          quiz: quizzes,
        });
      }
    }
  } catch (erro) {
    console.error("Erro ao salvar resultado:", erro);
  }
}

btnAnterior.addEventListener("click", () => {
  if (questaoAtual > 0) {
    questaoAtual--;
    renderizarQuestao();
  }
});

btnProximo.addEventListener("click", () => {
  const isUltima = questaoAtual === quiz.perguntas.length - 1;
  if (isUltima) {
    if (respostas.includes(null)) {
      if (
        !confirm(
          "Você ainda tem questões sem resposta. Deseja finalizar mesmo assim?",
        )
      ) {
        return;
      }
    }
    mostrarResultado();
  } else {
    questaoAtual++;
    renderizarQuestao();
  }
});

btnVoltar.addEventListener("click", () => {
  const url = new URLSearchParams({
    materia_id: materiaId,
    materia: materiaNome,
  });
  window.location.href = `avaliacoes.html?${url.toString()}`;
});

document
  .getElementById("btn-resultado-voltar")
  .addEventListener("click", () => {
    const url = new URLSearchParams({
      materia_id: materiaId,
      materia: materiaNome,
    });
    window.location.href = `avaliacoes.html?${url.toString()}`;
  });

carregarQuiz();

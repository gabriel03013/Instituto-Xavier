import { api, getIdTurma } from "./utils.js";

let todasAsObservacoes = [];
let todosOsAlunos = [];
let obsIdExcluindo = null;

const modalEditar = document.querySelector(
  ".observacoes-modal:not(.modal-adicionar):not(.modal-excluir)",
);
const modalAdicionar = document.querySelector(".modal-adicionar");
const modalExcluir = document.getElementById("modal-excluir-observacao");

document.addEventListener("DOMContentLoaded", async () => {
  const idTurma = getIdTurma();
  let materiaId = Number(localStorage.getItem("materia_id"));

  const turmaInfos = await api(`turma/${idTurma}`, "GET");
  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;

  await carregarObservacoes();
  await carregarAlunosParaSelect(idTurma, materiaId);

  const searchInput = document.querySelector(".turma-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsObservacoes.filter((obs) => {
        return (
          obs.aluno.nome.toLowerCase().includes(termo) ||
          obs.aluno.matricula.toLowerCase().includes(termo) ||
          obs.observacao.toLowerCase().includes(termo)
        );
      });
      renderizarTabela(filtradas);
    });
  }

  const formEditar = modalEditar.querySelector("form");
  formEditar.addEventListener("submit", async (e) => {
    e.preventDefault();
    const idObs = formEditar.dataset.idObs;
    const novaObs = document.getElementById("editar-observacao-aluno").value;
    await api(`observacao/${idObs}`, "PATCH", { observacao: novaObs });
    fecharModal(modalEditar);
    await carregarObservacoes();
  });

  const formAdicionar = modalAdicionar.querySelector("form");
  formAdicionar.addEventListener("submit", async (e) => {
    e.preventDefault();
    const mmId = document.getElementById("selectAluno").value;
    const textoObs = document.getElementById(
      "adicionar-observacao-aluno",
    ).value;
    await api(`observacao/`, "POST", {
      mutantesmaterias_id: Number(mmId),
      observacao: textoObs,
      data: new Date().toISOString().split("T")[0],
    });
    fecharModal(modalAdicionar);
    formAdicionar.reset();
    await carregarObservacoes();
  });

  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", async () => {
      if (obsIdExcluindo) {
        await api(`observacao/${obsIdExcluindo}`, "DELETE");
        fecharModal(modalExcluir);
        await carregarObservacoes();
      }
    });

  document
    .getElementById("adicionar-observação")
    .addEventListener("click", () => {
      abrirModal(modalAdicionar);
    });

  document.querySelectorAll(".fechar-modal").forEach((botao) => {
    botao.addEventListener("click", () => {
      fecharModal(botao.closest(".observacoes-modal"));
    });
  });

  document.querySelectorAll(".cancelar-alteracoes").forEach((botao) => {
    botao.addEventListener("click", (e) => {
      e.preventDefault();
      fecharModal(botao.closest(".observacoes-modal"));
    });
  });
});

async function carregarObservacoes() {
  const idTurma = getIdTurma();
  todasAsObservacoes = await api(`observacao/turma/${idTurma}`, "GET");
  renderizarTabela(todasAsObservacoes);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector("tbody");
  tbody.innerHTML = "";

  lista.forEach((obs) => {
    const tr = document.createElement("tr");
    tr.dataset.obs = obs.id;
    tr.innerHTML = `
      <td>${obs.aluno.nome}</td>
      <td>${obs.aluno.matricula}</td>
      <td>${obs.observacao.substring(0, 25)}${obs.observacao.length > 25 ? "..." : ""}</td>
      <td class="td-action">
        <button class="btn-edit" title="Editar">
          <i class="fa-solid fa-pen"></i>
        </button>
        <button class="btn-excluir" title="Excluir">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </td>
    `;
    tbody.appendChild(tr);

    tr.addEventListener("click", (e) => {
      if (e.target.closest(".btn-excluir")) {
        obsIdExcluindo = obs.id;
        abrirModal(modalExcluir);
        return;
      }
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        abrirModalEditar(obs);
      }
    });
  });
}

function abrirModalEditar(obs) {
  document.getElementById("nomeAluno").value = obs.aluno.nome;
  document.getElementById("editar-observacao-aluno").value = obs.observacao;
  modalEditar.querySelector("form").dataset.idObs = obs.id;
  abrirModal(modalEditar);
}

async function carregarAlunosParaSelect(idTurma, materiaId) {
  const alunosRes = await api(
    `mutante_materia/notas/turma/${idTurma}/materia/${materiaId}`,
    "GET",
  );
  const select = document.getElementById("selectAluno");
  select.innerHTML =
    '<option value="" disabled selected>Selecione um aluno</option>';
  alunosRes.forEach((aluno) => {
    const option = document.createElement("option");
    option.value = aluno.id;
    option.textContent = `${aluno.nome} (${aluno.matricula})`;
    select.appendChild(option);
  });
}

function abrirModal(modal) {
  if (modal) modal.style.display = "flex";
}

function fecharModal(modal) {
  if (modal) modal.style.display = "none";
}

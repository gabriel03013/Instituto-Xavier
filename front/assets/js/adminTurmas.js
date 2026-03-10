import { api } from "./utils.js";

const modalEditar = document.getElementById("modal-editar-turma");
const modalAdicionar = document.getElementById("modal-adicionar-turma");
const modalExcluir = document.getElementById("modal-excluir-turma");

const abrirModal = (modal) => {
  if (modal) modal.style.display = "flex";
};

const fecharModal = (modal) => {
  if (modal) modal.style.display = "none";
};

let turmaIdEditando = null;
let turmaIdExcluindo = null;
let todasAsTurmas = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTurmas();

  const btnAdicionar = document.getElementById("admin-adicionar");
  if (btnAdicionar) {
    btnAdicionar.addEventListener("click", () => {
      abrirModal(modalAdicionar);
    });
  }

  const searchInput = document.querySelector(".admin-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsTurmas.filter((t) => {
        const nomeTurma = `${t.serie}º Ano ${t.turma}`.toLowerCase();
        return nomeTurma.includes(termo);
      });
      renderizarTabela(filtradas);
    });
  }

  modalAdicionar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const serie = Number(document.getElementById("adicionar-turma-ano").value);
    const turma = document.getElementById("adicionar-turma-classe").value;

    await api("turma/", "POST", { serie, turma });
    fecharModal(modalAdicionar);
    e.target.reset();
    await carregarTurmas();
  });

  modalEditar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const serie = Number(document.getElementById("editar-turma-ano").value);
    const turma = document.getElementById("editar-turma-classe").value;

    await api(`turma/${turmaIdEditando}`, "PATCH", { serie, turma });
    fecharModal(modalEditar);
    await carregarTurmas();
  });

  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", async () => {
      await api(`turma/${turmaIdExcluindo}`, "DELETE");
      fecharModal(modalExcluir);
      await carregarTurmas();
    });

  document.querySelectorAll(".fechar-modal").forEach((botao) => {
    botao.addEventListener("click", () => {
      fecharModal(botao.closest(".admin-modal"));
    });
  });

  document.querySelectorAll(".cancelar-alteracoes").forEach((botao) => {
    botao.addEventListener("click", (e) => {
      e.preventDefault();
      fecharModal(botao.closest(".admin-modal"));
    });
  });
});

async function carregarTurmas() {
  todasAsTurmas = await api("turma/", "GET");
  renderizarTabela(todasAsTurmas);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector(".admin-table tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  lista.forEach((t) => {
    const tr = document.createElement("tr");
    tr.dataset.id = t.id;
    tr.dataset.serie = t.serie;
    tr.dataset.turma = t.turma;
    tr.innerHTML = `
      <td>${t.serie}º Ano ${t.turma}</td>
      <td>${t.alunos ? t.alunos.length : 0}</td>
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
  });

  carregarDados();
}

function carregarDados() {
  document.querySelectorAll(".admin-table tbody tr").forEach((linha) => {
    linha.addEventListener("click", (e) => {
      if (e.target.closest(".btn-excluir")) {
        turmaIdExcluindo = linha.dataset.id;
        abrirModal(modalExcluir);
        return;
      }
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        turmaIdEditando = linha.dataset.id;
        document.getElementById("editar-turma-ano").value = linha.dataset.serie;
        document.getElementById("editar-turma-classe").value =
          linha.dataset.turma;
        abrirModal(modalEditar);
      }
    });
  });
}

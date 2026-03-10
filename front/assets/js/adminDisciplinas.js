import { api } from "./utils.js";

const modalEditar = document.getElementById("modal-editar-disciplina");
const modalAdicionar = document.getElementById("modal-adicionar-disciplina");
const modalExcluir = document.getElementById("modal-excluir-disciplina");

const abrirModal = (modal) => {
  if (modal) modal.style.display = "flex";
};

const fecharModal = (modal) => {
  if (modal) modal.style.display = "none";
};

let materiaIdExcluindo = null;
let materiaIdEditando = null;
let todasAsMaterias = [];
let todosOsProfessores = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTudo();

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
      const filtradas = todasAsMaterias.filter((m) => {
        const nome = m.nome.toLowerCase();
        const professor = m.professorNome.toLowerCase();
        return nome.includes(termo) || professor.includes(termo);
      });
      renderizarTabela(filtradas);
    });
  }

  modalAdicionar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("adicionar-disciplina-nome").value;
    const professorId = document.getElementById(
      "adicionar-disciplina-docente",
    ).value;

    await api("materia/", "POST", { nome, professor_id: Number(professorId) });
    fecharModal(modalAdicionar);
    e.target.reset();
    await carregarTudo();
  });

  modalEditar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("editar-disciplina-nome").value;
    const professorId = document.getElementById(
      "editar-disciplina-docente",
    ).value;

    await api(`materia/${materiaIdEditando}`, "PATCH", {
      nome,
      professor_id: Number(professorId),
    });
    fecharModal(modalEditar);
    await carregarTudo();
  });

  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", async () => {
      await api(`materia/${materiaIdExcluindo}`, "DELETE");
      fecharModal(modalExcluir);
      await carregarTudo();
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

async function carregarTudo() {
  todosOsProfessores = await api("professor/", "GET");
  const materias = await api("materia/", "GET");

  todasAsMaterias = materias.map((m) => {
    const prof = todosOsProfessores.find((p) => p.id === m.professor_id);
    return {
      ...m,
      professorNome: prof ? prof.nome : "Sem professor",
    };
  });

  renderizarTabela(todasAsMaterias);
  popularSelectsProfessores();
}

function popularSelectsProfessores() {
  const selects = [
    document.getElementById("adicionar-disciplina-docente"),
    document.getElementById("editar-disciplina-docente"),
  ];

  selects.forEach((select) => {
    if (select) {
      const currentValue = select.value;
      select.innerHTML =
        '<option value="" disabled selected>Selecione um professor</option>';
      todosOsProfessores.forEach((p) => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = p.nome;
        select.appendChild(option);
      });
      if (currentValue) select.value = currentValue;
    }
  });
}

function renderizarTabela(lista) {
  const tbody = document.querySelector(".admin-table tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  lista.forEach((mat) => {
    const tr = document.createElement("tr");
    tr.dataset.id = mat.id;
    tr.dataset.nome = mat.nome;
    tr.dataset.professorId = mat.professor_id;
    tr.innerHTML = `
      <td>${mat.nome}</td>
      <td>${mat.professorNome}</td>
      <td>-</td>
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
        materiaIdExcluindo = linha.dataset.id;
        abrirModal(modalExcluir);
        return;
      }
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        materiaIdEditando = linha.dataset.id;
        document.getElementById("editar-disciplina-nome").value =
          linha.dataset.nome;
        document.getElementById("editar-disciplina-docente").value =
          linha.dataset.professorId;
        abrirModal(modalEditar);
      }
    });
  });
}

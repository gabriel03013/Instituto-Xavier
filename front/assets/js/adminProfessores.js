import { api } from "./utils.js";

const modalEditar = document.getElementById("modal-editar-professor");
const modalAdicionar = document.getElementById("modal-adicionar-professor");
const modalExcluir = document.getElementById("modal-excluir-professor");

const abrirModal = (modal) => {
  if (modal) modal.style.display = "flex";
};

const fecharModal = (modal) => {
  if (modal) modal.style.display = "none";
};

let profIdEditando = null;
let profIdExcluindo = null;
let todosOsProfessores = [];
let todasAsMaterias = [];

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTudo();

  const btnAdicionar = document.getElementById("admin-adicionar");
  if (btnAdicionar) {
    btnAdicionar.addEventListener("click", () => {
      popularSelectAdicionar();
      abrirModal(modalAdicionar);
    });
  }

  const searchInput = document.querySelector(".admin-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtrados = todosOsProfessores.filter((p) => {
        const nome = p.nome.toLowerCase();
        const usuario = p.usuario.toLowerCase();
        const materia =
          p.materias && p.materias.length > 0
            ? p.materias[0].nome.toLowerCase()
            : "";
        return (
          nome.includes(termo) ||
          usuario.includes(termo) ||
          materia.includes(termo)
        );
      });
      renderizarTabela(filtrados);
    });
  }

  modalAdicionar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("adicionar-professor-nome").value;
    const usuario = document.getElementById("adicionar-professor-login").value;
    const senha = document.getElementById("adicionar-professor-senha").value;
    const materia = document.getElementById(
      "adicionar-professor-materia",
    ).value;

    await api("professor/", "POST", { nome, usuario, senha, materia });
    fecharModal(modalAdicionar);
    e.target.reset();
    await carregarTudo();
  });

  modalEditar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("editar-professor-nome").value;
    const usuario = document.getElementById("editar-professor-login").value;
    const senha = document.getElementById("editar-professor-senha").value;
    const materia = document.getElementById("editar-professor-materia").value;

    const body = { nome, usuario, materia };
    if (senha) body.senha = senha;

    await api(`professor/${profIdEditando}`, "PATCH", body);
    fecharModal(modalEditar);
    await carregarTudo();
  });

  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", async () => {
      await api(`professor/${profIdExcluindo}`, "DELETE");
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
  const [profs, mats] = await Promise.all([
    api("professor/", "GET"),
    api("materia/", "GET"),
  ]);
  todosOsProfessores = profs;
  todasAsMaterias = mats;
  renderizarTabela(todosOsProfessores);
  popularSelectEditar();
}

function popularSelectAdicionar() {
  const select = document.getElementById("adicionar-professor-materia");
  if (!select) return;

  select.innerHTML =
    '<option value="" disabled selected>Selecione uma matéria</option>';

  const disponiveis = todasAsMaterias.filter((m) => !m.professor_id);
  disponiveis.forEach((m) => {
    const opt = document.createElement("option");
    opt.value = m.nome;
    opt.textContent = m.nome;
    select.appendChild(opt);
  });
}

function popularSelectEditar() {
  const select = document.getElementById("editar-professor-materia");
  if (!select) return;

  const currentVal = select.value;
  select.innerHTML = '<option value="">Nenhuma</option>';

  todasAsMaterias.forEach((m) => {
    const opt = document.createElement("option");
    opt.value = m.nome;
    opt.textContent = m.nome;
    select.appendChild(opt);
  });

  if (currentVal) select.value = currentVal;
}

function renderizarTabela(lista) {
  const tbody = document.querySelector(".admin-table tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  lista.forEach((prof) => {
    const materia =
      prof.materias && prof.materias.length > 0 ? prof.materias[0].nome : "-";
    const tr = document.createElement("tr");
    tr.dataset.id = prof.id;
    tr.dataset.nome = prof.nome;
    tr.dataset.usuario = prof.usuario;
    tr.dataset.materia = materia;
    tr.innerHTML = `
      <td>${prof.nome}</td>
      <td>${materia}</td>
      <td>${prof.usuario}</td>
      <td>••••••</td>
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
        profIdExcluindo = linha.dataset.id;
        abrirModal(modalExcluir);
        return;
      }
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        profIdEditando = linha.dataset.id;
        document.getElementById("editar-professor-nome").value =
          linha.dataset.nome;
        document.getElementById("editar-professor-login").value =
          linha.dataset.usuario;

        const materiaVal =
          linha.dataset.materia !== "-" ? linha.dataset.materia : "";
        document.getElementById("editar-professor-materia").value = materiaVal;

        document.getElementById("editar-professor-senha").value = "";
        abrirModal(modalEditar);
      }
    });
  });
}

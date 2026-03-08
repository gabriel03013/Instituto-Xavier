import { api } from "./utils.js";

const modalEditar = document.getElementById("modal-editar-aluno");
const modalAdicionar = document.getElementById("modal-adicionar-aluno");
const modalExcluir = document.getElementById("modal-excluir-aluno");

const abrirModal = (modal) => {
  if (modal) modal.style.display = "flex";
};

const fecharModal = (modal) => {
  if (modal) modal.style.display = "none";
};

let alunoIdExcluindo = null;
let alunoIdEditando = null;
let todosOsAlunos = [];

document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const turmaId = urlParams.get("turma");

  if (!turmaId) return;

  await carregarAlunos(turmaId);

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
      const filtrados = todosOsAlunos.filter((aluno) => {
        const nome = aluno.nome.toLowerCase();
        const matricula = aluno.matricula.toLowerCase();
        return nome.includes(termo) || matricula.includes(termo);
      });
      renderizarTabela(filtrados);
    });
  }

  const turmas = await api("turma/", "GET");
  const selectTurmaAdd = document.getElementById("adicionar-aluno-turma");
  const selectTurmaEdit = document.getElementById("editar-aluno-turma");

  const popularSelect = (select, defaultTurmaId = null) => {
    if (!select) return;
    select.innerHTML =
      '<option value="" disabled selected>Selecione a turma</option>';
    turmas.forEach((t) => {
      const option = document.createElement("option");
      option.value = t.id;
      option.textContent = `${t.serie}º Ano ${t.turma}`;
      if (defaultTurmaId && t.id == defaultTurmaId) {
        option.selected = true;
      } else if (!defaultTurmaId && t.id == turmaId) {
        // Default for add modal
        option.selected = true;
      }
      select.appendChild(option);
    });
  };

  popularSelect(selectTurmaAdd);
  popularSelect(selectTurmaEdit);

  modalAdicionar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const matricula = document.getElementById(
      "adicionar-aluno-matricula",
    ).value;
    const targetTurmaId = document.getElementById(
      "adicionar-aluno-turma",
    ).value;

    try {
      await api(
        `admin/create_registration?matricula=${encodeURIComponent(matricula)}&turma_id=${encodeURIComponent(targetTurmaId)}`,
        "POST",
      );

      fecharModal(modalAdicionar);
      e.target.reset();
      await carregarAlunos(turmaId);
      alert("Matrícula criada com sucesso! O aluno deve completar o cadastro.");
    } catch (error) {
      alert("Erro ao criar matrícula: " + error.message);
    }
  });

  modalEditar.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("editar-aluno-nome").value;
    const matricula = document.getElementById("editar-aluno-matricula").value;
    const targetTurmaId = document.getElementById("editar-aluno-turma").value;

    try {
      await api(`mutant/${alunoIdEditando}`, "PATCH", {
        nome,
        matricula,
        email: `${matricula}@instituto.com`,
        turma_id: Number(targetTurmaId),
      });

      fecharModal(modalEditar);
      await carregarAlunos(turmaId);
      alert("Aluno atualizado com sucesso!");
    } catch (error) {
      alert("Erro ao atualizar aluno: " + error.message);
    }
  });

  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", async () => {
      await api(`mutant/${alunoIdExcluindo}`, "DELETE");
      fecharModal(modalExcluir);
      await carregarAlunos(turmaId);
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

async function carregarAlunos(turmaId) {
  const turmaInfos = await api(`turma/${turmaId}`, "GET");
  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;
  todosOsAlunos = turmaInfos.alunos;
  renderizarTabela(todosOsAlunos);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector(".admin-table tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  lista.forEach((aluno) => {
    const tr = document.createElement("tr");
    tr.dataset.id = aluno.id;
    tr.dataset.nome = aluno.nome || "";
    tr.dataset.matricula = aluno.matricula;
    tr.dataset.turmaId = aluno.turma_id || "";

    const pendente = !aluno.nome || aluno.nome.trim() === "";
    const nomeDisplay = pendente
      ? `<span style="color: #999; font-style: italic;">Cadastro pendente</span>`
      : aluno.nome;

    tr.innerHTML = `
      <td>${nomeDisplay}</td>
      <td>${aluno.matricula}</td>
      <td>-</td>
      <td>-</td>
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
        alunoIdExcluindo = linha.dataset.id;
        abrirModal(modalExcluir);
        return;
      }
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        alunoIdEditando = linha.dataset.id;
        document.getElementById("editar-aluno-nome").value = linha.dataset.nome;
        document.getElementById("editar-aluno-matricula").value =
          linha.dataset.matricula;

        const selectTurmaEdit = document.getElementById("editar-aluno-turma");
        // Re-populando para garantir que o default role do 'turmaId' global não interfira
        // Ou apenas setando o value se já populado.
        if (selectTurmaEdit) {
          // Chamamos a função global popularSelect definida no DOMContentLoaded?
          // Ops, ela não é global. Vou mover ela ou apenas setar o value.
          // Vou assumir que popularSelect(selectTurmaEdit) foi chamado uma vez.
          selectTurmaEdit.value = linha.dataset.turmaId;
        }

        abrirModal(modalEditar);
      }
    });
  });
}

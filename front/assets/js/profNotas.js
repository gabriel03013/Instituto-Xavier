import { api, getIdTurma } from "./utils.js";

let todasAsNotas = [];

document.addEventListener("DOMContentLoaded", async () => {
  const idTurma = getIdTurma();
  const turmaInfos = await api(`turma/${idTurma}`, "GET");

  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;

  await carregarNotas();

  const searchInput = document.querySelector(".turma-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtrados = todasAsNotas.filter((n) => {
        return (
          n.nome.toLowerCase().includes(termo) ||
          n.matricula.toLowerCase().includes(termo)
        );
      });
      renderizarTabela(filtrados);
    });
  }

  document.getElementById("fechar-modal").addEventListener("click", () => {
    document.getElementById("editar-notas-modal").style.display = "none";
  });

  document
    .getElementById("cancelar-alteracoes")
    .addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById("editar-notas-modal").style.display = "none";
    });

  const form = document.getElementById("editar-notas-modal-content");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const idAluno = form.dataset.alunoId;
    const nota1 = document.getElementById("media1").value;
    const nota2 = document.getElementById("media2").value;

    await api(
      `mutante_materia/${idAluno}/${localStorage.getItem("materia_id")}`,
      "PATCH",
      {
        nota1: Number(nota1),
        nota2: Number(nota2),
      },
    );

    document.getElementById("editar-notas-modal").style.display = "none";
    await carregarNotas();
  });
});

async function carregarNotas() {
  const idTurma = getIdTurma();
  todasAsNotas = await api(
    `mutante_materia/notas/turma/${idTurma}/materia/${localStorage.getItem("materia_id")}`,
    "GET",
  );
  renderizarTabela(todasAsNotas);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector("tbody");
  tbody.innerHTML = "";

  lista.forEach((e) => {
    const tr = document.createElement("tr");
    tr.dataset.id = e.id;
    tr.dataset.alunoId = e.mutante_id;
    tr.innerHTML = `
      <td>${e.nome}</td>
      <td>${e.matricula}</td>
      <td>${e.nota1}</td>
      <td>${e.nota2}</td>
      <td>${e.media}</td>
      <td class="td-action">
        <button class="btn-edit" title="Editar">
          <i class="fa-solid fa-pen"></i>
        </button>
      </td>
    `;
    tbody.appendChild(tr);

    tr.addEventListener("click", (event) => {
      if (
        event.target.closest(".btn-edit") ||
        !event.target.closest("button")
      ) {
        abrirModalEditar(e);
      }
    });
  });
}

function abrirModalEditar(e) {
  const modal = document.getElementById("editar-notas-modal");
  const form = document.getElementById("editar-notas-modal-content");
  const inputNome = document.getElementById("selectAluno");
  const inputN1 = document.getElementById("media1");
  const inputN2 = document.getElementById("media2");

  modal.style.display = "flex";
  form.dataset.id = e.id;
  form.dataset.alunoId = e.mutante_id;
  inputNome.value = e.nome;
  inputN1.value = e.nota1;
  inputN2.value = e.nota2;
}

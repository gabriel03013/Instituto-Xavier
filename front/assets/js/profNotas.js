import { api } from "./utils.js";
import { getIdTurma } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const idTurma = getIdTurma();
  const turmaInfos = await api(`turma/${idTurma}`, "GET");
  console.log(turmaInfos);

  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;

  const notaRes = await api(
    `mutante_materia/notas/turma/${idTurma}/materia/${localStorage.getItem("materia_id")}`,
    "GET",
  );  

  notaRes.forEach((e) => {
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
    document.querySelector("tbody").appendChild(tr);

    tr.addEventListener("click", (event) => {
      if (
        event.target.closest(".btn-edit") ||
        !event.target.closest("button")
      ) {
        comportamentoModal(e.id, e.mutante_id, e.nome, e.nota1, e.nota2);
      }
    });
  });

  document
    .getElementById("fechar-modal")
    .addEventListener("click", () => comportamentoModal());

  const form = document.getElementById("editar-notas-modal-content");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const idAluno = form.dataset.alunoId;
    const nota1 = document.getElementById("media1").value;
    const nota2 = document.getElementById("media2").value;

    console.log("Dados:", { idAluno, nota1, nota2 });

    await api(
      `mutante_materia/${+idAluno}/${+localStorage.getItem("materia_id")}`,
      "PATCH",
      {
        nota1: +nota1,
        nota2: +nota2,
      },
    );

    comportamentoModal();
    location.reload(); // Recarregar para ver as notas novas
  });
});

const comportamentoModal = (
  id = "",
  alunoId = "",
  nome = "",
  n1 = "",
  n2 = "",
) => {
  const modal = document.getElementById("editar-notas-modal");
  const form = document.getElementById("editar-notas-modal-content");
  const inputNome = document.getElementById("selectAluno");
  const inputN1 = document.getElementById("media1");
  const inputN2 = document.getElementById("media2");

  if (modal.style.display === "") {
    modal.style.display = "flex";
    if (id) form.dataset.id = id;
    if (alunoId) form.dataset.alunoId = alunoId;
    if (nome) inputNome.value = nome;
    if (n1 !== "") inputN1.value = n1;
    if (n2 !== "") inputN2.value = n2;
  } else {
    modal.style.display = "";
    form.dataset.id = "";
    form.dataset.alunoId = "";
  }
};

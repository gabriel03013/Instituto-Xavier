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
  console.log(notaRes);

  notaRes.forEach((e) => {
    const tr = document.createElement("tr");
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
        comportamentoModal(e.nome, e.nota1, e.nota2);
      }
    });
  });

  document
    .getElementById("fechar-modal")
    .addEventListener("click", () => comportamentoModal());
});

const comportamentoModal = (nome = "", n1 = "", n2 = "") => {
  const modal = document.getElementById("editar-notas-modal");
  const inputNome = document.getElementById("selectAluno");
  const inputN1 = document.getElementById("media1");
  const inputN2 = document.getElementById("media2");

  if (modal.style.display === "") {
    modal.style.display = "flex";
    if (nome) inputNome.value = nome;
    if (n1 !== "") inputN1.value = n1;
    if (n2 !== "") inputN2.value = n2;
    console.log("abriu");
  } else {
    modal.style.display = "";
  }
};

// ! TODO -> Média preview conforme digitação
const span = document.getElementById("media-final-preview");

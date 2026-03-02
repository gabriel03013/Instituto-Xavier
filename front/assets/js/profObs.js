import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const idTurma = getIdTurma();
  const turmaInfos = await api(`turma/${idTurma}`, "GET");
  console.log(turmaInfos);

  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;

  const obsRes = await api(`observacao/turma/${idTurma}`, "GET");

  obsRes.forEach((obs) => {
    const tr = document.createElement("tr");
    tr.dataset.obs = obs.observacao;
    tr.innerHTML = `
            <td>${obs.aluno.nome}</td>
            <td>${obs.aluno.matricula}</td>
            <td>${obs.observacao.substring(0, 25)}...</td>
            <td class="td-action">
                <button class="btn-edit" title="Editar">
                    <i class="fa-solid fa-pen"></i>
                </button>
                <button class="btn-excluir">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </td>
        `;
    document.querySelector("tbody").appendChild(tr);

    tr.addEventListener("click", (e) => {
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        const nome = tr.querySelector("td:first-child").textContent;
        const observacao = tr.dataset.obs;
        document.getElementById("nomeAluno").value = nome;
        document.getElementById("observacao-aluno").value = observacao;
        abrirModal(modalEditar);
      }
    });
  });
});

const modalEditar = document.querySelector(
  ".observacoes-modal:not(.modal-adicionar)",
);
const modalAdicionar = document.querySelector(".modal-adicionar");

const getIdTurma = () => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("turma");
};

const abrirModal = (modal) => {
  modal.style.display = "flex";
};

const fecharModal = (modal) => {
  modal.style.display = "none";
};

document
  .getElementById("adicionar-observação")
  .addEventListener("click", () => {
    abrirModal(modalAdicionar);
  });

document.querySelectorAll(".fechar-modal").forEach((botao) => {
  botao.addEventListener("click", () => {
    const modal = botao.closest(".observacoes-modal");
    fecharModal(modal);
  });
});

document.querySelectorAll("#cancelar-alteracoes").forEach((botao) => {
  botao.addEventListener("click", (e) => {
    e.preventDefault();
    const modal = botao.closest(".observacoes-modal");
    fecharModal(modal);
  });
});

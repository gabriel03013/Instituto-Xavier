import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const idTurma = getIdTurma();
  const materiaId = localStorage.getItem("materia_id");

  const turmaInfos = await api(`turma/${idTurma}`, "GET");
  document.querySelector(".turma-titulo").textContent =
    `${turmaInfos.serie}º ANO ${turmaInfos.turma}`;

  await carregarObservacoes(idTurma);

  await carregarAlunos(idTurma, materiaId);

  const formEditar = document.querySelector(
    ".observacoes-modal:not(.modal-adicionar) form",
  );

  formEditar.addEventListener("submit", async (e) => {
    e.preventDefault();
    const idObs = formEditar.dataset.idObs;
    const novaObs = document.getElementById("editar-observacao-aluno").value;

    console.log("Submit Editar:", { idObs, novaObs });

    await api(`observacao/${idObs}`, "PATCH", { observacao: novaObs });

    fecharModal(modalEditar);
    carregarObservacoes(idTurma);
  });

  const formAdicionar = document.querySelector(".modal-adicionar form");
  formAdicionar.addEventListener("submit", async (e) => {
    e.preventDefault();
    const mmId = document.getElementById("selectAluno").value;
    const textoObs = document.getElementById(
      "adicionar-observacao-aluno",
    ).value;

    console.log("Submit Adicionar:", { mmId, textoObs });

    await api(`observacao/`, "POST", {
      mutantesmaterias_id: +mmId,
      observacao: textoObs,
      data: new Date().toISOString().split("T")[0],
    });

    fecharModal(modalAdicionar);
    carregarObservacoes(idTurma);
  });
});

async function carregarObservacoes(idTurma) {
  const obsRes = await api(`observacao/turma/${idTurma}`, "GET");
  const tbody = document.querySelector("tbody");
  tbody.innerHTML = "";

  obsRes.forEach((obs) => {
    const tr = document.createElement("tr");
    tr.dataset.obs = obs.id;
    tr.dataset.aluno = obs.aluno.id;
    tr.dataset.texto = obs.observacao;
    tr.innerHTML = `
            <td>${obs.aluno.nome}</td>
            <td>${obs.aluno.matricula}</td>
            <td>${obs.observacao.substring(0, 25)}${obs.observacao.length > 25 ? "..." : ""}</td>
            <td class="td-action">
                <button class="btn-edit" title="Editar">
                    <i class="fa-solid fa-pen"></i>
                </button>
                <button class="btn-excluir">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </td>
        `;
    tbody.appendChild(tr);

    tr.addEventListener("click", (e) => {
      if (e.target.closest(".btn-edit") || !e.target.closest("button")) {
        const nome = tr.querySelector("td:first-child").textContent;
        const observacao = tr.dataset.texto;
        const idObs = tr.dataset.obs;

        document.getElementById("nomeAluno").value = nome;
        document.getElementById("editar-observacao-aluno").value = observacao;

        const formEditar = document.querySelector(
          ".observacoes-modal:not(.modal-adicionar) form",
        );
        formEditar.dataset.idObs = idObs;

        abrirModal(modalEditar);
      }

      if (e.target.closest(".btn-excluir")) {
        if (confirm("Deseja realmente excluir esta observação?")) {
          const idObs = tr.dataset.obs;
          api(`observacao/${idObs}`, "DELETE").then(() => {
            carregarObservacoes(getIdTurma());
          });
        }
      }
    });
  });
}

async function carregarAlunos(idTurma, materiaId) {
  try {
    const alunosRes = await api(
      `mutante_materia/notas/turma/${idTurma}/materia/${materiaId}`,
      "GET",
    );
    const select = document.getElementById("selectAluno");

    alunosRes.forEach((aluno) => {
      const option = document.createElement("option");
      option.value = aluno.id;
      option.textContent = `${aluno.nome} (${aluno.matricula})`;
      select.appendChild(option);
    });
  } catch (error) {
    console.error("Erro ao carregar alunos:", error);
  }
}

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

document.querySelectorAll(".cancelar-alteracoes").forEach((botao) => {
  botao.addEventListener("click", (e) => {
    e.preventDefault();
    const modal = botao.closest(".observacoes-modal");
    fecharModal(modal);
  });
});

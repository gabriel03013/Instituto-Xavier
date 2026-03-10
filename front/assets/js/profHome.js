import { api } from "./utils.js";

let professorData = null;

document.addEventListener("DOMContentLoaded", async () => {
  const userId = localStorage.getItem("userId");

  const profRes = await api(`professor/${userId}`, "GET");
  professorData = profRes;
  console.log(profRes);

  if (profRes.materias && profRes.materias.length > 0) {
    document.getElementById("materia-professor").textContent =
      profRes.materias[0].nome;
  }
  document.getElementById("nome-professor").textContent = profRes.nome;

  preencherModal(profRes);

  const { dashboard: dash } = await api(
    `professor/dashboard?id_professor=${userId}`,
    "GET",
  );
  document.getElementById("total-alunos").textContent = dash.total_alunos;
  document.getElementById("media-notas").textContent =
    dash.media_notas.toFixed(2);
  document.getElementById("total-observacoes").textContent =
    dash.total_observacoes;
});

const modal = document.getElementById("editar-perfil-modal");
const inputUsuario = document.getElementById("usuario");
const inputSenha = document.getElementById("senha");

function preencherModal(prof) {
  const modalNome = document.querySelector("#form-inputs > div:first-child h4");
  const modalMateria = document.querySelector(
    "#form-inputs > div:first-child p",
  );

  if (modalNome) modalNome.textContent = prof.nome;
  if (modalMateria)
    modalMateria.textContent =
      prof.materias && prof.materias.length > 0
        ? prof.materias[0].nome
        : "Sem matéria";

  inputUsuario.value = prof.usuario || "";
  inputSenha.value = "";

  inputUsuario.disabled = false;
  inputSenha.disabled = false;
}

document.getElementById("editar-perfil").addEventListener("click", () => {
  if (professorData) preencherModal(professorData);
  modal.style.display = "flex";
});

document.getElementById("fechar-modal").addEventListener("click", () => {
  modal.style.display = "";
});

document
  .getElementById("cancelar-alteracoes-btn")
  .addEventListener("click", (e) => {
    e.preventDefault();
    modal.style.display = "";
  });

document
  .getElementById("salvar-alteracoes-btn")
  .addEventListener("click", async (e) => {
    e.preventDefault();

    const userId = localStorage.getItem("userId");
    const novoUsuario = inputUsuario.value.trim();
    const novaSenha = inputSenha.value.trim();

    if (!novoUsuario) {
      return;
    }

    const body = {};
    if (novoUsuario !== professorData.usuario) {
      body.usuario = novoUsuario;
    }
    if (novaSenha) {
      body.senha = novaSenha;
    }

    if (Object.keys(body).length === 0) {
      modal.style.display = "";
      return;
    }

    try {
      const updated = await api(`professor/${userId}`, "PATCH", body);
      professorData = updated;

      document.getElementById("nome-professor").textContent = updated.nome;
      if (updated.materias && updated.materias.length > 0) {
        document.getElementById("materia-professor").textContent =
          updated.materias[0].nome;
      }

      modal.style.display = "";
    } catch (err) {
      console.error("erro ao atualizar perfil:", err);
    }
  });

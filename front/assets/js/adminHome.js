import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const kpis = await api("admin/kpis", "GET");

  document.querySelector("#total-alunos p").textContent = kpis.total_alunos;
  document.querySelector("#total-professores p").textContent =
    kpis.total_professores;
  document.querySelector("#total-turmas p").textContent = kpis.total_turmas;
});

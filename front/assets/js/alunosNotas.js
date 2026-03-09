import { api } from "./utils.js";
import { gerarBoletimPDF } from "./pdf.js";

let todasAsNotas = [];

document.addEventListener("DOMContentLoaded", async () => {
  const userId = localStorage.getItem("userId");
  await carregarNotas(userId);

  const searchInput = document.querySelector(".aluno-search input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const termo = e.target.value.toLowerCase();
      const filtradas = todasAsNotas.filter((n) => {
        return (
          n.professor.toLowerCase().includes(termo) ||
          n.materia.toLowerCase().includes(termo)
        );
      });
      renderizarTabela(filtradas);
    });
  }

  document
    .getElementById("baixar-boletim")
    .addEventListener("click", async () => {
      const alunoRes = await api(`mutant/info?id_mutante=${userId}`);
      const aluno = {
        nome: alunoRes.nome,
        turma: alunoRes.turma,
      };

      const materias = todasAsNotas.map((item) => ({
        nome: item.materia,
        professor: item.professor,
        nota1: item.nota1,
        nota2: item.nota2,
        media_final: item.media_final,
        status: item.status,
      }));

      const pdf = gerarBoletimPDF(aluno, materias);
      pdf.save(`Boletim_${alunoRes.nome}.pdf`);
    });
});

async function carregarNotas(userId) {
  todasAsNotas = await api(`mutant/my_grades?id_mutante=${userId}`);
  renderizarTabela(todasAsNotas);
}

function renderizarTabela(lista) {
  const tbody = document.querySelector(".aluno-table tbody");
  tbody.innerHTML = "";

  lista.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.professor}</td>
      <td>${item.materia}</td>
      <td>${item.nota1}</td>
      <td>${item.nota2}</td>
      <td>${item.media_final}</td>
      <td class="${item.status === "Aprovado" ? "status-aprovado" : "status-reprovado"}">${item.status}</td>
    `;
    tbody.appendChild(tr);
  });
}

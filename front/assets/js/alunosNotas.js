import { api } from "./utils.js";
import { gerarBoletimPDF } from "./pdf.js";

let pdfGerado;

document.addEventListener("DOMContentLoaded", async () => {
    const res = await api(`mutant/my_grades?id_mutante=${localStorage.getItem("userId")}`);

    res.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.professor}</td>
            <td>${item.materia}</td>
            <td>${item.nota1}</td>
            <td>${item.nota2}</td>
            <td>${item.media_final}</td>
            <td class="${item.status === "Aprovado" ? "status-aprovado" : "status-reprovado"}">${item.status}</td>
        `;
        document.querySelector(".aluno-table tbody").appendChild(tr);
    })

    document.getElementById("baixar-boletim").addEventListener("click", async () => {
        const alunoRes = await api(`mutant/info?id_mutante=${localStorage.getItem("userId")}`);


        const aluno = {
            nome: alunoRes.nome,
            turma: alunoRes.turma,
        }

        const materias = res.map((item) => {
            return {
                nome: item.materia,
                professor: item.professor,
                nota1: item.nota1,
                nota2: item.nota2,
                media_final: item.media_final,
                status: item.status,
            }
        })

        pdfGerado = gerarBoletimPDF(aluno, materias);

    });
});

document.getElementById("baixar-boletim").addEventListener("click", () => {
    pdfGerado.save(`Boletim_${alunoRes.nome}.pdf`);
});
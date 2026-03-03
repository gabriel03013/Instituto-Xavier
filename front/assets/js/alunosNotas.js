import { api } from "./utils.js";

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

});
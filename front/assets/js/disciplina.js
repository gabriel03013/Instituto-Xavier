import {api} from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
    const aluno = await api(`mutant/info?id_mutante=${localStorage.getItem("userId")}`);

    document.getElementById("nome-aluno").textContent = aluno.nome;
    document.getElementById("turma-aluno").textContent = aluno.turma;

    const materias = await api(`mutant/my_subjects?id_mutante=${localStorage.getItem("userId")}`);

    materias.forEach((materia) => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
            <div class="card-accent dark"></div>
            <img src="../assets/images/image 9.svg" class="avatar">
            <div class="card-text">
                <h2>${materia.materia}</h2>
                <span>${materia.professor}</span>
            </div>
        `;
        document.querySelector(".container").appendChild(card);
    });
        
});
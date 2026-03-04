import {api} from "./utils.js"

const urlParams = new URLSearchParams(window.location.search)
const tipo = urlParams.get("tipo")
let destinoFinal = ""

if (tipo === "obs") {
  destinoFinal = "observacoes.html";
  document.getElementById("obs").classList.add("aba-professor-ativa");
} else if (tipo === "notas") {
  destinoFinal = "notas.html";
  document.getElementById("notas").classList.add("aba-professor-ativa");
} else {
  throw new Error(`Tipo ${tipo} não é valido.`);
}

document.addEventListener("DOMContentLoaded", async () => {
    const turmasRes = await api("turma", "GET")
    console.log(turmasRes);
    
    turmasRes.forEach(turma => {
        const div = document.createElement("div")
        div.classList.add("turma-div")
        div.setAttribute("data-turma", turma.id)
        div.innerHTML = `
            <h2>${turma.serie}º ANO ${turma.turma}</h2>
            <p>${turma.alunos.length} alunos</p>
        `
        document.getElementById("turmas").appendChild(div)
    })


document.querySelectorAll(".turma-div").forEach((e) => {
  e.addEventListener("click", () => {
    window.location.href = `./${destinoFinal}?turma=${e.getAttribute("data-turma")}`;
  });
});
})



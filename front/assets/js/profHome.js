import {api} from "./utils.js"

document.addEventListener("DOMContentLoaded", async () => {
    const profRes = await api(`professor/${localStorage.getItem("userId")}` , "GET")
    console.log(profRes);
    
    
    document.getElementById("materia-professor").textContent = profRes.materias[0].nome;   
    document.getElementById("nome-professor").textContent = profRes.nome

    const dashRes = await api(`professor/dashboard?id_professor=${localStorage.getItem("userId")}` , "GET")
    document.getElementById("total-alunos").textContent = dashRes.total_alunos
    document.getElementById("media-notas").textContent = dashRes.media_notas.toFixed(2)
    document.getElementById("total-observacoes").textContent = dashRes.total_observacoes

})


const modal = document.getElementById("editar-perfil-modal")

document.getElementById("editar-perfil").addEventListener("click", () => {
    console.log(modal.style)
    modal.style.display == "" ? modal.style.display = "flex" : modal 
})

document.getElementById("fechar-modal").addEventListener("click", () => {
    modal.style.display = ""
})
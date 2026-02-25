const modal = document.getElementById("editar-perfil-modal")

document.getElementById("editar-perfil").addEventListener("click", () => {
    console.log(modal.style)
    modal.style.display == "" ? modal.style.display = "flex" : modal 
})

document.getElementById("fechar-modal").addEventListener("click", () => {
    modal.style.display = ""
})
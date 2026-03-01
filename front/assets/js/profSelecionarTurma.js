const urlParams = new URLSearchParams(window.location.search)
const tipo = urlParams.get("tipo")
let destinoFinal = ""

if(tipo === "obs") {
    destinoFinal = "observacoes.html"
    document.getElementById("obs").classList.add("aba-professor-ativa")
} else if(tipo === "notas") {
    destinoFinal = "notas.html"
    document.getElementById("notas").classList.add("aba-professor-ativa")
} else {
    throw new Error(`Tipo ${tipo} não é valido.`)
}

document.querySelectorAll(".turma-div").forEach(e => {
    e.addEventListener("click", () => {
        window.location.href = `./${destinoFinal}?turma=${e.getAttribute("data-turma")}`
    })
})



document.addEventListener("DOMContentLoaded", () => {
    
    fetch("http://127.0.0.1:8000/professor/dashboard?id_professor=2") //parametro teste
    .then(res => res.json())
    .then(data => { // data é um array aqui

        const dados = data.notas_turma_materia

        const turmas = dados.map(d => d.turma)
        const materias = dados.map(d => d.materia)
        const medias = dados.map(d => d.media)
        
        console.log("Médias", medias);
        // Visualizar as médias por turma para ver qual sala sofre de retardo mental
        const trace = { 
            x: turmas,
            y: medias,
            type: "bar"
        }
        
        // Dá pra criar a div no html direto tambem
        const div = document.createElement("div")
        div.setAttribute("id", "grafico")
        document.body.appendChild(div)
        
        Plotly.newPlot("grafico", [trace])
    })
})
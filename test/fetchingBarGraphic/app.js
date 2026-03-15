


document.addEventListener("DOMContentLoaded", () => {
    
    fetch("http://127.0.0.1:8000/professor/dashboard?id_professor=2") //parametro teste
    .then(res => res.json())
    .then(data => { // data é um array aqui

        const dados = data.notas_turma_materia

        const turmas = dados.map(d => d.turma)
        const medias = dados.map(d => d.media)
        
        // Visualizar as médias por turma para ver qual sala sofre de retardo mental
        const trace = { 
            x: turmas,
            y: medias,
            type: "bar",
        }

        const layoutProf = {
            title: "Gráfico Professor"
        };
        
        // Dá pra criar a div no html direto tambem
        const div = document.createElement("div")
        div.setAttribute("id", "grafico-professor")
        div.style.height = "500px"
        div.style.width = "900px";
        document.body.appendChild(div)
        
        Plotly.newPlot("grafico-professor", [trace], layoutProf)
    })
})




document.addEventListener("DOMContentLoaded", () => {
    
    fetch("http://127.0.0.1:8000/admin/visao-geral")
    .then(res => res.json())
    .then(data => {

        const groupedTurmaMaterias = data.reduce((acc, curr) => {
            if (!acc[curr.turma]) {
                acc[curr.turma] = [];
            }

            acc[curr.turma].push({
                materia: curr.materia,
                media: curr.media
            });

            return acc;
        }, {});

        console.log(groupedTurmaMaterias);

        const traces = [];

        Object.entries(groupedTurmaMaterias).forEach(([turma, materias]) => {

            const nomesMaterias = materias.map(m => m.materia);
            const medias = materias.map(m => m.media);

            traces.push({
                x: nomesMaterias,
                y: medias,
                type: "bar",
            });
        });

        const layoutAdmin = {
            title: "Gráfico Admin"
        };

        const div = document.createElement("div");
        div.setAttribute("id", "grafico-admin");
        div.style.height = "500px"
        div.style.width = "900px";
        document.body.appendChild(div);

        Plotly.newPlot("grafico-admin", traces, layoutAdmin);
    });
});
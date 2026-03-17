import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const kpis = await api("admin/kpis", "GET");

  document.querySelector("#total-alunos p").textContent = kpis.total_alunos;
  document.querySelector("#total-professores p").textContent = kpis.total_professores;
  document.querySelector("#total-turmas p").textContent = kpis.total_turmas;


  const dashRes = await api("admin/visao-geral", "GET"); //Array de dicts

  const dadosBarras = dashRes.dashboards.barras;

  const groupedTurmaMaterias = dadosBarras.reduce((acc, curr) => {
      if (!acc[curr.turma]) {
          acc[curr.turma] = [];
      }

      acc[curr.turma].push({
          materia: curr.materia,
          media: curr.media
      });

      return acc;
  }, {});

  const tracesBarras = [];

  Object.entries(groupedTurmaMaterias).forEach(([turma, materias]) => {
      const nomesMaterias = materias.map(m => m.materia);
      const medias = materias.map(m => m.media);

      tracesBarras.push({
          x: nomesMaterias,
          y: medias,
          type: "bar",
          name: turma,
      });
  });

  const layoutBarras = {
    title: "Média da turma em cada matéria",
    barmode: "group",
    yaxis: {
      dtick: 2,
      range: [0, 10] 
    }
  };

  Plotly.newPlot("grafico-barras", tracesBarras, layoutBarras);


  // Gráfico de Pizza:
  const dadosPizza = dashRes.dashboards.pizza;

  const coresPorSituacao = {
    "Aprovado": "#4CAF50",
    "Recuperação": "#FFC107",
    "Reprovado": "#F44336",
    "Sem Notas": "#9E9E9E"
  }

  const tracesPizza = [{
    values: dadosPizza.map(d => d.quantidade),
    labels: dadosPizza.map(d => d.situacao),
    type: "pie",
    textinfo: 'label+value', // conteúdo dos labels (valor, porcentagem, etc.)
    textposition: "outside", // Labels fora da pizza
    marker: {
      colors: dadosPizza.map(d => coresPorSituacao[d.situacao]) // Cor pra cada situação
    }
  }];

  const layoutPizza = {
    title: "Situação dos alunos",
    showlegend: false,
  };

  Plotly.newPlot("grafico-pizza", tracesPizza, layoutPizza)
});

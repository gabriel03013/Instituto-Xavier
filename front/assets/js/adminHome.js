const ctx = document.getElementById("meuGrafico");

new Chart(ctx, {
  type: "bar", 
  data: {
    labels: ["João", "Maria", "Pedro", "Ana"],
    datasets: [
      {
        label: "Notas",
        data: [8, 7, 9, 6],
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
  },
});

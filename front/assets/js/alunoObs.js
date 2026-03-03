import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", async () => {
  const id = localStorage.getItem("userId");
  const tbody = document.querySelector("tbody");
  const modal = document.querySelector(".observacoes-modal");

  
  try {
    const response = await api(`observacao/aluno/${id}`);

    response.forEach((item) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
              <td>${item.professor}</td>
              <td>${item.materia}</td>
              <td>${item.observacao.substring(0, 10)}${item.observacao.length > 10 ? "..." : ""}</td>
          `;

      
      tr.addEventListener("click", () => {
        document.getElementById("modal-professor").textContent = item.professor;
        document.getElementById("modal-materia").textContent = item.materia;
        document.getElementById("modal-texto").textContent = item.observacao;
        modal.style.display = "flex";
      });

      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar observações:", error);
  }

  
  document.querySelectorAll(".fechar-modal").forEach((button) => {
    button.addEventListener("click", (e) => {
      modal.style.display = "none";
    });
  });

  
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

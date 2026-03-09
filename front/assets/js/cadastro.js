import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const matricula = document.getElementById("matricula").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
      await api("mutant/complete_registration", "PUT", {
        nome,
        matricula,
        email,
        senha,
      });

      alert("Cadastro concluído com sucesso! Agora você pode fazer login.");
      window.location.href = "../index.html";
    } catch (error) {
      alert("Erro ao concluir cadastro. Verifique sua matrícula.");
    }
  });

  const loginLink = document.createElement("p");
  loginLink.innerHTML =
    'Já possui cadastro? <a href="../index.html" style="color: var(--roxo-escuro); font-weight: bold; text-decoration: none;">Faça login</a>';
  loginLink.style.marginTop = "1rem";
  loginLink.style.fontSize = "1.4rem";
  loginLink.style.textAlign = "center";
  form.appendChild(loginLink);
});

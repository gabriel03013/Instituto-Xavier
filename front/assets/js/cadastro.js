import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = capitalize(document.getElementById("nome").value).trim();
    const matricula = document.getElementById("matricula").value.trim();
    const email = document.getElementById("email").value.toLowerCase().trim();
    const senha = document.getElementById("senha").value.trim();

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


function capitalize(str) {
  const stringArr = str.split(" ");
  stringArr.forEach((word, index) => {
    stringArr[index] = word.charAt(0).toUpperCase() + word.slice(1);
  });
  return stringArr.join(" ");
}
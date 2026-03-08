import { api } from "./utils.js";
const form = document.querySelector("form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const [user, senha] = form.querySelectorAll("input");

  try {
    const res = await api("login", "POST", {
      username: user.value,
      password: senha.value,
    });

    localStorage.setItem("token", res.access_token);
    localStorage.setItem("userId", res.id);
    localStorage.setItem("userTipo", res.tipo);
    localStorage.setItem("materia_id", res.materia_id);

    const pastas = {
      professor: "professor",
      mutante: "aluno",
      admin: "admin",
    };

    const lower = res.tipo.toLowerCase();
    const pastaDestino = pastas[lower];

    window.location.href = `./pages/${pastaDestino}/index.html?tipo=${pastaDestino}&id=${res.id}`;
  } catch (e) {
    document.getElementById("erro").style.display = "flex";
  }
});

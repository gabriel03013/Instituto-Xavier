import { api } from "./utils.js";
const form = document.querySelector("form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const [user, senha] = form.querySelectorAll("input");

  try {
    const res = await api("token", "POST", {
      username: user.value,
      password: senha.value,
    });

    localStorage.setItem("token", res.access_token);
    localStorage.setItem("userId", res.id);
    localStorage.setItem("userTipo", res.tipo);
    localStorage.setItem("materia_id", res.materia_id);

    window.location.href = `./pages/${res.tipo.toLowerCase()}/index.html?tipo=${res.tipo.toLowerCase()}&id=${res.id}`;
  } catch (e) {
    document.getElementById("erro").style.display = "flex";
  }
});

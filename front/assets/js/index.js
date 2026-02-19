import { api } from "./utils.js";
const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const [user, senha] = form.querySelectorAll("input");

  try {
    const res = api("login", "POST", {
      user,
      senha,
    });

    window.location.href = `./pages/${res.tipo.toLowerCase()}/index.html?tipo=${res.tipo.toLowerCase()}&id=${res.id}`
  } catch (e) {
    document.getElementById("erro").style.display = "flex";
  }
});
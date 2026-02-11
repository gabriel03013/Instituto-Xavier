const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
    e.preventDefault();

    const [user, senha] = form.querySelectorAll("input");

    console.log(user.value, senha.value)
})
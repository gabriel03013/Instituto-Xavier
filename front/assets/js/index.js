const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("dsakdkla")
    const user = form.querySelector("#user").value;
    const senha = form.querySelector("#senha").value;

    console.log(user, senha)
})
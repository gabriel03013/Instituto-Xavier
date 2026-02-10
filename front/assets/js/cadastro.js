const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("dsakdkla")
    const user = form.querySelector("#nome").value;
    const matricula = form.querySelector("#matricula").value;
    const email = form.querySelector("#email").value;
    const senha = form.querySelector("#senha").value;



    console.log(user, matricula, email, senha)
})
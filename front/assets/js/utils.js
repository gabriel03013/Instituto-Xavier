export async function api(endpoint, metodo = "GET", body = null) {
  const headers = {};
  const token = localStorage.getItem("token");
  if (token && token !== "null" && token !== "undefined") {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let processedBody = body;
  if (
    body &&
    !(body instanceof FormData) &&
    !(body instanceof URLSearchParams)
  ) {
    if (endpoint === "login") {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
      processedBody = new URLSearchParams(body).toString();
    } else {
      headers["Content-Type"] = "application/json";
      processedBody = JSON.stringify(body);
    }
  }

  const res = await fetch(`http://127.0.0.1:8000/${endpoint}`, {
    method: metodo,
    headers: headers,
    body: processedBody,
  });

  if (!res.ok) throw new Error("Erro na requisição");

  return res.json();
}

export const getIdTurma = () => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("turma");
};

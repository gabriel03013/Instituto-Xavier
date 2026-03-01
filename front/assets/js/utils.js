export async function api(endpoint, metodo = "GET", body = null) {
  const headers = {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };

  let processedBody = body;
  if (
    body &&
    !(body instanceof FormData) &&
    !(body instanceof URLSearchParams)
  ) {
    if (endpoint === "token") {
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

export async function api(endpoint, metodo = "GET", body = null) {
  const res = await fetch(`apiUrl/${endpoint}`, {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : null,
  });

  if (!res.ok) throw new Error("Erro na requisição");

  return res.json();
}

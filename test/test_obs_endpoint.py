import requests

try:
    res = requests.get('http://127.0.0.1:8000/mutante_materia/notas/turma/1/materia/1')
    print("Status code:", res.status_code)
    print("Response:", res.text[:200])
except Exception as e:
    print("Error:", e)

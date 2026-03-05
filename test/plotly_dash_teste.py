import plotly.express as px
import pandas as pd

from dao.dashboard_professor import DashboardProfessorDAO
from database import Session

session = Session()
dash = DashboardProfessorDAO(session=session)

info_kpi = dash.obter_dashboard(id_professor=1)
info_notas = dash.obter_notas_por_turma_materia(id_professor=1)
info_situacao = dash.obter_situacao_alunos(id_professor=1)

print(info_kpi)

info_notas = pd.DataFrame(info_notas)
info_notas = info_notas.groupby("materia")

fig_notas = px.bar(
    info_notas,
    x='turma',
    y='media'
)
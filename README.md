<h1>📚Instituto Xavier</h1>
<p>Plataforma de gerenciamento escolar com usabilidade para alunos e professores. A nossa aplicação une alunos e professores com distribuição de notas, visibilidade de boletim e gerenciamento de alunos e turmas.</p>

<hr>

<h2>⚙️Principais funcionalidades: </h2>
<h3>👨‍🏫Para professores:</h3>
  <ul>
    <li>Gerenciamento de alunos e turmas</li>
    <li>Distribuição de notas e observações</li>
    <li>Visualização em dashboards de desempenho da turma</li>
  </ul>
<h3>🧑‍🎓Para alunos</h3>
  <ul>
    <li>Visualização de notas por disciplina</li>
    <li>Geração de boletim</li>
  </ul>

<hr>
<h2>💻Executar o Projeto localmente</h2>

<ul>
  <li>
    <h3>Passo 0: Clonar o repositório.</h3>
    <p>Execute o código abaixo para clonar esse repositório em sua máquina:</p>
    <code>git clone link_aqui</code>
  </li>
  
  <li>
    <h3>Passo 1: Instalação das dependências e criação do ambiente virtual</h3>
    <p>Para instalar as bibliotecas necessárias, execute os comandos abaixo (Windows):</p>
    <code>cd api</code><br>
    <code>make prepare-venvironment</code><br>
    <code>.venv\Scripts\activate</code>
  </li>

  <li>
    <h3>Passo 3: Rodando via Uvicorn</h3>
    <p>Fácil né? agora para rodar o projeto, basta executar o comando abaixo (lembre-se de pedir o .env para os admins):</p>
    <code>uvicorn main:app --app-dir src --reload</code>
  </li>
</ul>
<br>

<p><b>Muito bem! se os passos anteriores deram certo, nosso projeto está no ar!
  <br>
  Confira tudo o que o Instituto Xavier tem a oferecer e aproveite. Certifique-se de ter o arquivo .env preenchido e as ferramentas instaladas na sua máquina como <i>make</i>
</b></p>

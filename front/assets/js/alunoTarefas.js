const STORAGE_KEY = "tarefas_aluno";

const TarefaService = {
  async listar() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  }, 

  async criar(tarefa) {
    const tarefas = await this.listar();
    tarefa.id = Date.now();
    tarefa.criadoEm = new Date().toISOString();
    tarefas.push(tarefa);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tarefas));
    return tarefa;
  },

  async atualizar(id, dadosAtualizados) {
    const tarefas = await this.listar();
    const index = tarefas.findIndex((t) => t.id === id);
    if (index === -1) throw new Error("Tarefa não encontrada");
    tarefas[index] = { ...tarefas[index], ...dadosAtualizados };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tarefas));
    return tarefas[index];
  },
  async excluir(id) {
    let tarefas = await this.listar();
    tarefas = tarefas.filter((t) => t.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tarefas));
  },
};

let todasAsTarefas = [];
let filtroAtual = "todas";
let tarefaEditando = null;
let tarefaExcluindo = null;

document.addEventListener("DOMContentLoaded", async () => {
  await carregarTarefas();
  configurarEventos();
});

async function carregarTarefas() {
  todasAsTarefas = await TarefaService.listar();
  atualizarStats();
  atualizarContadoresFiltros();
  renderizarTarefas();
}

function configurarEventos() {
  
  document
    .getElementById("btn-adicionar-tarefa")
    .addEventListener("click", () => abrirModal());

  
  document.querySelectorAll(".filtro-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document
        .querySelectorAll(".filtro-btn")
        .forEach((b) => b.classList.remove("ativo"));
      btn.classList.add("ativo");
      filtroAtual = btn.dataset.filtro;
      renderizarTarefas();
    });
  });

  
  const searchInput = document.querySelector(".aluno-search input");
  if (searchInput) {
    searchInput.addEventListener("input", () => renderizarTarefas());
  }

  
  const modalForm = document.getElementById("modal-tarefa");
  document
    .getElementById("form-tarefa")
    .addEventListener("submit", handleSubmit);

  document.querySelectorAll("#modal-tarefa .fechar-modal").forEach((btn) => {
    btn.addEventListener("click", () => fecharModal(modalForm));
  });
  document
    .getElementById("btn-cancelar-tarefa")
    .addEventListener("click", () => fecharModal(modalForm));

  
  const modalExcluir = document.getElementById("modal-excluir-tarefa");
  document
    .querySelectorAll("#modal-excluir-tarefa .fechar-modal")
    .forEach((btn) => {
      btn.addEventListener("click", () => fecharModal(modalExcluir));
    });
  document
    .getElementById("btn-cancelar-excluir")
    .addEventListener("click", () => fecharModal(modalExcluir));
  document
    .getElementById("btn-confirmar-excluir")
    .addEventListener("click", handleExcluir);

  
  [modalForm, modalExcluir].forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) fecharModal(modal);
    });
  });
}

function getTarefasFiltradas() {
  const searchInput = document.querySelector(".aluno-search input");
  const termo = searchInput ? searchInput.value.toLowerCase() : "";

  return todasAsTarefas.filter((tarefa) => {
    
    if (filtroAtual !== "todas" && tarefa.status !== filtroAtual) return false;

    
    if (termo) {
      return (
        tarefa.titulo.toLowerCase().includes(termo) ||
        tarefa.materia.toLowerCase().includes(termo) ||
        tarefa.descricao.toLowerCase().includes(termo)
      );
    }

    return true;
  });
}

function renderizarTarefas() {
  const grid = document.getElementById("tarefas-grid");
  const vazio = document.getElementById("tarefas-vazio");
  const tarefasFiltradas = getTarefasFiltradas();

  if (tarefasFiltradas.length === 0) {
    grid.style.display = "none";
    vazio.style.display = "flex";
    return;
  }

  vazio.style.display = "none";
  grid.style.display = "grid";
  grid.innerHTML = "";
  
  const ordenadas = [...tarefasFiltradas].sort((a, b) => {
    const ordemStatus = { pendente: 0, "em-andamento": 1, concluida: 2 };
    const statusDiff = ordemStatus[a.status] - ordemStatus[b.status];
    if (statusDiff !== 0) return statusDiff;
    return new Date(a.dataEntrega) - new Date(b.dataEntrega);
  });

  ordenadas.forEach((tarefa, index) => {
    const card = criarCardTarefa(tarefa);
    card.style.animationDelay = `${index * 0.05}s`;
    grid.appendChild(card);
  });
}

function criarCardTarefa(tarefa) {
  const card = document.createElement("div");
  card.className = `tarefa-card${tarefa.status === "concluida" ? " concluida-card" : ""}`;

  const statusClass =
    tarefa.status === "pendente"
      ? "status-pendente"
      : tarefa.status === "em-andamento"
        ? "status-em-andamento"
        : "status-concluida";

  const prioridadeClass =
    tarefa.prioridade === "alta"
      ? "prioridade-alta"
      : tarefa.prioridade === "media"
        ? "prioridade-media"
        : "prioridade-baixa";

  const prioridadeLabel =
    tarefa.prioridade === "alta"
      ? "Alta"
      : tarefa.prioridade === "media"
        ? "Média"
        : "Baixa";

  const dataEntrega = formatarData(tarefa.dataEntrega);
  const atrasada = estaAtrasada(tarefa);

  card.innerHTML = `
    <div class="tarefa-status-bar ${statusClass}"></div>
    <div class="tarefa-check">
      <div class="tarefa-checkbox ${tarefa.status === "concluida" ? "checked" : ""}" 
           data-id="${tarefa.id}" title="Marcar como concluída"></div>
      <div style="flex: 1;">
        <div class="tarefa-card-header">
          <h3>${tarefa.titulo}</h3>
          <span class="tarefa-card-materia">${tarefa.materia}</span>
        </div>
        <p class="tarefa-card-descricao">${tarefa.descricao || "Sem descrição"}</p>
      </div>
    </div>
    <div class="tarefa-card-footer">
      <div class="tarefa-card-data ${atrasada ? "atrasada" : ""}">
        <i class="fa-regular fa-calendar"></i>
        ${dataEntrega}
        ${atrasada ? '<i class="fa-solid fa-triangle-exclamation"></i>' : ""}
      </div>
      <div style="display: flex; align-items: center; gap: 1rem;">
        <span class="prioridade-badge ${prioridadeClass}">${prioridadeLabel}</span>
        <div class="tarefa-card-acoes">
          <button class="btn-editar-tarefa" data-id="${tarefa.id}" title="Editar">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="btn-excluir-tarefa" data-id="${tarefa.id}" title="Excluir">
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>
    </div>
  `;

  
  card
    .querySelector(".tarefa-checkbox")
    .addEventListener("click", async (e) => {
      e.stopPropagation();
      const novoStatus =
        tarefa.status === "concluida" ? "pendente" : "concluida";
      await TarefaService.atualizar(tarefa.id, { status: novoStatus });
      await carregarTarefas();
    });

  
  card.querySelector(".btn-editar-tarefa").addEventListener("click", (e) => {
    e.stopPropagation();
    abrirModal(tarefa);
  });

  
  card.querySelector(".btn-excluir-tarefa").addEventListener("click", (e) => {
    e.stopPropagation();
    abrirModalExcluir(tarefa);
  });

  return card;
}

function atualizarStats() {
  const pendentes = todasAsTarefas.filter(
    (t) => t.status === "pendente",
  ).length;
  const andamento = todasAsTarefas.filter(
    (t) => t.status === "em-andamento",
  ).length;
  const concluidas = todasAsTarefas.filter(
    (t) => t.status === "concluida",
  ).length;

  document.getElementById("stat-pendentes").textContent = pendentes;
  document.getElementById("stat-andamento").textContent = andamento;
  document.getElementById("stat-concluidas").textContent = concluidas;
  document.getElementById("stat-total").textContent = todasAsTarefas.length;
}

function atualizarContadoresFiltros() {
  const contadores = {
    todas: todasAsTarefas.length,
    pendente: todasAsTarefas.filter((t) => t.status === "pendente").length,
    "em-andamento": todasAsTarefas.filter((t) => t.status === "em-andamento")
      .length,
    concluida: todasAsTarefas.filter((t) => t.status === "concluida").length,
  };

  document.querySelectorAll(".filtro-btn").forEach((btn) => {
    const filtro = btn.dataset.filtro;
    const contador = btn.querySelector(".filtro-contador");
    if (contador) {
      contador.textContent = contadores[filtro] || 0;
    }
  });
}

function abrirModal(tarefa = null) {
  const modal = document.getElementById("modal-tarefa");
  const titulo = document.getElementById("modal-titulo");
  const form = document.getElementById("form-tarefa");

  tarefaEditando = tarefa;

  if (tarefa) {
    titulo.textContent = "Editar Tarefa";
    document.getElementById("tarefa-titulo").value = tarefa.titulo;
    document.getElementById("tarefa-materia").value = tarefa.materia;
    document.getElementById("tarefa-descricao").value = tarefa.descricao || "";
    document.getElementById("tarefa-data").value = tarefa.dataEntrega || "";
    document.getElementById("tarefa-prioridade").value = tarefa.prioridade;
    document.getElementById("tarefa-status").value = tarefa.status;
  } else {
    titulo.textContent = "Nova Tarefa";
    form.reset();
    document.getElementById("tarefa-status").value = "pendente";
    document.getElementById("tarefa-prioridade").value = "media";
  }

  modal.style.display = "flex";
}

function fecharModal(modal) {
  modal.style.display = "none";
  tarefaEditando = null;
  tarefaExcluindo = null;
}

async function handleSubmit(e) {
  e.preventDefault();

  const dados = {
    titulo: document.getElementById("tarefa-titulo").value.trim(),
    materia: document.getElementById("tarefa-materia").value.trim(),
    descricao: document.getElementById("tarefa-descricao").value.trim(),
    dataEntrega: document.getElementById("tarefa-data").value,
    prioridade: document.getElementById("tarefa-prioridade").value,
    status: document.getElementById("tarefa-status").value,
  };

  if (!dados.titulo || !dados.materia) return;

  if (tarefaEditando) {
    await TarefaService.atualizar(tarefaEditando.id, dados);
  } else {
    await TarefaService.criar(dados);
  }

  fecharModal(document.getElementById("modal-tarefa"));
  await carregarTarefas();
}

function abrirModalExcluir(tarefa) {
  tarefaExcluindo = tarefa;
  const modal = document.getElementById("modal-excluir-tarefa");
  document.getElementById("excluir-tarefa-nome").textContent = tarefa.titulo;
  modal.style.display = "flex";
}

async function handleExcluir() {
  if (!tarefaExcluindo) return;
  await TarefaService.excluir(tarefaExcluindo.id);
  fecharModal(document.getElementById("modal-excluir-tarefa"));
  await carregarTarefas();
}

function formatarData(dataStr) {
  if (!dataStr) return "Sem data";
  const data = new Date(dataStr + "T00:00:00");
  return data.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

function estaAtrasada(tarefa) {
  if (!tarefa.dataEntrega || tarefa.status === "concluida") return false;
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  const dataEntrega = new Date(tarefa.dataEntrega + "T00:00:00");
  return dataEntrega < hoje;
}

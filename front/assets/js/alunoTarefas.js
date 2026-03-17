import { api } from "./utils.js";

const idUsuario = localStorage.getItem("userId");

const mapeamentoStatus = {
  pendente: "Pendente",
  "em-andamento": "Em andamento",
  concluida: "Concluída",
};

const mapeamentoStatusReverso = {
  Pendente: "pendente",
  "Em andamento": "em-andamento",
  Concluída: "concluida",
  Cancelada: "pendente",
};

const mapeamentoPrioridade = {
  baixa: "Baixa",
  media: "Média",
  alta: "Alta",
};

const mapeamentoPrioridadeReverso = {
  Baixa: "baixa",
  Média: "media",
  Alta: "alta",
};

const ServicoTarefa = {
  async listar() {
    return await api(`tarefa/mutante/${idUsuario}`, "GET");
  },

  async criar(tarefa) {
    const dados = {
      titulo: tarefa.titulo,
      descricao: tarefa.descricao,
      status: mapeamentoStatus[tarefa.status] || "Pendente",
      prioridade: mapeamentoPrioridade[tarefa.prioridade] || "Média",
      data_limite: tarefa.dataEntrega
        ? new Date(tarefa.dataEntrega).toISOString()
        : null,
      mutante_id: parseInt(idUsuario),
    };
    return await api("tarefa/create", "POST", dados);
  },

  async atualizar(id, novosDados) {
    const dados = {};
    if (novosDados.titulo) dados.titulo = novosDados.titulo;
    if (novosDados.descricao !== undefined)
      dados.descricao = novosDados.descricao;
    if (novosDados.status)
      dados.status = mapeamentoStatus[novosDados.status] || "Pendente";
    if (novosDados.prioridade)
      dados.prioridade = mapeamentoPrioridade[novosDados.prioridade] || "Média";
    if (novosDados.dataEntrega)
      dados.data_limite = new Date(novosDados.dataEntrega).toISOString();

    return await api(`tarefa/${id}`, "PATCH", dados);
  },

  async excluir(id) {
    return await api(`tarefa/${id}`, "DELETE");
  },

  async concluir(id) {
    return await api(`tarefa/${id}/concluir`, "PATCH");
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
  try {
    const tarefasApi = await ServicoTarefa.listar();
    todasAsTarefas = tarefasApi.map((t) => ({
      id: t.id,
      titulo: t.titulo,
      descricao: t.descricao,
      status: mapeamentoStatusReverso[t.status] || "pendente",
      prioridade: mapeamentoPrioridadeReverso[t.prioridade] || "media",
      dataEntrega: t.data_limite ? t.data_limite.split("T")[0] : null,
    }));

    atualizarEstatisticas();
    atualizarContadoresFiltros();
    renderizarTarefas();
  } catch (erro) {
    console.error("Erro ao carregar tarefas:", erro);
    todasAsTarefas = [];
    atualizarEstatisticas();
    atualizarContadoresFiltros();
    renderizarTarefas();
  }
}

function configurarEventos() {
  document
    .getElementById("btn-adicionar-tarefa")
    .addEventListener("click", () => abrirModal());

  document.querySelectorAll(".filtro-btn").forEach((botao) => {
    botao.addEventListener("click", () => {
      document
        .querySelectorAll(".filtro-btn")
        .forEach((b) => b.classList.remove("ativo"));
      botao.classList.add("ativo");
      filtroAtual = botao.dataset.filtro;
      renderizarTarefas();
    });
  });

  const campoBusca = document.querySelector(".aluno-search input");
  if (campoBusca) {
    campoBusca.addEventListener("input", () => renderizarTarefas());
  }

  const modalFormulario = document.getElementById("modal-tarefa");
  document
    .getElementById("form-tarefa")
    .addEventListener("submit", processarSubmissao);

  document.querySelectorAll("#modal-tarefa .fechar-modal").forEach((btn) => {
    btn.addEventListener("click", () => fecharModal(modalFormulario));
  });
  document
    .getElementById("btn-cancelar-tarefa")
    .addEventListener("click", () => fecharModal(modalFormulario));

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
    .addEventListener("click", processarExclusao);

  [modalFormulario, modalExcluir].forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) fecharModal(modal);
    });
  });
}

function obterTarefasFiltradas() {
  const campoBusca = document.querySelector(".aluno-search input");
  const termo = campoBusca ? campoBusca.value.toLowerCase() : "";

  return todasAsTarefas.filter((tarefa) => {
    if (filtroAtual !== "todas" && tarefa.status !== filtroAtual) return false;
    if (termo) {
      return (
        tarefa.titulo.toLowerCase().includes(termo) ||
        (tarefa.descricao && tarefa.descricao.toLowerCase().includes(termo))
      );
    }
    return true;
  });
}

function renderizarTarefas() {
  const grade = document.getElementById("tarefas-grid");
  const vazio = document.getElementById("tarefas-vazio");
  const tarefasFiltradas = obterTarefasFiltradas();

  if (tarefasFiltradas.length === 0) {
    grade.style.display = "none";
    vazio.style.display = "flex";
    return;
  }

  vazio.style.display = "none";
  grade.style.display = "grid";
  grade.innerHTML = "";

  const ordenadas = [...tarefasFiltradas].sort((a, b) => {
    const ordemStatus = { pendente: 0, "em-andamento": 1, concluida: 2 };
    const diferencaStatus = ordemStatus[a.status] - ordemStatus[b.status];
    if (diferencaStatus !== 0) return diferencaStatus;
    if (!a.dataEntrega) return 1;
    if (!b.dataEntrega) return -1;
    return new Date(a.dataEntrega) - new Date(b.dataEntrega);
  });

  ordenadas.forEach((tarefa, indice) => {
    const card = criarCardTarefa(tarefa);
    card.style.animationDelay = `${indice * 0.05}s`;
    grade.appendChild(card);
  });
}

function criarCardTarefa(tarefa) {
  const card = document.createElement("div");
  card.className = `tarefa-card${tarefa.status === "concluida" ? " concluida-card" : ""}`;

  const classeStatus =
    tarefa.status === "pendente"
      ? "status-pendente"
      : tarefa.status === "em-andamento"
        ? "status-em-andamento"
        : "status-concluida";

  const classePrioridade =
    tarefa.prioridade === "alta"
      ? "prioridade-alta"
      : tarefa.prioridade === "media"
        ? "prioridade-media"
        : "prioridade-baixa";

  const rotuloPrioridade =
    tarefa.prioridade === "alta"
      ? "Alta"
      : tarefa.prioridade === "media"
        ? "Média"
        : "Baixa";

  const dataEntrega = formatarData(tarefa.dataEntrega);
  const atrasada = estaAtrasada(tarefa);

  card.innerHTML = `
    <div class="tarefa-status-bar ${classeStatus}"></div>
    <div class="tarefa-check">
      <div class="tarefa-checkbox ${tarefa.status === "concluida" ? "checked" : ""}" 
           data-id="${tarefa.id}" title="Marcar como concluída"></div>
      <div style="flex: 1;">
        <div class="tarefa-card-header">
          <h3>${tarefa.titulo}</h3>
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
        <span class="prioridade-badge ${classePrioridade}">${rotuloPrioridade}</span>
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
      try {
        if (tarefa.status !== "concluida") {
          await ServicoTarefa.concluir(tarefa.id);
        } else {
          await ServicoTarefa.atualizar(tarefa.id, { status: "pendente" });
        }
        await carregarTarefas();
      } catch (erro) {
        console.error(erro);
      }
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

function atualizarEstatisticas() {
  const pendentes = todasAsTarefas.filter(
    (t) => t.status === "pendente",
  ).length;
  const andamento = todasAsTarefas.filter(
    (t) => t.status === "em-andamento",
  ).length;
  const concluidas = todasAsTarefas.filter(
    (t) => t.status === "concluida",
  ).length;

  const sp = document.getElementById("stat-pendentes");
  const sa = document.getElementById("stat-andamento");
  const sc = document.getElementById("stat-concluidas");
  const st = document.getElementById("stat-total");

  if (sp) sp.textContent = pendentes;
  if (sa) sa.textContent = andamento;
  if (sc) sc.textContent = concluidas;
  if (st) st.textContent = todasAsTarefas.length;
}

function atualizarContadoresFiltros() {
  const contadores = {
    todas: todasAsTarefas.length,
    pendente: todasAsTarefas.filter((t) => t.status === "pendente").length,
    "em-andamento": todasAsTarefas.filter((t) => t.status === "em-andamento")
      .length,
    concluida: todasAsTarefas.filter((t) => t.status === "concluida").length,
  };

  document.querySelectorAll(".filtro-btn").forEach((botao) => {
    const filtro = botao.dataset.filtro;
    const contador = botao.querySelector(".filtro-contador");
    if (contador) {
      contador.textContent = contadores[filtro] || 0;
    }
  });
}

function abrirModal(tarefa = null) {
  const modal = document.getElementById("modal-tarefa");
  const titulo = document.getElementById("modal-titulo");
  const formulario = document.getElementById("form-tarefa");

  tarefaEditando = tarefa;

  if (tarefa) {
    titulo.textContent = "Editar Tarefa";
    document.getElementById("tarefa-titulo").value = tarefa.titulo;
    document.getElementById("tarefa-descricao").value = tarefa.descricao || "";
    document.getElementById("tarefa-data").value = tarefa.dataEntrega || "";
    document.getElementById("tarefa-prioridade").value = tarefa.prioridade;
    document.getElementById("tarefa-status").value = tarefa.status;
  } else {
    titulo.textContent = "Nova Tarefa";
    formulario.reset();
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

async function processarSubmissao(e) {
  e.preventDefault();

  const dadosEntrada = {
    titulo: document.getElementById("tarefa-titulo").value.trim(),
    descricao: document.getElementById("tarefa-descricao").value.trim(),
    dataEntrega: document.getElementById("tarefa-data").value,
    prioridade: document.getElementById("tarefa-prioridade").value,
    status: document.getElementById("tarefa-status").value,
  };

  if (!dadosEntrada.titulo) return;

  try {
    if (tarefaEditando) {
      await ServicoTarefa.atualizar(tarefaEditando.id, dadosEntrada);
    } else {
      await ServicoTarefa.criar(dadosEntrada);
    }

    fecharModal(document.getElementById("modal-tarefa"));
    await carregarTarefas();
  } catch (erro) {
    console.error("Erro ao salvar tarefa:", erro);
  }
}

function abrirModalExcluir(tarefa) {
  tarefaExcluindo = tarefa;
  const modal = document.getElementById("modal-excluir-tarefa");
  document.getElementById("excluir-tarefa-nome").textContent = tarefa.titulo;
  modal.style.display = "flex";
}

async function processarExclusao() {
  if (!tarefaExcluindo) return;
  try {
    await ServicoTarefa.excluir(tarefaExcluindo.id);
    fecharModal(document.getElementById("modal-excluir-tarefa"));
    await carregarTarefas();
  } catch (erro) {
    console.error("Erro ao excluir tarefa:", erro);
  }
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

import { api } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal-recuperacao");
  const botaoAbrir = document.getElementById("abrir-modal-recuperacao");
  const botaoFechar = document.getElementById("fechar-modal-recuperacao");
  const passo1 = document.getElementById("passo-recuperacao-1");
  const passo2 = document.getElementById("passo-recuperacao-2");
  const mensagem = document.getElementById("mensagem-recuperacao");

  const botaoSolicitar = document.getElementById("btn-solicitar-codigo");
  const botaoRedefinir = document.getElementById("btn-redefinir-senha");

  botaoAbrir?.addEventListener("click", (e) => {
    e.preventDefault();
    modal.style.display = "flex";
    limparModal();
  });

  botaoFechar?.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });

  function limparModal() {
    passo1.style.display = "block";
    passo2.style.display = "none";
    mensagem.style.display = "none";
    mensagem.className = "";
    document.getElementById("email-recuperacao").value = "";
    document.getElementById("codigo-recuperacao").value = "";
    document.getElementById("nova-senha-recuperacao").value = "";
    document.getElementById("confirmar-senha-recuperacao").value = "";
  }

  function exibirMensagem(texto, erro = true) {
    mensagem.textContent = texto;
    mensagem.style.display = "block";
    mensagem.className = erro ? "error" : "success";
  }

  botaoSolicitar?.addEventListener("click", async () => {
    const email = document.getElementById("email-recuperacao").value;

    if (!email) {
      return exibirMensagem("Por favor, insira seu email ou usuário.");
    }

    try {
      botaoSolicitar.disabled = true;
      botaoSolicitar.textContent = "Solicitando...";

      await api("auth/recuperar-senha", "POST", { email: email });

      exibirMensagem(
        "Código enviado! Verifique o console do servidor de API para copiá-lo.",
        false,
      );

      setTimeout(() => {
        passo1.style.display = "none";
        passo2.style.display = "block";
        mensagem.style.display = "none";
      }, 3000);
    } catch (error) {
      console.error(error);
      exibirMensagem("Erro ao solicitar recuperação. Verifique os dados.");
    } finally {
      botaoSolicitar.disabled = false;
      botaoSolicitar.textContent = "Solicitar Código";
    }
  });

  botaoRedefinir?.addEventListener("click", async () => {
    const token = document.getElementById("codigo-recuperacao").value;
    const novaSenha = document.getElementById("nova-senha-recuperacao").value;
    const confirmarSenha = document.getElementById(
      "confirmar-senha-recuperacao",
    ).value;

    if (!token || !novaSenha || !confirmarSenha) {
      return exibirMensagem("O código é obrigatório.");
    }

    if (novaSenha !== confirmarSenha) {
      return exibirMensagem("As senhas não conferem.");
    }

    if (novaSenha.length < 6) {
      return exibirSenha("A senha deve ter no mínimo 6 caracteres.");
    }

    try {
      botaoRedefinir.disabled = true;
      botaoRedefinir.textContent = "Processando...";

      await api("auth/redefinir-senha", "POST", {
        token: token,
        nova_senha: novaSenha,
        confirmar_senha: confirmarSenha,
      });

      exibirMensagem(
        "Senha redefinida com sucesso! Você já pode fazer login.",
        false,
      );

      setTimeout(() => {
        modal.style.display = "none";
      }, 3000);
    } catch (error) {
      console.error(error);
      exibirMensagem(
        "Erro ao redefinir senha. O código pode estar expirado ou inválido.",
      );
    } finally {
      botaoRedefinir.disabled = false;
      botaoRedefinir.textContent = "Redefinir Senha";
    }
  });
});

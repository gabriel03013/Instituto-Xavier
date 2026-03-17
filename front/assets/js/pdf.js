const CORES = {
  primaria: [28, 78, 128],
  secundaria: [245, 212, 50],
  texto: [33, 37, 41],
  textoSuave: [108, 117, 125],
  sucesso: [40, 167, 69],
  erro: [220, 53, 69],
  borda: [222, 226, 230],
  fundoTabela: [248, 249, 250],
  branco: [255, 255, 255],
};

function aplicarFonte(doc, estilo = "normal", tamanho = 10) {
  try {
    doc.setFont("IBS", estilo);
  } catch (e) {
    console.debug("Fonte IBS não encontrada, usando Helvetica.");
    doc.setFont("helvetica", estilo);
  }
  doc.setFontSize(tamanho);
}

function carregarImagem(url) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = () => {
      try {
        if (url.toLowerCase().endsWith(".svg")) {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");
          canvas.width = img.width || 200;
          canvas.height = img.height || 200;
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          resolve(canvas.toDataURL("image/png"));
        } else {
          resolve(img);
        }
      } catch (err) {
        console.error("Erro ao processar imagem no canvas:", err);
        resolve(null);
      }
    };
    img.onerror = (e) => {
      console.error("Erro ao carregar imagem:", url, e);
      resolve(null);
    };
    img.src = url;
  });
}

async function desenharCabecalho(doc, pageWidth) {
  try {
    console.log("Desenhando cabeçalho...");
    const logoUrl = "../../assets/images/Group 14.svg";
    const logo = await carregarImagem(logoUrl);
    if (logo) {
      console.log("Logo carregada, adicionando ao PDF...");
      doc.addImage(logo, "PNG", 15, 12, 22, 20);
    }
  } catch (e) {
    console.warn("Erro ao carregar logo, continuando sem ela:", e);
  }

  aplicarFonte(doc, "bold", 16);
  doc.setTextColor(...CORES.primaria);
  doc.text("INSTITUTO XAVIER", 42, 22);

  aplicarFonte(doc, "normal", 8);
  doc.setTextColor(...CORES.textoSuave);
  doc.text("Xavier Institute for Gifted Youngsters", 42, 27);

  doc.setDrawColor(...CORES.borda);
  doc.setLineWidth(0.1);
  doc.line(15, 38, pageWidth - 15, 38);
}

function desenharInformacoes(doc, dados, pageWidth) {
  const y = 48;

  aplicarFonte(doc, "bold", 11);
  doc.setTextColor(...CORES.texto);
  doc.text("BOLETIM DE DESEMPENHO ACADÊMICO", 15, y);

  aplicarFonte(doc, "normal", 9);
  doc.setTextColor(...CORES.textoSuave);
  doc.text(`Estudante:`, 15, y + 8);
  doc.setTextColor(...CORES.texto);
  doc.text(`${dados.nome.toUpperCase()}`, 35, y + 8);

  doc.setTextColor(...CORES.textoSuave);
  doc.text(`Turma:`, 15, y + 13);
  doc.setTextColor(...CORES.texto);
  doc.text(`${dados.turma}`, 35, y + 13);

  const data = new Date().toLocaleDateString("pt-BR");
  doc.setTextColor(...CORES.textoSuave);
  doc.text(`Emissão: ${data}`, pageWidth - 15, y + 13, { align: "right" });

  return y + 25;
}

function desenharTabela(doc, materias, yInicial, pageWidth) {
  const colunas = [
    { header: "DISCIPLINA", x: 15, w: 70 },
    { header: "PROFESSOR", x: 85, w: 45 },
    { header: "N1", x: 130, w: 15, align: "center" },
    { header: "N2", x: 145, w: 15, align: "center" },
    { header: "MÉDIA", x: 160, w: 15, align: "center" },
    { header: "STATUS", x: 175, w: 20, align: "right" },
  ];

  let y = yInicial;

  doc.setFillColor(...CORES.fundoTabela);
  doc.rect(15, y, pageWidth - 30, 8, "F");

  aplicarFonte(doc, "bold", 7);
  doc.setTextColor(...CORES.textoSuave);

  colunas.forEach((col) => {
    const textX =
      col.align === "center"
        ? col.x + col.w / 2
        : col.align === "right"
          ? col.x + col.w
          : col.x;
    doc.text(col.header, textX, y + 5.5, { align: col.align || "left" });
  });

  y += 8;
  aplicarFonte(doc, "normal", 8);
  doc.setTextColor(...CORES.texto);

  let somaMedias = 0;
  let materiasCont = 0;

  materias.forEach((materia, i) => {
    if (y > 260) {
      doc.addPage();
      y = 20;
    }

    const n1 = Number(materia.nota1) || 0;
    const n2 = Number(materia.nota2) || 0;
    const media = Number(materia.media_final) || 0;
    somaMedias += media;
    materiasCont++;

    y += 8;
    const nomeMateria =
      materia.nome.length > 35
        ? materia.nome.substring(0, 32) + "..."
        : materia.nome;
    doc.text(nomeMateria, 15, y);

    const nomeProf =
      materia.professor.split(" ")[0] +
      " " +
      (materia.professor.split(" ")[1] || "");
    doc.text(nomeProf, 85, y);

    doc.text(n1.toFixed(1), 137.5, y, { align: "center" });
    doc.text(n2.toFixed(1), 152.5, y, { align: "center" });

    doc.setTextColor(...(media < 6 ? CORES.erro : CORES.primaria));
    doc.text(media.toFixed(1), 167.5, y, { align: "center" });

    doc.setTextColor(
      ...(materia.status === "Aprovado" ? CORES.sucesso : CORES.erro),
    );
    doc.text(materia.status.toUpperCase(), pageWidth - 15, y, {
      align: "right",
    });

    doc.setTextColor(...CORES.texto);
    doc.setDrawColor(...CORES.borda);
    doc.line(15, y + 2, pageWidth - 15, y + 2);
    y += 2;
  });

  y += 15;
  if (y > 270) {
    doc.addPage();
    y = 20;
  }

  const mediaGeral =
    materiasCont > 0 ? (somaMedias / materiasCont).toFixed(1) : "0.0";

  doc.setFillColor(...CORES.fundoTabela);
  doc.rect(pageWidth - 75, y, 60, 15, "F");

  aplicarFonte(doc, "normal", 8);
  doc.text("MÉDIA GERAL DO PERÍODO:", pageWidth - 70, y + 6);
  aplicarFonte(doc, "bold", 12);
  doc.setTextColor(...(Number(mediaGeral) < 6 ? CORES.erro : CORES.primaria));
  doc.text(mediaGeral, pageWidth - 20, y + 10, { align: "right" });

  return y + 15;
}

function desenharRodape(doc, p, pageWidth, pageHeight) {
  aplicarFonte(doc, "normal", 7);
  doc.setTextColor(...CORES.textoSuave);
  const dataExtenso = new Date().toLocaleDateString("pt-BR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  doc.text(
    `Documento eletrônico gerado em ${dataExtenso}`,
    15,
    pageHeight - 10,
  );
  doc.text(
    `Instituto Xavier de Educação Especial - Página ${p}`,
    pageWidth - 15,
    pageHeight - 10,
    { align: "right" },
  );
}

export async function gerarBoletimPDF(dadosAluno, materias) {
  let jsPDF;
  if (window.jspdf && window.jspdf.jsPDF) {
    jsPDF = window.jspdf.jsPDF;
  } else if (window.jsPDF) {
    jsPDF = window.jsPDF;
  } else {
    throw new Error("Biblioteca jsPDF não carregada corretamente.");
  }

  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

  console.log("Página gerada, adicionando conteúdo...");
  await desenharCabecalho(doc, pageWidth);

  console.log("Desenhando informações do aluno...");
  let y = desenharInformacoes(doc, dadosAluno, pageWidth);

  console.log("Desenhando tabela de notas...");
  y = desenharTabela(doc, materias, y, pageWidth);

  const totalPages = doc.internal.getNumberOfPages();
  console.log(`Finalizando ${totalPages} páginas...`);
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    desenharRodape(doc, i, pageWidth, pageHeight);
  }

  return doc;
}

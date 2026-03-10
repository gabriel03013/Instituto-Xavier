export function gerarBoletimPDF(dadosAluno, materias) {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  doc.setFont("helvetica", "bold");
  doc.setFontSize(18);
  doc.text("BOLETIM ESCOLAR", 105, 20, { align: "center" });

  doc.setFont("helvetica", "normal");
  doc.setFontSize(12);
  doc.text(`Aluno: ${dadosAluno.nome}`, 14, 35);
  doc.text(`Turma: ${dadosAluno.turma}`, 14, 42);

  let y = 55;

  doc.setFont("helvetica", "bold");
  doc.text("Professor", 14, y);
  doc.text("Matéria", 45, y);
  doc.text("Nota 1", 90, y);
  doc.text("Nota 2", 110, y);
  doc.text("Média Final", 130, y);
  doc.text("Situação", 165, y);

  y += 5;
  doc.line(14, y, 195, y);

  doc.setFont("helvetica", "normal");

  materias.forEach((materia) => {
    y += 10;

    if (y > 280) {
      doc.addPage();
      y = 20;
    }

    doc.text(String(materia.professor), 14, y);
    doc.text(String(materia.nome), 45, y);
    doc.text(String(materia.nota1), 95, y);
    doc.text(String(materia.nota2), 115, y);
    doc.text(String(materia.media_final), 145, y);

    if (materia.status === "Aprovado") {
      doc.setTextColor(0, 128, 0);
    } else {
      doc.setTextColor(255, 0, 0);
    }

    doc.text(String(materia.status), 165, y);
    doc.setTextColor(0, 0, 0);
  });

  return doc;
}

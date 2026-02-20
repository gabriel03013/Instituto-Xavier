DROP VIEW IF EXISTS Materias_Professores;
DROP VIEW IF EXISTS Mutantes_Poderes;
DROP VIEW IF EXISTS Mutantes_Turmas;
DROP VIEW IF EXISTS Visao_Geral;

CREATE VIEW Materias_Professores AS (
	SELECT 
		p.nome AS professor,
		m.nome AS materia
	FROM professores p
	JOIN materias m
		ON m.professor_id = p.id
);

CREATE VIEW Visao_Geral AS (
	SELECT 
		a.nome AS nome_mutante,
		CONCAT(t.serie, 'º', t.turma) AS turma,
		a.matricula,
		p.nome AS professor,
		mt.nome AS materia,
		o.observacao AS obs,
		o.data AS data_obs,
		mm.nota1,
		mm.nota2
	FROM mutantes a
	JOIN mutantesmaterias mm
		ON mm.mutante_id = a.id
	JOIN materias mt 
		ON mm.materia_id = mt.id
	JOIN observacoes o
		ON o.mutantesmaterias_id = mm.id
	JOIN professores p 
		ON mt.professor_id = p.id
	JOIN turmas t
		ON a.turma_id = t.id
);

CREATE VIEW Mutantes_Poderes AS (
	SELECT 
		m.id AS id_aluno,
		m.nome,
		p.nome AS poder
	FROM mutantes m 
	JOIN poderes p 
		ON m.poder_id = p.id
);

CREATE VIEW Mutantes_Turmas AS (
	SELECT 
		m.id AS id_mutante,
		m.nome,
		t.serie,
		t.turma,
		CONCAT(t.serie,'º',t.turma) AS turma_concat
	FROM mutantes m 
	JOIN turmas t
		ON m.turma_id = t.id
);

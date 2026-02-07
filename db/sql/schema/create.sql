DROP TABLE IF EXISTS MutantesMaterias;
DROP TABLE IF EXISTS Mutantes;
DROP TABLE IF EXISTS Materias;
DROP TABLE IF EXISTS Professores;
DROP TABLE IF EXISTS Poderes;

CREATE TABLE Professores (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	usuario VARCHAR(100) NOT NULL,
	senha VARCHAR(200) NOT NULL
);

CREATE TABLE Poderes (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL
);

CREATE TABLE Materias (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	professor_id INTEGER NOT NULL,
	CONSTRAINT fk_professor FOREIGN KEY (professor_id)
		REFERENCES Professores(id)
);

CREATE TABLE Mutantes (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	matricula VARCHAR(50) NOT NULL,
	email VARCHAR(150) NOT NULL,
	senha VARCHAR(200) NOT NULL,
	poder_id INTEGER NOT NULL,
	CONSTRAINT fk_poder FOREIGN KEY (poder_id)
		REFERENCES Poderes(id)
);

CREATE TABLE MutantesMaterias (
	id SERIAL PRIMARY KEY,
	nota1 NUMERIC(4,2),
	nota2 NUMERIC(4,2),
	observacao TEXT,
	materia_id INTEGER NOT NULL,
	mutante_id INTEGER NOT NULL,
	CONSTRAINT fk_materia FOREIGN KEY (materia_id)
		REFERENCES Materias(id),
	CONSTRAINT fk_aluno FOREIGN KEY (mutante_id)
		REFERENCES Mutantes(id)
);
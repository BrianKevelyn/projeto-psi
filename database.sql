CREATE TABLE IF NOT EXISTS tb_usuarios (
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_nome VARCHAR(100) NOT NULL,
    usu_matricula VARCHAR(50) UNIQUE NOT NULL,
    usu_telefone VARCHAR(20),
    usu_email VARCHAR(100) UNIQUE,
    usu_tipo VARCHAR(50),
    usu_senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_livros (
    liv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    liv_titulo VARCHAR(200) NOT NULL,
    liv_descricao VARCHAR(450),
    liv_editora VARCHAR(100),
    liv_ano INTEGER,
    liv_autor VARCHAR(100),
    liv_genero VARCHAR(50),
    liv_quantidade INTEGER,
    liv_preco REAL
);

CREATE TABLE IF NOT EXISTS tb_reservas (
    res_id INTEGER PRIMARY KEY AUTOINCREMENT,
    res_usu_id INTEGER NOT NULL,
    res_liv_id INTEGER NOT NULL,
    res_data_reserva DATE,
    status VARCHAR(50),
    FOREIGN KEY (res_usu_id) REFERENCES tb_usuarios(usu_id),
    FOREIGN KEY (res_liv_id) REFERENCES tb_livros(liv_id)
);

CREATE TABLE IF NOT EXISTS tb_emprestimos (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_usu_id INTEGER NOT NULL,
    emp_liv_id INTEGER NOT NULL,
    emp_data_emprestimo DATE,
    emp_data_a_devolver DATE,
    emp_data_devolucao DATE,
    status VARCHAR(50),
    FOREIGN KEY (emp_usu_id) REFERENCES tb_usuarios(usu_id),
    FOREIGN KEY (emp_liv_id) REFERENCES tb_livros(liv_id)
);

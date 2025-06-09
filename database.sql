-- Tabela: usuarios
CREATE TABLE tb_usuarios (
    usu_id INT AUTO_INCREMENT PRIMARY KEY,
    usu_nome VARCHAR(100) NOT NULL,
    usu_matricula VARCHAR(50) UNIQUE NOT NULL,
    usu_telefone VARCHAR(20),
    usu_email VARCHAR(100) UNIQUE,
    usu_tipo VARCHAR(50),
    usu_senha VARCHAR(100)
);

-- Tabela: livros
CREATE TABLE tb_livros (
    liv_id INT AUTO_INCREMENT PRIMARY KEY,
    liv_titulo VARCHAR(200) NOT NULL,
    liv_editora VARCHAR(100),
    liv_ano INT,
    liv_autor VARCHAR(100),
    liv_genero VARCHAR(50),
    liv_quantidade INT
);

-- Tabela: reservas
CREATE TABLE tb_reservas (
    res_id INT AUTO_INCREMENT PRIMARY KEY,
    res_usu_id INT NOT NULL,
    res_liv_id INT NOT NULL,
    res_data_reserva DATE,
    status VARCHAR(50),
    FOREIGN KEY (res_usu_id) REFERENCES tb_usuarios(usu_id),
    FOREIGN KEY (res_liv_id) REFERENCES tb_livros(liv_id)
);

-- Tabela: emprestimos
CREATE TABLE tb_emprestimos (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_usu_id INT NOT NULL,
    emp_liv_id INT NOT NULL,
    emp_data_emprestimo DATE,
    emp_data_a_devolver DATE,
    emp_data_devolucao DATE,
    status VARCHAR(50),
    FOREIGN KEY ( emp_usu_id) REFERENCES tb_usuarios(usu_id),
    FOREIGN KEY (emp_liv_id) REFERENCES tb_livros(liv_id)
);

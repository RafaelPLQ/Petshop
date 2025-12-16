create table cliente(
  id_cliente INT,
  nome VARCHAR(100),
  telefone VARCHAR(20),
  email VARCHAR(100),
  endedeco VARCHAR(150),
  PRIMARY KEY (id_cliente)
);


create table funcionario(
	id_funcionario INT,
	nome VARCHAR(100),
	telefone VARCHAR(20),
	email VARCHAR(100),
	funcao VARCHAR(150),
	PRIMARY KEY (id_funcionario)
);

create table raca(
	id_raca INT,
	nome VARCHAR(45),
	PRIMARY KEY (id_raca)
);

create table especie(
	id_especie INT,
	nome VARCHAR(45),
	PRIMARY KEY (id_especie)
);

create table pet(
	id_pet INT,
	nome VARCHAR(45),
	id_raca INT,
	id_especie INT,
	idade INT,
    id_cliente INT,
    PRIMARY KEY (id_pet),
    FOREIGN KEY (id_raca) 
		REFERENCES raca(id_raca),
    FOREIGN KEY (id_especie) 
		REFERENCES especie(id_especie),
    FOREIGN KEY (id_cliente) 
		REFERENCES cliente(id_cliente)
);

create table servico(
	id_servico INT,
    nome VARCHAR(45),
    valor DECIMAL(10,2),
	PRIMARY KEY (id_servico)
);

create table agendamento(
	id_agendamento INT,
	data_agendamento DATE,
    hora TIME,
    descricao VARCHAR(45),
	id_pet INT,
	id_servico INT,
    id_funcionario INT,
    PRIMARY KEY (id_agendamento),
    FOREIGN KEY (id_pet) 
		REFERENCES pet(id_pet),
    FOREIGN KEY (id_servico) 
		REFERENCES servico(id_servico),
    FOREIGN KEY (id_funcionario) 
		REFERENCES funcionario(id_funcionario)
);

create table pagamento(
	id_pagamento INT,
    id_agendamento INT,
    valor DECIMAL(10,2),
    forma_pagamento VARCHAR(20),
    data_pagamento DATETIME,
	PRIMARY KEY (id_pagamento),
	FOREIGN KEY (id_agendamento) 
		REFERENCES agendamento(id_agendamento)
);

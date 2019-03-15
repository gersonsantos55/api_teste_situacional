# API teste situacional


Simples micro serviço desenvolvido em Python.

Esta API tem como objetivo visualizar e gerenciar transferências feitas por clientes de um banco.

Tomei a liberdade de adicionar dois campos na tabela de banco de dados, "ativo" para fazer exclusão lógica e "data" para fazer a filtragem por data.

A API foi desenvolvida utilizando a IDE PyCharm.

Foram desenvolvidas 3 funções para alcançar esse objetivo, uma de cadastro, uma de consulta que cria um filtro com os parâmetros passados e ignora os com null, e por último uma de exclusão lógica, foi utilizando os framework Flask e PyMySQL.

A documentação detalhada da API utilizando swagger foi a única parte que não foi feita, mas no último tópico disponibilizei as paths para testar as funcionalidades de listagem, e adicionei comentários no código fonte.


# Instalação


Para o funcionamento é necessário ter instalado:

**Python 3.6**

**Flask 1.0.2**

**PyMySQL 0.9.3**

A configuração da conexão com o bando de dados está disponível logo no inicio do arquivo **api_transf.py**.

No arquivo **script_database.sql** se encontra a estrutura do banco com os apmpos novos e alguns registros.

A execução do arquivo pode ser feita da forma que mais for conveniente, como não possuo experiência em implementação de API em Python, eu particularmente sugiro que o teste da mesma seja feito pelo PyCharm, já que automaticamente ele cria uma venv possibilitando que as dependencias sejam instaladas em um ambiente fechado.

Quando executada, a API fica disponível na porta **5000** da máquina.


# PATHS


**No inicio de todos os paths adicionar o ip da máquina e a porta 5000 ex: 127.0.0.1:5000.**
**Quando utilizar os paths, substituir os valores entre <> por ex: usu_id=<usuario_id> para usu_id=1**

Cadastro (Importante não deixar nenhum parâmetro vazio)

/transferencia/cadastrar/usu_id=<usuario_id>&p_nome=<pagador_nome>&p_banco=<pagador_banco>&p_agencia=<pagador_agencia>&p_conta=<pagador_conta>&b_nome=<beneficiario_nome>&b_banco=<beneficiario_banco>&b_agencia=<beneficiario_agencia>&b_conta=<beneficiario_conta>&valor=<valor_da_transferencia> 

Consulta (Importante não deixar nenhum parâmetro vazio)

**Caso não queira utilizar um dos parâmetros para filtrar sua consulta, apenas coloque null ex caso não queira utilizar paginação: _pag_atual=null&tam_pag=null_**

/transferencia/listar/usu_id=<usuario_id>&dt_inicio=<dt_inicio>&dt_fim=<dt_fim>&pag=<pagador>&ben=<beneficiario>&pag_atual=<pagina_atual>&tam_pag=<tamanho_pagina> 
  
 Exclusão
 
 /transferencia/deletar/id=<id_do_registro> 
 
 
# Testando
 

As datas devem ser utilizadas no padrão date time 2000-01-01 00:00:00

Abaixo alguns exemplos.

Retorna todos os registros do banco:

http://127.0.0.1:5000/transferencia/listar/usu_id=null&dt_inicio=null&dt_fim=null&pag=null&ben=null&pag_atual=null&tam_pag=null

Retorna todas as transferências feitas pelo cliente com id 1:

http://127.0.0.1:5000/transferencia/listar/usu_id=1&dt_inicio=null&dt_fim=null&pag=null&ben=null&pag_atual=null&tam_pag=null
  
Retorna todas as transferências feitas no dia 14/03/2019
  
http://127.0.0.1:5000/transferencia/listar/usu_id=1&dt_inicio=2019-03-14%2000:00:00&dt_fim=2019-03-15%2000:00:00&pag=null&ben=null&pag_atual=null&tam_pag=null

Retorna todas as transferências em que tanto o pagador quanto o beneficiário contem a letra **N** no nome

http://127.0.0.1:5000/transferencia/listar/usu_id=1&dt_inicio=null&dt_fim=null&pag=n&ben=n&pag_atual=null&tam_pag=null

Retorna todas as transferências da página 2 sendo que cada página possui 5 registros

http://127.0.0.1:5000/transferencia/listar/usu_id=null&dt_inicio=null&dt_fim=null&pag=null&ben=null&pag_atual=2&tam_pag=5

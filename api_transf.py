from pymysql import connect
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

conn = connect(
    host='localhost',
    user='root',
    passwd='',
    db='teste_situacional'
)

cursor = conn.cursor()


@app.route('/')
def home():
    return '<h1>Bem Vindo!</h1> <p>Essa é uma API desenvolvida para o banco Nix visualizar as transferências feitas ' \
           'pelos seus clientes.</p>'


@app.route('/transferencia/cadastro/'
           'usu_id=<usuario_id>'
           '&p_nome=<pagador_nome>'
           '&p_banco=<pagador_banco>'
           '&p_agencia=<pagador_agencia>'
           '&p_conta=<pagador_conta>'
           '&b_nome=<beneficiario_nome>'
           '&b_banco=<beneficiario_banco>'
           '&b_agencia=<beneficiario_agencia>'
           '&b_conta=<beneficiario_conta>'
           '&valor=<valor>')
def cadastro_transf(usuario_id, pagador_nome, pagador_banco, pagador_agencia, pagador_conta, beneficiario_nome,
                    beneficiario_banco, beneficiario_agencia, beneficiario_conta, valor):
    # Comando para reconectar caso a conexão esteja fechada
    conn.ping(reconnect=True)

    try:
        # Aqui se verifica se o id de usuário informado já está cadastrado, se estiver a API da continuidade
        # ao cadastramento, caso contrário retorna "false" para evitar inconsistencias
        cursor.execute('SELECT id FROM usuario WHERE id = %s', int(usuario_id))

        if cursor.rowcount == 1:

            if (pagador_nome != '' and pagador_banco != '' and pagador_agencia != '' and pagador_conta != ''
                    and beneficiario_nome != '' and beneficiario_banco != '' and beneficiario_agencia != ''
                    and beneficiario_conta != '' and valor != ''):

                if float(valor) <= 100000.0:
                    status = 'OK'
                else:
                    status = 'ERRO'

                if pagador_banco == beneficiario_banco:
                    tipo = 'CC'
                else:
                    horario = datetime.now()
                    if (10 <= horario.hour < 16) and (float(valor) < 5000.0):
                        tipo = 'TED'
                    else:
                        tipo = 'DOC'

                sql = 'INSERT INTO transferencia (usuario_id, pagador_nome, pagador_banco, pagador_agencia, ' \
                      'pagador_conta, beneficiario_nome, beneficiario_banco, beneficiario_agencia, beneficiario_conta, ' \
                      'valor, tipo, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                cursor.execute(sql, (int(usuario_id), pagador_nome, pagador_banco, pagador_agencia, pagador_conta,
                                     beneficiario_nome, beneficiario_banco, beneficiario_agencia, beneficiario_conta,
                                     float(valor), tipo, status))
                conn.commit()

                resposta = True
            else:
                resposta = False
        else:
            resposta = False
    except:
        # Se der qualquer exceção ele desfaz as alterações no banco
        conn.rollback()
        resposta = False
    finally:
        # Fecha a conexão para aliviar o banco de dados
        conn.close()

    return jsonify(resposta)


@app.route('/transferencia/listar/usu_id=<usuario_id>'
           '&dt_inicio=<dt_inicio>'
           '&dt_fim=<dt_fim>'
           '&pag=<pagador>'
           '&ben=<beneficiario>'
           '&pag_atual=<pagina_atual>'
           '&tam_pag=<tamanho_pagina>')
def listar_transf(usuario_id, dt_inicio, dt_fim, pagador, beneficiario, pagina_atual, tamanho_pagina):
    conn.ping(reconnect=True)

    # Por padrão a busca só irá trazer os registros ativos
    sql = 'SELECT id, usuario_id, pagador_nome, pagador_banco, pagador_agencia, pagador_conta, ' \
          'beneficiario_nome, beneficiario_banco, beneficiario_agencia, beneficiario_conta, valor, ' \
          'tipo, status FROM transferencia WHERE ativo = 1 '

    sql = monta_consulta_sql_transf(sql, usuario_id, dt_inicio, dt_fim, pagador, beneficiario, pagina_atual,
                                    tamanho_pagina)

    cursor.execute(sql)

    print(sql)

    results = cursor.fetchall()

    # Pegando o nome dos campos para inserir no json
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    sql_consulta_total = 'SELECT SUM(valor) AS somatoria_valor, COUNT(id) AS total_transferencias FROM ' \
                         '(' + sql + ') AS subquery'

    print(sql_consulta_total)

    cursor.execute(sql_consulta_total)
    results = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return jsonify(json_data)


def monta_consulta_sql_transf(sql, usuario_id, dt_inicio, dt_fim, pagador, beneficiario, pagina_atual, tamanho_pagina):
    # Monta a sql de acordo com os parametros preenchidos
    if usuario_id != 'null':
        sql += ' AND usuario_id = ' + usuario_id
    if pagador != 'null':
        sql += ' AND pagador_nome LIKE \'%' + pagador + '%\''
    if beneficiario != 'null':
        sql += ' AND beneficiario_nome LIKE \'%' + beneficiario + '%\''
    if dt_inicio != 'null':
        sql += ' AND data >= \'' + dt_inicio + '\''
    if dt_fim != 'null':
        sql += ' AND data < \'' + dt_fim + '\''
    if pagina_atual != 'null' and tamanho_pagina != 'null':
        inicio = str((int(pagina_atual) - 1) * int(tamanho_pagina))
        fim = tamanho_pagina
        sql += ' LIMIT ' + inicio + ',' + fim
    return sql


@app.route('/transferencia/deletar/id=<id>')
def delete_transf(id):
    conn.ping(reconnect=True)

    try:
        # Exclusão lógica setando o campo "ativo" para 0
        cursor.execute('UPDATE transferencia SET ativo = 0 WHERE id = %s', int(id))

        # Verifica se o campo "ativo" foi realmente alterado para 0
        cursor.execute('SELECT id FROM transferencia WHERE id = %s AND ativo = 0', int(id))

        # Se ele retornar um registro então retorna "true" para a tela, se não retorna "false"
        if cursor.rowcount == 1:
            resposta = True
            conn.commit()
        else:
            resposta = False
            conn.rollback()
    except:
        conn.rollback()
    finally:
        conn.close()
    return jsonify(resposta)


if __name__ == '__main__':
    app.run(debug=True)

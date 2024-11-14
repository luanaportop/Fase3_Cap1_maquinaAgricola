# instalando bibliotecas

import oracledb
import pandas as pd
import os

#conectando banco de dados
try:
    conn = oracledb.connect(user='', password='', dsn='oracle.fiap.com.br:1521/ORCL') # Inserir user e password correspondente
    #CRUD
    var_create = conn.cursor()
    var_read = conn.cursor()
    var_update = conn.cursor()
    var_delete = conn.cursor()

except Exception as e:
    print("Erro: ", e)
    conexao = False
else:
    conexao = True
if conexao:
    print("Conexão estabelecida com sucesso.")
    print()
else:
    print("Falha na conexão.")

# Funções

def create_dados():
    # Função para inserção de dados no banco criado
    while True:
        try:
            print("-------Registrar-------")
            # Recebendo os inputs
            ph = float(input("Digite a leitura do sensor de PH: "))
            fosforo = input("Presença de Fósforo no solo? (S/N): ")
            potassio = input("Presença de Potássio no solo? (S/N): ")
            umidade = float(input("Digite a leitura do sensor de Umidade (%): "))
            temperatura = float(input("Digite a leitura do sensor de Temperatura (°C): "))

            # Instrução banco de dados
            cadastro = "INSERT INTO t_sensor (id_sensor, leitura_ph, leitura_fosforo_p, leitura_potassio_k, leitura_umidade, leitura_temperatura) VALUES (SENSOR_SEQ.NEXTVAL, :1, :2, :3, :4, :5)"
            var_create.execute(cadastro, (ph, fosforo, potassio, umidade, temperatura))
            conn.commit()
        except ValueError:
            print("Digite um número válido!")
        except Exception as e:
            print("Algo deu errado...", e)
        else:
            print("DADOS ARMAZENADOS")

        continuar = input("Deseja inserir outros dados? (s/n): ").strip().lower()
        if continuar != 's':
            break

def consulta_dados():
    print("-------- CONSULTAR --------")

    lista_dados = []
    try:
        consulta = "SELECT id_sensor, leitura_ph, leitura_fosforo_p, leitura_potassio_k, leitura_umidade, leitura_temperatura, data_hora FROM t_sensor"
        var_read.execute(consulta)

        data = var_read.fetchall()
        for dt in data:
            lista_dados.append(dt)

        lista_dados.sort()

        data_frame_dados = pd.DataFrame.from_records(lista_dados, columns=['id_sensor', 'leitura_ph', 'leitura_fosforo_p', 'leitura_potassio_k', 'leitura_umidade', 'leitura_temperatura', 'data_hora'])
        data_frame_dados['data_hora'] = pd.to_datetime(data_frame_dados['data_hora']).dt.strftime('%Y-%m-%d %H:%M:%S')

        if data_frame_dados.empty:
            print("Não há dados armazenados!")
        else:
            print(data_frame_dados.to_string(index=False))

    except Exception as e:
        print("Algo deu errado:", e)

def update_dados():
    try:
        print("-------Atualizar-------")
        sensor_id = int(input("Escolha um ID: "))

        # Verificar se o sensor existe
        consulta = "SELECT * FROM t_sensor WHERE id_sensor = :1"
        var_read.execute(consulta, (sensor_id,))
        data = var_read.fetchall()

        if len(data) == 0:
            print(f"Não existe sensor com o ID = {sensor_id}")
        else:
            # Pedir novos valores ao usuário
            novo_ph = float(input("Digite um novo valor para leitura do sensor de PH: "))
            novo_fosforo = input("Presença de Fósforo no solo? (S/N): ")
            novo_potassio = input("Presença de Potássio no solo? (S/N):: ")
            nova_umidade = float(input("Digite um novo valor para leitura do sensor de Umidade: "))
            nova_temperatura = float(input("Digite um novo valor para leitura do sensor de Temperatura (°C): "))

            # Atualizar os dados
            atualizar = """
                UPDATE t_sensor
                SET leitura_ph = :1, leitura_fosforo_p = :2, leitura_potassio_k = :3, leitura_umidade = :4, leitura_temperatura = :5
                WHERE id_sensor = :6
            """
            var_update.execute(atualizar, (novo_ph, novo_fosforo, novo_potassio, nova_umidade, nova_temperatura, sensor_id))
            conn.commit()
            print("Dados atualizados com sucesso!")
    except ValueError as e:
        print("Erro de valor, por favor insira um número válido.", e)
    except Exception as e:
        print("Algo deu errado!", e)

def leitura_irrigacao():
    try:
        print("-------Controle da Irrigação-------")

        limite_umidade = 30.0

        # Obter o último registro do sensor de umidade
        consulta = "SELECT * FROM t_sensor ORDER BY data_hora DESC FETCH FIRST 1 ROWS ONLY"
        var_read.execute(consulta)
        data = var_read.fetchone()

        if data:
            id_sensor, _, _, _, leitura_umidade, leitura_temperatura, data_hora = data

            # Verificar se a umidade está abaixo do limite
            if leitura_umidade < limite_umidade:
                # Registrar a irrigação na tabela t_irrigacao
                irrigacao_sql = "INSERT INTO t_irrigacao (id_irrigacao, id_sensor, data_hora) VALUES (IRRIGACAO_SEQ.NEXTVAL, :1, CURRENT_TIMESTAMP)"
                var_create.execute(irrigacao_sql, (id_sensor,))
                conn.commit()
                print("Irrigação ativada e registrada.")
            else:
                print("A umidade do solo está adequada. Não é necessário irrigação!.")
        else:
            print("Nenhum dado de sensor foi encontrado.")
    except Exception as e:
        print("Erro no controle da irrigação:", e)

def delet_dados():
    print("-------- DELETAR --------")

    escolha_id = input("Escolha um ID: ")

    if escolha_id.isdigit():
        escolha_id = int(escolha_id)

        try:
            consulta = "SELECT * FROM t_sensor WHERE id_sensor = :id"
            var_read.execute(consulta, [escolha_id])
            dado = var_read.fetchone()

            if dado:
                deletar = f"""DELETE FROM t_sensor WHERE id_sensor = {escolha_id}"""
                var_delete.execute(deletar)
                conn.commit()
                print("Dados deletados com sucesso!")
            else:
                print(f"Não há dados com o ID = {escolha_id}")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
    else:
        print("O ID fornecido não é válido.")

# MENU
while conexao:
    os.system('cls')

    # Menu
    print("-------------MENU-------------")
    print(""""
    1 - Registrar dados
    2 - Listar dados
    3 - Atualizar dados
    4 - Deletar dados
    5 - Controle irrigação
    6 - Sair
    """)
    # input
    escolha = input("Escolha um número: ")

    if escolha.isdigit():
        escolha = int(escolha)
    else:
        print("Digite um número!")
        continue

    match escolha:
        case 1:
            create_dados()
        case 2:
            consulta_dados()
        case 3:
            update_dados()
        case 4:
            delet_dados()
        case 5:
            leitura_irrigacao()
        case 6:
            break
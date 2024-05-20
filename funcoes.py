import oracledb
import os 
import time
import json

TABLE_NAME = "T_CH_PRODUTOS"

def saida():
    print("""  
   ___ _          _                 _                    _               _     _ _        
  /___\ |__  _ __(_) __ _  __ _  __| | ___    _ __   ___| | __ _  __   _(_)___(_) |_ __ _ 
 //  // '_ \| '__| |/ _` |/ _` |/ _` |/ _ \  | '_ \ / _ \ |/ _` | \ \ / / / __| | __/ _` |
/ \_//| |_) | |  | | (_| | (_| | (_| | (_) | | |_) |  __/ | (_| |  \ V /| \__ \ | || (_| |
\___/ |_.__/|_|  |_|\__, |\__,_|\__,_|\___/  | .__/ \___|_|\__,_|   \_/ |_|___/_|\__\__,_|
                    |___/                    |_|                                          """)
def cabecalho():
     
     limpar_tela()
     print("""
                     _        _           _ _                       
  ___ _ __ _   _  __| |   ___| |__   __ _| | | ___ _ __   __ _  ___ 
 / __| '__| | | |/ _` |  / __| '_ \ / _` | | |/ _ \ '_ \ / _` |/ _ 
| (__| |  | |_| | (_| | | (__| | | | (_| | | |  __/ | | | (_| |  __/
 \___|_|   \__,_|\__,_|  \___|_| |_|\__,_|_|_|\___|_| |_|\__, |\___|
                                                         |___/      """)

def limpar_tela():
    # Verifica o sistema operacional
    if os.name == 'posix':  # Para Linux e macOS
        _ = os.system('clear')
    elif os.name == 'nt':  # Para Windows
        _ = os.system('cls')
    else:
        # Se não estiver em nenhum dos sistemas acima, limpa usando caracteres de nova linha
        print('\n' * 100)  # Imprime 100 novas linhas para "limpar" a tela

def pula_linha(valor):
    print("\n" * valor)

def menu():
    print("1- INSERIR PRODUTO")
    print("2- LISTAR PRODUTOS")
    print("3- BUSCAR PRODUTO")
    print("4- ALTERAR PRODUTOS")
    print("5- DELETAR PRODUTOS")
    print("6- SAIR")
    print("\n")

def conexa_db():
    try:
        
        with open("credenciais.json") as f:
                credenciais = json.load(f)

        USER = credenciais["user"]
        PASS = credenciais["pass"]
    
        # Conecta o servidor
        dsnStr = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")
        # Efetua a conexão com o Usuário
        connection = oracledb.connect(user=USER, password=PASS, dsn=dsnStr)

        return connection

    except FileNotFoundError:
        print("Arquivo não encontrado")    
    except Exception as e:
        print("Conexão mal-sucedida {e}")


def criar_cursor(connection):
    cursor = connection.cursor()

    return cursor

def inserir_produto(id_produto, nome, descricao, area_atuacao, valor):

    connection = conexa_db()
    

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Comando SQL para inserir um novo produto na tabela
        sql = f"INSERT INTO {TABLE_NAME} (id_produto, nome, descricao, area_atuacao, valor) VALUES (:1, :2, :3, :4, :5)"

        # Executar o comando SQL com os parâmetros
        cursor.execute(sql, (id_produto, nome, descricao, area_atuacao, valor))

        # Confirmar a transação
        connection.commit()
        print("Produto inserido com sucesso!")

    except oracledb.Error as error:
        print(f"Erro ao inserir produto: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def listar_produtos():
    # Estabelecer conexão com o banco de dados Oracle
    connection = conexa_db()

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Comando SQL para selecionar todos os produtos da tabela
        sql = f"SELECT id_produto, nome, descricao, area_atuacao, valor FROM {TABLE_NAME}"

        # Executar o comando SQL
        cursor.execute(sql)

        # Recuperar todos os resultados da consulta
        produtos = cursor.fetchall()

        # Imprimir os resultados
        print("Lista de Produtos:")
        print("=================")
        for produto in produtos:
            print(f"ID: {produto[0]}")
            print(f"Nome: {produto[1]}")
            print(f"Descrição: {produto[2]}")
            print(f"Área de Atuação: {produto[3]}")
            print(f"Valor: R$ {produto[4]}")
            print("-----------------")

    except oracledb.Error as error:
        print(f"Erro ao listar produtos: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Função para buscar um produto por ID
def buscar_produto_por_id(id_produto):
    # Estabelecer conexão com o banco de dados Oracle
    connection = conexa_db()

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Comando SQL para selecionar um produto pelo ID
        sql = f"SELECT id_produto, nome, descricao, area_atuacao, valor FROM {TABLE_NAME} WHERE id_produto = :id_produto"

        # Executar o comando SQL com o parâmetro de ID do produto
        cursor.execute(sql, {'id_produto': id_produto})

        # Recuperar o resultado da consulta
        produto = cursor.fetchone()

        if produto:
            print("Detalhes do Produto:")
            print("===================")
            print(f"ID: {produto[0]}")
            print(f"Nome: {produto[1]}")
            print(f"Descrição: {produto[2]}")
            print(f"Área de Atuação: {produto[3]}")
            print(f"Valor: R$ {produto[4]}")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")

    except oracledb.Error as error:
        print(f"Erro ao buscar produto: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Função para buscar um produto por ID e exportar para JSON
def exportar_produto_para_json(id_produto, nome_arquivo):
    # Estabelecer conexão com o banco de dados Oracle
    connection = conexa_db()

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Comando SQL para selecionar um produto pelo ID
        sql = f"SELECT id_produto, nome, descricao, area_atuacao, valor FROM {TABLE_NAME} WHERE id_produto = :id_produto"

        # Executar o comando SQL com o parâmetro de ID do produto
        cursor.execute(sql, {'id_produto': id_produto})

        # Recuperar o resultado da consulta
        produto = cursor.fetchone()

        if produto:
            # Criar um dicionário com os dados do produto
            produto_dict = {
                'id_produto': produto[0],
                'nome': produto[1],
                'descricao': produto[2],
                'area_atuacao': produto[3],
                'valor': float(produto[4]) if produto[4] is not None else None
            }

            # Exportar o dicionário para JSON
            with open(nome_arquivo, 'w') as json_file:
                json.dump(produto_dict, json_file, indent=4)
            
            print(f"Dados do produto exportados para o arquivo: {nome_arquivo}\n")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")

    except oracledb.Error as error:
        print(f"Erro ao buscar produto e exportar para JSON: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Função para alterar os dados de um produto
def alterar_produto(id_produto, novo_nome, nova_descricao, nova_area_atuacao, novo_valor):
    # Estabelecer conexão com o banco de dados Oracle
    connection = conexa_db()

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Verificar se o produto com o ID fornecido existe na tabela
        if verificar_produto_existente(id_produto, cursor):
            # Comando SQL para atualizar um produto na tabela
            sql = f"""
                UPDATE {TABLE_NAME}
                SET nome = :novo_nome,
                    descricao = :nova_descricao,
                    area_atuacao = :nova_area_atuacao,
                    valor = :novo_valor
                WHERE id_produto = :id_produto
            """

            # Executar o comando SQL com os novos valores
            cursor.execute(sql, {
                'novo_nome': novo_nome,
                'nova_descricao': nova_descricao,
                'nova_area_atuacao': nova_area_atuacao,
                'novo_valor': novo_valor,
                'id_produto': id_produto
            })

            # Confirmar a transação
            connection.commit()
            print(f"Dados do produto com ID {id_produto} foram alterados com sucesso.")
        else:
            print(f"Produto com ID {id_produto} não encontrado. Nenhuma alteração foi realizada.")

    except oracledb.Error as error:
        print(f"Erro ao alterar produto: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()




# Função para excluir um produto pelo ID
def excluir_produto(id_produto):

    # Estabelecer conexão com o banco de dados Oracle
    connection = conexa_db()

    try:
        # Criar um cursor para executar comandos SQL
        cursor = criar_cursor(connection)

        # Verificar se o produto com o ID fornecido existe na tabela
        if verificar_produto_existente(id_produto, cursor):
            # Comando SQL para excluir um produto da tabela
            sql = f"DELETE FROM {TABLE_NAME} WHERE id_produto = :id_produto"

            # Executar o comando SQL com o parâmetro de ID do produto
            cursor.execute(sql, {'id_produto': id_produto})

            # Confirmar a transação
            connection.commit()
            print(f"Produto com ID {id_produto} foi excluído com sucesso.")
        else:
            print(f"Produto com ID {id_produto} não encontrado. Nenhuma exclusão foi realizada.")

    except oracledb.Error as error:
        print(f"Erro ao excluir produto: {error}")

    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Função para verificar se um produto existe pelo ID
def verificar_produto_existente(id_produto, cursor):
    # Comando SQL para verificar se o produto existe
    sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE id_produto = :id_produto"

    # Executar o comando SQL com o parâmetro de ID do produto
    cursor.execute(sql, {'id_produto': id_produto})

    # Recuperar o resultado da contagem
    count = cursor.fetchone()[0]

    return count > 0



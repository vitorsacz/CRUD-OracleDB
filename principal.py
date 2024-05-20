import funcoes as f
import time 

while True:

    f.cabecalho()
    f.menu()

    opcao = int(input("Informe sua opção: "))

    if opcao == 1:
        while True:
            f.limpar_tela()
            f.cabecalho()

            id = int(input('Informe o id do produto: '))
            nome = input('Informe o nome do produto: ')
            descricao = input('Informe a descrição do produto: ')
            area_atuacao = input('Informe a área de atuação do produto: ')
            preco = int(input('Informe o valor do produto: '))
            
            f.pula_linha(2)

            f.inserir_produto(id, nome, descricao, area_atuacao, preco)

            op = int(input("\n\nGostaria de inserir outro produto?\n1- SIM\n2- NÃO\n"))

            if op == 2:
                break
            
    elif opcao == 2:
        f.limpar_tela()
        f.listar_produtos()
        time.sleep(5)

    elif opcao == 3:
        f.limpar_tela()
        f.pula_linha(1)
        f.listar_produtos()
        f.pula_linha(2)

        id = int(input("informe o id produto que deseja as informações: "))

        f.pula_linha(1)

        f.buscar_produto_por_id(id)

        f.pula_linha(2)

        exportar = int(input("Deseja exportar esse produto em arquivo JSON?\n1- SIM \n2- NÃO\n"))

        if exportar == 1:
            nome_arquivo = input("Informe um nome para o arquivo: ")
            f.exportar_produto_para_json(id, nome_arquivo)

        else:
            print("Sem problemas!")
            break

    elif opcao == 4:
        while True:
            f.limpar_tela()
            f.cabecalho()
            f.listar_produtos()
        
            id_produto = int(input("\n\nInforme o id do produto que você deseja alterar: \n"))

            
            novo_nome = input('Informe o novo nome do produto: ')
            nova_descricao = input('Informe a nova descrição do produto: ')
            nova_area_atuacao = input('Informe a área de atuação do produto: ')
            novo_preco = int(input('Informe o valor do produto: '))
            
            f.pula_linha(2)
            f.alterar_produto(id_produto, novo_nome, nova_descricao, nova_area_atuacao, novo_preco)

            op = int(input("\n\nGostaria de alterar outro produto?\n1- SIM\n2- NÃO\n"))

            if op == 2:
                break

    elif opcao == 5:
       while True:
            f.limpar_tela()
            f.pula_linha(2)
            f.listar_produtos()
            f.pula_linha(2)

            id_produto = int(input("Informe o id do produto que deseja deletar: \n"))

            op = int(input("Você tem certeza que deseja concluir a ação?\n1- SIM\n2- NÃO\n"))

            if op == 1:
                f.excluir_produto(id_produto)
            else:
                print("Continuando...")
                break

            opcao = int(input("\n\nDeseja excluir outro produto? \n1- SIM\n2- NÃO\n"))

            if opcao == 2:
               break
            
    elif opcao == 6:
        f.limpar_tela()
        print("\n\n")
        f.saida()
        print("\n\n")
        break


    
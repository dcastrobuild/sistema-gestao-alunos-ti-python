
ARQUIVO_DADOS = "alunos.txt"

# Valor de cada curso por turno
MENSALIDADES = {
    (1, 1): 210.00,   # PHP    - Manha
    (1, 2): 260.00,   # PHP    - Noite
    (2, 1): 320.00,   # Java   - Manha
    (2, 2): 390.00,   # Java   - Noite
    (3, 1): 290.00,   # Python - Manha
    (3, 2): 310.00,   # Python - Noite
}

NOMES_CURSOS = {1: "PHP", 2: "Java", 3: "Python"}
NOMES_TURNOS = {1: "Manha", 2: "Noite"}
NOMES_SEXO   = {1: "Feminino", 2: "Masculino"}
SIGLA_SEXO   = {1: "F", 2: "M"}


def carregar_alunos():
    # Le o arquivo linha por linha e monta a lista de alunos.
    # Se o arquivo nao existir ainda, devolve lista vazia.
    lista = []

    try:
        arquivo = open(ARQUIVO_DADOS, "r", encoding="utf-8")
    except FileNotFoundError:
        return lista

    for linha in arquivo:
        linha = linha.strip()
        if linha == "":
            continue

        campos = linha.split(";")

        # Linha com numero errado de campos e ignorada para nao travar o programa
        if len(campos) != 7:
            continue

        try:
            # Converte "1,2" para lista de inteiros [1, 2]
            cursos = []
            for parte in campos[4].split(","):
                cursos.append(int(parte))

            turnos = []
            for parte in campos[5].split(","):
                turnos.append(int(parte))

            aluno = {
                "matricula":   int(campos[0]),
                "nome":        campos[1],
                "sexo":        int(campos[2]),
                "idade":       int(campos[3]),
                "cursos":      cursos,
                "turnos":      turnos,
                "mensalidade": float(campos[6])
            }
            lista.append(aluno)
        except ValueError:
            continue

    arquivo.close()
    return lista


def salvar_alunos(lista_alunos):
    # Grava todos os alunos no arquivo, um por linha.
    arquivo = open(ARQUIVO_DADOS, "w", encoding="utf-8")

    for aluno in lista_alunos:
        # Converte [1, 2] para "1,2"
        cursos_str = ""
        for i in range(len(aluno["cursos"])):
            if i > 0:
                cursos_str = cursos_str + ","
            cursos_str = cursos_str + str(aluno["cursos"][i])

        turnos_str = ""
        for i in range(len(aluno["turnos"])):
            if i > 0:
                turnos_str = turnos_str + ","
            turnos_str = turnos_str + str(aluno["turnos"][i])

        linha = (str(aluno["matricula"])               + ";" +
                 aluno["nome"]                         + ";" +
                 str(aluno["sexo"])                    + ";" +
                 str(aluno["idade"])                   + ";" +
                 cursos_str                            + ";" +
                 turnos_str                            + ";" +
                 "{:.2f}".format(aluno["mensalidade"]) + "\n")

        arquivo.write(linha)

    arquivo.close()


def ler_inteiro(mensagem, opcoes_validas):
    # Pede um numero e so aceita se estiver entre as opcoes validas.
    # Protege contra letras, simbolos e numeros fora do esperado.
    while True:
        try:
            valor = int(input(mensagem))
            if valor in opcoes_validas:
                return valor
            print("  Opcao invalida. Tente novamente.")
        except ValueError:
            print("  Digite apenas numeros.")


def ler_idade():
    # Pede a idade e valida se esta entre 16 e 120.
    while True:
        try:
            idade = int(input("  Idade: "))
            if idade >= 16 and idade <= 120:
                return idade
            print("  Idade invalida. A idade minima é 16 anos e a maxima é 120.")
        except ValueError:
            print("  Digite apenas numeros.")


def ler_nome(mensagem):
    # Pede o nome e valida as seguintes regras:
    #   - Apenas letras e espacos (sem numeros ou simbolos)
    #   - Minimo de 2 caracteres, maximo de 60
    #   - Espacos duplos internos sao reduzidos para um unico espaco
    # Isso impede entradas como "C4stro", "Ana;Silva" ou "Ana   Castro".
    while True:
        nome = input(mensagem).strip()

        # Reduz qualquer sequencia de espacos internos para um unico espaco
        while "  " in nome:
            nome = nome.replace("  ", " ")

        if len(nome) < 2:
            print("  Nome invalido. Digite ao menos 2 letras.")
            continue

        if len(nome) > 60:
            print("  Nome muito longo. Maximo de 60 caracteres.")
            continue

        valido = True
        for c in nome:
            if not (c.isalpha() or c == " "):
                valido = False
                break

        if not valido:
            print("  Nome invalido. Use apenas letras e espacos.")
            continue

        return nome


def turno_ja_usado(turnos, turno):
    # Verifica se o turno ja esta ocupado por outro curso.
    # Impede dois cursos no mesmo horario (ex: PHP Manha + Java Manha).
    for t in turnos:
        if t == turno:
            return True
    return False


def curso_ja_cadastrado(cursos, curso):
    # Verifica se o aluno ja esta matriculado nesse curso.
    # Impede o mesmo curso em turnos diferentes (ex: Python Manha + Python Noite).
    for c in cursos:
        if c == curso:
            return True
    return False



def gerar_matricula(lista_alunos):
    # Acha a maior matricula da lista e soma 1.
    # Comeca do 1001 se ainda nao houver alunos.
    if len(lista_alunos) == 0:
        return 1001

    maior = lista_alunos[0]["matricula"]
    for aluno in lista_alunos:
        if aluno["matricula"] > maior:
            maior = aluno["matricula"]

    return maior + 1


def calcular_mensalidade(cursos, turnos, idade):
    # Soma o valor de cada curso no turno escolhido.
    # Desconto de 30% para mais de 1 curso (tem prioridade).
    # Desconto de 15% para mais de 45 anos (so se tiver 1 curso).
    total = 0.0
    for i in range(len(cursos)):
        chave = (cursos[i], turnos[i])
        total = total + MENSALIDADES[chave]

    if len(cursos) > 1:
        total = total * 0.70
    elif idade > 45:
        total = total * 0.85

    return round(total, 2)


def coletar_cursos():
    # Coleta os cursos do aluno durante o cadastro.
    # Regras: nao repete curso, nao repete turno, limite de 2 cursos.
    cursos = []
    turnos = []

    while True:
        if len(cursos) == 2:
            print("  Limite de 2 cursos atingido (um por turno).")
            break

        print("  Cursos disponiveis: 1-PHP / 2-Java / 3-Python")
        curso = ler_inteiro("  Curso: ", [1, 2, 3])

        if curso_ja_cadastrado(cursos, curso):
            print("  " + NOMES_CURSOS[curso] + " ja foi adicionado. Escolha outro curso.")
            continue

        print("  Turnos disponiveis: 1-Manha / 2-Noite")
        turno = ler_inteiro("  Turno: ", [1, 2])

        if turno_ja_usado(turnos, turno):
            print("  Turno " + NOMES_TURNOS[turno] + " ja esta ocupado. Escolha o outro turno.")
            continue

        cursos.append(curso)
        turnos.append(turno)
        print("  Adicionado: " + NOMES_CURSOS[curso] + " - " + NOMES_TURNOS[turno])

        if len(cursos) < 2:
            outro = input("  Deseja cadastrar outro curso? (1-Sim / 2-Nao): ").strip()
            if outro != "1":
                break

    return cursos, turnos


def cadastrar_aluno(lista_alunos):
    # Coleta os dados, gera matricula, calcula mensalidade e salva.
    print("\n  === CADASTRO DE ALUNO ===")

    nome  = ler_nome("  Nome: ")
    sexo  = ler_inteiro("  Sexo (1-Feminino / 2-Masculino): ", [1, 2])
    idade = ler_idade()

    cursos, turnos = coletar_cursos()

    matricula   = gerar_matricula(lista_alunos)
    mensalidade = calcular_mensalidade(cursos, turnos, idade)

    aluno = {
        "matricula":   matricula,
        "nome":        nome,
        "sexo":        sexo,
        "idade":       idade,
        "cursos":      cursos,
        "turnos":      turnos,
        "mensalidade": mensalidade
    }

    lista_alunos.append(aluno)
    salvar_alunos(lista_alunos)

    print("\n  Aluno cadastrado com sucesso!")
    print("  Matricula: " + str(matricula) + " | Mensalidade: R$ " + "{:.2f}".format(mensalidade))

def buscar_aluno_por_matricula(lista_alunos, matricula):
    # Percorre a lista procurando pela matricula.
    # Retorna a posicao e o dicionario do aluno, ou -1 e None.
    for i in range(len(lista_alunos)):
        if lista_alunos[i]["matricula"] == matricula:
            return i, lista_alunos[i]
    return -1, None

def gerenciar_cursos(aluno):
    # Tela de edicao de cursos: remove ou adiciona, respeitando as regras.
    while True:
        print("\n  Cursos atuais:")
        for i in range(len(aluno["cursos"])):
            c = aluno["cursos"][i]
            t = aluno["turnos"][i]
            print("    " + str(i + 1) + " - " + NOMES_CURSOS[c] + " (" + NOMES_TURNOS[t] + ")")

        print("\n  O que deseja fazer?")
        print("  1 - Remover um curso")
        print("  2 - Adicionar um curso")
        print("  3 - Concluir")
        opcao = input("  Opcao: ").strip()

        # --- Remover ---
        if opcao == "1":
            if len(aluno["cursos"]) == 1:
                print("  O aluno precisa ter ao menos 1 curso. Remocao nao permitida.")
                continue

            try:
                num = int(input("  Digite o numero do curso a remover (1-" + str(len(aluno["cursos"])) + "): "))
                idx = num - 1
                if idx >= 0 and idx < len(aluno["cursos"]):
                    nome_curso = NOMES_CURSOS[aluno["cursos"][idx]]
                    nome_turno = NOMES_TURNOS[aluno["turnos"][idx]]
                    aluno["cursos"].pop(idx)
                    aluno["turnos"].pop(idx)
                    print("  Curso " + nome_curso + " (" + nome_turno + ") removido.")
                else:
                    print("  Numero invalido.")
            except ValueError:
                print("  Digite apenas numeros.")

        # --- Adicionar ---
        elif opcao == "2":
            if len(aluno["cursos"]) == 2:
                print("  Limite de 2 cursos atingido. Remova um antes de adicionar.")
                continue

            print("  Cursos disponiveis: 1-PHP / 2-Java / 3-Python")
            curso = ler_inteiro("  Curso: ", [1, 2, 3])

            if curso_ja_cadastrado(aluno["cursos"], curso):
                print("  " + NOMES_CURSOS[curso] + " ja esta cadastrado. Escolha outro curso.")
                continue

            print("  Turnos disponiveis: 1-Manha / 2-Noite")
            turno = ler_inteiro("  Turno: ", [1, 2])

            if turno_ja_usado(aluno["turnos"], turno):
                print("  Turno " + NOMES_TURNOS[turno] + " ja esta ocupado. Escolha o outro turno.")
                continue

            aluno["cursos"].append(curso)
            aluno["turnos"].append(turno)
            print("  Adicionado: " + NOMES_CURSOS[curso] + " (" + NOMES_TURNOS[turno] + ")")

        # --- Concluir ---
        elif opcao == "3":
            break

        else:
            print("  Opcao invalida.")

def editar_aluno(lista_alunos):
    # Busca o aluno pela matricula e permite alterar cada campo.
    # A mensalidade e sempre recalculada ao salvar.
    print("\n  === EDITAR ALUNO ===")

    try:
        matricula = int(input("  Digite a matricula do aluno: "))
    except ValueError:
        print("  Matricula invalida.")
        return

    indice, aluno = buscar_aluno_por_matricula(lista_alunos, matricula)
    if aluno is None:
        print("  Aluno nao encontrado.")
        return

    print("\n  Aluno encontrado: " + aluno["nome"])
    print("  Deixe em branco para manter o valor atual.\n")

    # Nome
    print("  Nome atual: " + aluno["nome"])
    trocar_nome = input("  Deseja alterar o nome? (1-Sim / 2-Nao): ").strip()
    if trocar_nome == "1":
        aluno["nome"] = ler_nome("  Novo nome: ")

    # Sexo
    sexo_atual = NOMES_SEXO[aluno["sexo"]]
    entrada = input("  Sexo (1-Feminino / 2-Masculino) [" + sexo_atual + "]: ").strip()
    if entrada == "1" or entrada == "2":
        aluno["sexo"] = int(entrada)

    # Idade
    entrada = input("  Idade [" + str(aluno["idade"]) + "]: ").strip()
    if entrada != "":
        try:
            nova_idade = int(entrada)
            if nova_idade >= 16 and nova_idade <= 120:
                aluno["idade"] = nova_idade
            else:
                print("  Idade invalida. A idade minima e 16 anos.")
        except ValueError:
            print("  Valor invalido. Mantendo idade atual.")

    # Cursos
    alterar = input("\n  Deseja alterar os cursos? (1-Sim / 2-Nao): ").strip()
    if alterar == "1":
        gerenciar_cursos(aluno)

    aluno["mensalidade"] = calcular_mensalidade(aluno["cursos"], aluno["turnos"], aluno["idade"])

    lista_alunos[indice] = aluno
    salvar_alunos(lista_alunos)

    print("\n  Aluno atualizado com sucesso!")
    print("  Nova mensalidade: R$ " + "{:.2f}".format(aluno["mensalidade"]))


def remover_aluno(lista_alunos):
    # Remove o aluno da lista depois de confirmacao.
    print("\n  === REMOVER ALUNO ===")

    try:
        matricula = int(input("  Digite a matricula do aluno: "))
    except ValueError:
        print("  Matricula invalida.")
        return

    indice, aluno = buscar_aluno_por_matricula(lista_alunos, matricula)
    if aluno is None:
        print("  Aluno nao encontrado.")
        return

    print("\n  Aluno: " + aluno["nome"] + " | Matricula: " + str(aluno["matricula"]))
    confirmacao = input("  Confirma remocao? (1-Sim / 2-Nao): ").strip()

    if confirmacao == "1":
        lista_alunos.pop(indice)
        salvar_alunos(lista_alunos)
        print("  Aluno removido com sucesso.")
    else:
        print("  Operacao cancelada.")

def exibir_linha_aluno(aluno):
    # Monta e imprime uma linha formatada na tabela de listagem.
    cursos_str = ""
    for i in range(len(aluno["cursos"])):
        if i > 0:
            cursos_str = cursos_str + " / "
        c = aluno["cursos"][i]
        t = aluno["turnos"][i]
        cursos_str = cursos_str + NOMES_CURSOS[c] + "(" + NOMES_TURNOS[t] + ")"

    print(
        f"  {aluno['matricula']:<8} "
        f"{aluno['nome']:<25} "
        f"{SIGLA_SEXO[aluno['sexo']]:<4} "
        f"{aluno['idade']:<6} "
        f"{cursos_str:<35} "
        f"R$ {aluno['mensalidade']:>8.2f}"
    )

def cabecalho_listagem():
    # Imprime o titulo das colunas antes de listar os alunos.
    print()
    print(f"  {'Matricula':<8} {'Nome':<25} {'Sx':<4} {'Idade':<6} {'Cursos (Turno)':<35} {'Mensalidade':>11}")
    print("  " + "-" * 93)


def listagem_geral(lista_alunos):
    # Exibe todos os alunos em formato de tabela.
    print("\n  === LISTAGEM GERAL ===")

    if len(lista_alunos) == 0:
        print("  Nenhum aluno cadastrado.")
        return

    cabecalho_listagem()
    for aluno in lista_alunos:
        exibir_linha_aluno(aluno)
    print()


def listagem_por_curso(lista_alunos):
    # Filtra e exibe os alunos de um curso especifico.
    print("\n  === LISTAGEM POR CURSO ===")

    curso_filtro = ler_inteiro("  Selecione o curso (1-PHP / 2-Java / 3-Python): ", [1, 2, 3])

    filtrados = []
    for aluno in lista_alunos:
        for c in aluno["cursos"]:
            if c == curso_filtro:
                filtrados.append(aluno)
                break

    if len(filtrados) == 0:
        print("  Nenhum aluno matriculado em " + NOMES_CURSOS[curso_filtro] + ".")
        return

    print("\n  Curso: " + NOMES_CURSOS[curso_filtro])
    cabecalho_listagem()
    for aluno in filtrados:
        exibir_linha_aluno(aluno)
    print()


def listagem_por_sexo(lista_alunos):
    # Filtra e exibe os alunos pelo sexo selecionado.
    print("\n  === LISTAGEM POR SEXO ===")

    sexo_filtro = ler_inteiro("  Selecione o sexo (1-Feminino / 2-Masculino): ", [1, 2])
    rotulo      = NOMES_SEXO[sexo_filtro]

    filtrados = []
    for aluno in lista_alunos:
        if aluno["sexo"] == sexo_filtro:
            filtrados.append(aluno)

    if len(filtrados) == 0:
        print("  Nenhum aluno do sexo " + rotulo + " encontrado.")
        return

    print("\n  Sexo: " + rotulo)
    cabecalho_listagem()
    for aluno in filtrados:
        exibir_linha_aluno(aluno)
    print()


def exibir_menu():
    # Mostra as opcoes do sistema para o usuario.
    print("\n" + "=" * 40)
    print("           TI CURSOS")
    print("=" * 40)
    print("  1 - Cadastrar Aluno")
    print("  2 - Editar Aluno")
    print("  3 - Remover Aluno")
    print("  4 - Listagem Geral")
    print("  5 - Listagem por Curso")
    print("  6 - Listagem por Sexo")
    print("  0 - Sair")
    print("=" * 40)


def main():
    # Carrega os dados e entra no loop principal do menu.
    lista_alunos = carregar_alunos()

    while True:
        exibir_menu()
        opcao = input("  Opcao: ").strip()

        if opcao == "1":
            cadastrar_aluno(lista_alunos)
        elif opcao == "2":
            editar_aluno(lista_alunos)
        elif opcao == "3":
            remover_aluno(lista_alunos)
        elif opcao == "4":
            listagem_geral(lista_alunos)
        elif opcao == "5":
            listagem_por_curso(lista_alunos)
        elif opcao == "6":
            listagem_por_sexo(lista_alunos)
        elif opcao == "0":
            print("\n  Encerrando o sistema. Ate logo!")
            break
        else:
            print("  Opcao invalida. Tente novamente.")

        if opcao != "0":
            input("\n  Tecle Enter para voltar ao menu...")
            
# Ponto de entrada do programa
if __name__ == "__main__":
    main()

# Sistema Acadêmico de Gestão de Matrículas para Cursos de Tecnologia

## Descrição

Sistema desenvolvido em Python para gerenciamento de alunos matriculados em cursos de tecnologia.

O sistema permite cadastro, edição, remoção e consulta de alunos, além do cálculo automático das mensalidades conforme regras de negócio estabelecidas.

Os dados são persistidos em arquivo texto, garantindo armazenamento simples e recuperação das informações entre execuções.

---

## Funcionalidades

* Cadastro de alunos
* Edição de alunos
* Remoção de alunos
* Geração automática de matrícula
* Controle de cursos e turnos
* Cálculo automático de mensalidades
* Aplicação de descontos
* Listagem geral
* Listagem por curso
* Listagem por sexo
* Persistência em arquivo TXT
* Tratamento de erros
* Validações de entrada

---

## Regras de Negócio

### Limite de Cursos

Cada aluno pode possuir no máximo 2 cursos.

### Restrições de Turno

Não é permitido que dois cursos sejam cadastrados no mesmo turno para o mesmo aluno.

### Cursos Duplicados

Não é permitido cadastrar o mesmo curso mais de uma vez.

### Cálculo da Mensalidade

A mensalidade é calculada pela soma dos cursos escolhidos.

### Descontos

* 30% para alunos matriculados em mais de um curso.
* 15% para alunos com mais de 45 anos matriculados em apenas um curso.

### Matrícula

Gerada automaticamente a partir da última matrícula existente.

---

## Tecnologias Utilizadas

* Python 3
* Manipulação de arquivos TXT
* Programação Estruturada

---

## Como Executar

```bash
python gestao-alunos.py
```

---

## Estrutura do Projeto

README.md → documentação principal

gestao-alunos.py → sistema principal

alunos.txt → armazenamento dos dados

.gitignore → exclusão de arquivos temporários

---

## Exemplo de Uso

Cadastro:

Nome: Maria Silva

Sexo: Feminino

Idade: 25

Curso: Python

Turno: Noite

Resultado:

Matrícula: 1001

Mensalidade: R$ 310,00

---

## Tratamento de Erros

O sistema valida:

* Nome inválido
* Idade inválida
* Matrícula inexistente
* Curso duplicado
* Turno duplicado
* Entradas não numéricas
* Arquivo inexistente

---

## Melhorias Futuras

* Banco de dados SQLite
* Interface gráfica
* API REST
* Exportação PDF
* Exportação Excel
* Login de usuários
* Dashboard administrativo

---

## Autor(es)

Rafael Henrique Ferreira D' castro

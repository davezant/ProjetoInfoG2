# LU Estilo

Projeto desenvolvido especialmente para a **Lu Estilo**, uma empresa de confecção que busca automatizar e facilitar seus processos por meio de uma API moderna e flexível.

## Descrição

Este projeto apresenta uma API robusta, desenvolvida em Python, com foco em atender as demandas do setor de confecção da Lu Estilo. O sistema foi pensado para integrar facilmente com sistemas internos, validar informações de clientes (como CPF), gerenciar usuários e permitir expansão por meio de plugins, promovendo agilidade e inovação no dia a dia da empresa.

> **Compatibilidade:**  
> Este programa é compatível com plugins, permitindo a extensão de suas funcionalidades conforme a necessidade da empresa.

---

## Funcionalidades

- **Validação de CPF:** Função robusta para validar CPFs brasileiros.
- **Criação e Gerenciamento de Usuários:** Criação de usuários com verificação automática de CPF.
- **Testes Automatizados:** Testes unitários para garantir a integridade da validação e das regras de negócio.
- **Integração com PostgreSQL:** Scripts para criação de tabelas e configuração do banco de dados.
- **Scripts Úteis:** Automatização de tarefas comuns de setup.

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/davezant/ProjetoInfoG2.git
   cd ProjetoInfoG2
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Modifique a url do Banco de Dados:**
   ```bash
   echo "DATABASE_URL="postgresql://USARIO:SENHA@.../DATABASE"" > ./specs.env
    
   ```
4. **Configure o Banco de Dados**
   ```bash
   psql -U USUARIO -d DATABASE -f create_tables.sql      
   ```

---

## Configuração do Banco de Dados

É necessário possuir uma instância do PostgreSQL em funcionamento.  
Você pode definir a URL do banco de dados alterando o valor da variável `DATABASE_URL` no arquivo `specs.env`, por exemplo:

```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

---

## Criação das Tabelas

Antes de rodar a aplicação, crie as tabelas necessárias no banco PostgreSQL executando o seguinte comando:

```bash
psql -h <host> -p <porta> -U <usuario> -d <nome_do_banco> -f create_tables.sql
```

Certifique-se de que o arquivo `create_tables.sql` está presente na raiz do projeto.

---

## Testes

Para rodar os testes automatizados, execute:+

```bash
pytest
```

Os testes abrangem casos de CPF válido, inválido e duplicado.

---
## Estrutua

- `tests/` — Testes automatizados.
- `requirements.txt` — Dependências do projeto.
- `create_tables.sql` — SQL para criação das tabelas no PostgreSQL, execute o script para a Tables serem adicionadas.
- `specs.env` — Arquivo para definição da variável `DATABASE_URL`.

---

## Observações

- Utilize o PostgreSQL como banco de dados.
- A variável `DATABASE_URL` deve ser alterada em `specs.env` conforme a configuração do seu ambiente.
- Execute os scripts de criação de tabelas antes de iniciar o uso da aplicação.

---

## Autor

Projeto desenvolvido por [davezant](https://github.com/davezant).

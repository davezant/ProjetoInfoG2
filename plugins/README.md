# Sistema de Plugins

O diretório `plugins` contém módulos que estendem as funcionalidades principais do ProjetoInfoG2. O sistema de plugins foi projetado para ser simples, flexível e facilmente expansível, permitindo que qualquer pessoa adicione novas funcionalidades ao projeto sem modificar o núcleo da aplicação.

---

## Como funciona o sistema de plugins?

- **Detecção automática:** Todos os arquivos `.py` presentes neste diretório são carregados automaticamente quando a aplicação é iniciada, desde que estejam devidamente estruturados.
- **Estrutura padrão:** Cada plugin deve definir, no mínimo, uma função chamada `register_plugin(app)` (ou semelhante, conforme especificação do projeto principal). Essa função é chamada durante a inicialização para integrar o plugin ao sistema.
- **Compatibilidade:** Os plugins podem adicionar rotas, comandos, validações extras ou integrações externas, de acordo com a necessidade.
- **Isolamento:** Cada plugin é independente e pode possuir suas próprias dependências, desde que estejam listadas nos requisitos do projeto.

---

## Exemplo de plugin básico

```python
# plugins/exemplo_plugin.py

def register_plugin(app):
    @app.route("/plugin-exemplo")
    def plugin_exemplo():
        return {"mensagem": "Este endpoint veio de um plugin!"}
```

---

## Como criar um novo plugin

1. Crie um novo arquivo Python em `plugins/`, por exemplo, `meu_plugin.py`.
2. Implemente a função `register_plugin(app)` no seu arquivo.
3. (Opcional) Adicione instruções ao README do plugin, se necessário.
4. Certifique-se de que qualquer dependência extra do seu plugin está listada no `requirements.txt` do projeto principal.

---

## Observações

- Plugins mal estruturados podem causar erros na inicialização do sistema.
- Mantenha o padrão de implementação para garantir a compatibilidade.
- É recomendável documentar cada plugin criado, explicando sua função e comportamento esperado.

---


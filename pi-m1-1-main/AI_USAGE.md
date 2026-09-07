## Declaração de IA

**Ferramenta:** Chat GPT

**Finalidade:** Suporte na sintaxe do python, na estruturação dos testes e na validação de erros.

**Partes Afetadas:** __main__.py e test_pdi_lab.py

**Forma de Validação:** Executar comandos no terminal verificando se retornam 0 e executar os testes com pytest.

**Modificações Realizadas:** Correções pontuais de sintaxe no geral e estruturação de test_pdi_lab no padrão recomendado.

**Registro:** 

    Pergunta: Como usar condicional de if em python?
    Orientação: Em Python, utilizam-se os blocos `if`, `elif` e `else` estruturados por indentação (4 espaços), comparando textos com `==` e valores numéricos com operadores padrão (`<`, `>`, `==`).
    Uso: Aplicado em todo o __main__.py quando necessário o uso de condicionais.
    
    Pergunta: Como eu posso usar pytest para implementar testes sobre o que eu implementei?
    Orientação: Para testar a aplicação com o pytest, crie funções iniciadas com test_ no arquivo tests/test_pdi_lab.py e utilize a instrução assert para validar duas abordagens: testes unitários diretos das funções de imagem e testes de integração/linha de comando (CLI).
    Uso: Estruturação de testes em test_pdi_lab.py.

    Pergunta: Como posso validar erros ou falhas?
    Orientação: Verificar se a imagem carregada não é nula (`None`) e testar se os argumentos da CLI atendem aos pré-requisitos (ex.: `--levels >= 2`). Em caso de falha, exibir mensagem explicativa e encerrar a execução na `main()` retornando o código de erro `sys.exit(1)`.
    Uso: Aplicado em __main__.py para garantir que os resultados saiam como esperado.

    Pergunta: Como usar parâmetros passados em comandos?
    Orientação: Utilizar a biblioteca nativa `argparse` configurando um `ArgumentParser` com o método `add_argument()` para definir cada parâmetro. Após o parsing com `parse_args()`, os valores são acessados diretamente como atributos do objeto retornado (ex.: `args.input`, `args.operation`).
    Uso: Direcionamento implementado no main() de __main__.py

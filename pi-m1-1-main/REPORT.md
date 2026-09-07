Aluno 1: Cassiano Soares da Silveira

Aluno 2: Pedro Henrique Silva Coelho

**Objetivo**

Implementar manualmente operações de manipulação e representação de imagens digitais por meio do percurso e acesso direto aos pixels. O foco do laboratório é relacionar conceitos de dimensões, canais de cor, intensidade e resolução com funções manuais.

**Operações Implementadas**

`inspect`: Inspeção da imagem

`copy`: Cópia manual da imagem

`channel_b`, `channel_g` e `channel_r`: Separação manual dos canais

`grayscale_average`: Conversão manual para níveis de cinza por média simples

`grayscale_weighted`: Conversão manual para níveis de cinza por média ponderada

`quantize`: Quantização da imagem em diferentes níveis

**Testes**

`testeSintetico`: Utiliza matriz de imagem artificial de 2x2 pixels e 3 canais de cor em formato uint8 para validar se funções estão funcionando corretamente.

`testeNiveis`: Valida se ao passar --levels 1 é interrompida a execução com código de erro diferente de zero.

`testeImagemNone`: Valida se ao ler uma imagem inexistente a aplicação encerra retornando código de erro.


**Resultados**

Ao rodar os comandos referentes as operações de pdi_lab.py é possível notar que as imagens são geradas corretamente em images/output.

Testes de test_pdi_lab.py passaram normalmente. 

**Análise Técnica**

As imagens com escala cinza possuem um canal e utilizam coordenadas bidimensionais, enquanto as coloridas tridimensionais, pois possuem 3 canais, para cada índice de cor. 

A imagem gerada por grayscale_weighted demonstra ser mais natural que a gerada por grayscale_average, e isso se deve por conta da distribuição dos pesos por canal. 
A média ponderada distribui de acordo com a fórmula de iluminãncia perceptiva do olho humano enquanto a média simples da peso igual a todos os canais.

Ao analisar as imagens entre os níveis de quantização de 16 até 2 percebe-se que quanto menor o nível mais informação a imagem perde, com o aumento de uma espécie de contorno em alguns espaços que vai ficando cada vez maior.

**Limitações**

Por realizar as transformações manualmente pela matriz a implementação não tem um desempenho tão alto quanto teria se usasse funções vetorizadas de numpy e opencv.

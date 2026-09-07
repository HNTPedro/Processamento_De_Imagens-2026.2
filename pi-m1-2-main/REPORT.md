# Relatório Técnico — M1.2 Transformações de Intensidade

**Estudante:** Pedro Henrique Silva Coelho
**Linguagem:** Python

---

## 1. Objetivo
Implementar e avaliar transformações pontuais de intensidade em imagens em níveis de cinza (brilho, contraste, negativo e limiarização) e a geração manual de histogramas, operando diretamente sobre os pixels.

---

## 2. Análise Técnica dos Resultados

### Q1. Qual é a diferença observada entre alteração de brilho e alteração de contraste?
* **Brilho:** Aplica uma translação aditiva constante ($g = f + b$). Todos os pixels da imagem são deslocados de forma rígida pela mesma quantidade na escala de cinza.
* **Contraste:** Aplica uma mudança de escala multiplicativa centrada no nível médio 128 ($g = \alpha(f - 128) + 128$). A amplitude da distribuição de intensidades expande ($\alpha > 1$) ou contrai ($\alpha < 1$).

### Q2. Em quais testes ocorreu saturação e qual foi seu efeito?
* **Ajuste de Brilho Positivo ($b > 0$) e Ampliação de Contraste ($\alpha > 1.5$):** Ocasionaram saturação superior no limite 255.
* **Ajuste de Brilho Negativo ($b < 0$):** Ocasionou saturação inferior no limite 0.
* **Efeito:** Perda irrecuperável de detalhes nas áreas atingidas, pois múltiplos tons distintos de entrada foram mapeados para o mesmo valor estourado ($0$ ou $255$).

### Q3. Como o histograma se deslocou após alterar o brilho?
O formato da distribuição do histograma permaneceu inalterado, porém deslocou-se rigidamente para a direita ($b > 0$) ou para a esquerda ($b < 0$). Os picos que ultrapassaram $0$ ou $255$ acumularam-se nessas extremidades devido ao *clamping*.

### Q4. Como a distribuição das intensidades mudou ao alterar o contraste?
* **$\alpha < 1.0$ (Redução):** O histograma encolheu em direção ao centro ($128$), reduzindo o desvio padrão da distribuição.
* **$\alpha > 1.0$ (Ampliação):** As barras do histograma se afundaram e se espalharam em direção às extremidades ($0$ e $255$), aumentando a dispersão das intensidades.

### Q5. Que informação é perdida após a limiarização?
Perde-se toda a variação contínua de níveis de cinza e a textura interna das regiões. A imagem é reduzida a uma representação estritamente binária (0 ou 255), restando apenas a separação geométrica entre fundo e primeiro plano.

---

## 3. Limitações
A implementação manual em Python com loops explícitos aninhados atende ao requisito pedagógico e rigor técnico de M1, porém apresenta menor desempenho em imagens de altíssima resolução se comparada a implementações nativas em C++ ou vetorizadas.
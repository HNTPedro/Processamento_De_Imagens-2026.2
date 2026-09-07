# Relatório Técnico — M1.3 Convolução e Filtragem Espacial

**Estudante:** Pedro Henrique Silva Coelho
**Linguagem:** Python 3.12  
**Ambiente:** Windows (MSYS2 — Terminal UCRT64 / VS Code)

---

## 1. Objetivo

Implementar manualmente a convolução bidimensional genérica no domínio espacial, o tratamento de bordas (`copy` e `replicate`), filtros de suavização, realce via Laplaciano e detecção de bordas via operador de Sobel, sem o uso de funções prontas de filtragem espacial.

---

## 2. Análise e Respostas às Questões Técnicas

### Q1. Qual é a diferença entre uma operação pontual e uma operação de vizinhança?
* **Operação Pontual (ex: M1.2):** O valor de saída do pixel $g(x,y)$ depende exclusivamente e isoladamente do valor do pixel de entrada $f(x,y)$ na mesma coordenada.
* **Operação de Vizinhança (ex: M1.3):** O valor do pixel de saída $g(x,y)$ depende do valor do pixel original $f(x,y)$ e dos pixels contíguos ao seu redor contidos dentro da janela definida pelo kernel (ex: $3 \times 3$, $5 \times 5$).

---

### Q2. Por que kernels normalmente possuem dimensões ímpares?
Kernels possuem dimensões ímpares ($3 \times 3$, $5 \times 5$, $7 \times 7$) para garantir a existência de um **pixel central bem-definido e simétrico** em coordenadas inteiras:

$$
\text{centro} = \left(\left\lfloor\frac{N}{2}\right\rfloor, \left\lfloor\frac{N}{2}\right\rfloor\right)
$$

Em kernels de tamanho par (ex: $2 \times 2$ ou $4 \times 4$), o centro ficaria situado entre pixels, o que causaria um deslocamento geométrico (phase shift) na imagem filtrada.

---

### Q3. Qual é o efeito de aumentar o tamanho do kernel de média?
Aumentar o tamanho da janela (ex: de $3 \times 3$ para $5 \times 5$):
* **Suavização e Ruído:** Intensifica o desfoque (*blurring*) e reduz ruídos de alta frequência com maior força.
* **Perda de Detalhes:** Atenua transições bruscas, borrando e atenuando contornos e texturas finas.
* **Custo Computacional:** Aumenta a complexidade de cálculo por pixel de $\mathcal{O}(3^2)$ para $\mathcal{O}(5^2)$ operações de multiplicação e adição.

---

### Q4. Como a estratégia de tratamento de bordas interfere no resultado?
Pixels situados nas margens da imagem não possuem vizinhança completa para cobrir o kernel:
* **Estratégia `copy`:** Ignora o processamento do kernel nessas regiões e preserva o pixel de entrada original, gerando uma moldura ao redor do resultado que não foi filtrada.
* **Estratégia `replicate`:** Projeta o pixel válido mais próximo para preencher as posições fora do limite, mantendo a continuidade do filtro sem introduzir artefatos escuros ou descontinuidades nas margens.

---

### Q5. Por que a resposta bruta do Laplaciano pode conter valores negativos?
O operador Laplaciano mede a segunda derivada espacial da imagem ($\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$). 
Em regiões de transição de intensidade (degraus):
* No lado mais claro da borda, a curvatura é negativa.
* No lado mais escuro da borda, a curvatura é positiva.

Como o kernel contém pesos negativos no centro (ex: $-4$), a soma ponderada resulta em valores negativos para regiões claras adjacentes a bordas. Esses valores devem ser mantidos em tipos de ponto flutuante (`float`) antes de serem saturados para exibição.

---

### Q6. Qual é a diferença entre $G_x$ e $G_y$ no Sobel?
* **$G_x$ (Gradiente Horizontal):** Destaca variações de intensidade ao longo do eixo horizontal (detecta **bordas verticais**).
* **$G_y$ (Gradiente Vertical):** Destaca variações de intensidade ao longo do eixo vertical (detecta **bordas horizontais**).

---

### Q7. Que diferenças são observadas entre $|G_x| + |G_y|$ e $\sqrt{G_x^2 + G_y^2}$?
* **Magnitude Aproximada ($|G_x| + |G_y|$):** Computacionalmente mais leve por evitar o cálculo da raiz quadrada e potenciação. Porém, é uma aproximação anistrópica que superestima certas direções diagonais.
* **Magnitude Euclidiana ($\sqrt{G_x^2 + G_y^2}$):** Fornece o módulo real do vetor gradiente de forma isotopicamente invariante à rotação, produzindo contornos mais suaves e precisos independentemente da orientação da borda.

---

## 3. Testes Sintéticos e Validação

Os testes automatizados em `tests/test_pdi_lab.py` validaram:
1. **Preservação por Identidade:** Matrizes filtradas pelo kernel $3 \times 3$ identidade retornaram exatamente a mesma entrada.
2. **Espalhamento do Impulso:** Matriz com ponto isolado $9$ propagou o valor de $1.0$ por toda a vizinhança no filtro de média $3 \times 3$.
3. **Respostas a Degraus no Sobel:** Matriz com variação em coluna registrou resposta nula em $G_y$ e magnitude máxima em $G_x$.

---

## 4. Limitações

A implementação manual foi realizada com loops aninhados em Python. Para imagens com resolução superior a Full HD, o tempo de execução é maior se comparado a linguagens compiladas (C++) ou primitivas vetorizadas em C (NumPy/OpenCV).
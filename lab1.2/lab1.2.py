from PIL import Image
import os
import math


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "saida"
PASTA_HIST = "histogramas"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def criar_pastas():
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_HIST, exist_ok=True)


def limitar_255(valor):
    """
    Limita manualmente um valor ao intervalo [0, 255].
    """
    if valor < 0:
        return 0

    if valor > 255:
        return 255

    return valor


def arredondar(valor):
    """
    Arredondamento manual para o inteiro mais próximo.
    """
    if valor >= 0:
        return int(math.floor(valor + 0.5))

    return int(math.ceil(valor - 0.5))


def verificar_imagem(imagem):
    """
    As operações deste laboratório trabalham com imagens
    de 8 bits em níveis de cinza.
    """
    if imagem is None:
        raise ValueError("Imagem inválida.")

    if imagem.mode != "L":
        raise ValueError(
            "Imagem incompatível: a imagem deve estar no modo L "
            "(níveis de cinza, 8 bits)."
        )


def carregar_imagem(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"Falha na leitura: arquivo não encontrado: {caminho}"
        )

    try:
        imagem = Image.open(caminho)
        imagem.load()
    except Exception as erro:
        raise ValueError(
            f"Falha na leitura da imagem: {erro}"
        )

    verificar_imagem(imagem)

    return imagem


def salvar_imagem(imagem, caminho):
    try:
        imagem.save(caminho)
    except Exception as erro:
        raise IOError(
            f"Falha ao salvar imagem {caminho}: {erro}"
        )


# ============================================================
# 1. AJUSTE DE BRILHO
# ============================================================

def ajustar_brilho(imagem, b):
    """
    g(x,y) = f(x,y) + b

    Cada pixel de saída depende somente do pixel correspondente
    da imagem de entrada.

    O resultado é limitado manualmente a [0, 255].
    """

    verificar_imagem(imagem)

    if not isinstance(b, (int, float)):
        raise ValueError("O parâmetro de brilho deve ser numérico.")

    largura, altura = imagem.size

    saida = Image.new("L", (largura, altura))

    entrada_pixels = imagem.load()
    saida_pixels = saida.load()

    for y in range(altura):
        for x in range(largura):
            valor = entrada_pixels[x, y]

            novo_valor = valor + b

            novo_valor = limitar_255(novo_valor)
            novo_valor = arredondar(novo_valor)

            saida_pixels[x, y] = novo_valor

    return saida


# ============================================================
# 2. AJUSTE DE CONTRASTE
# ============================================================

def ajustar_contraste(imagem, alpha):
    """
    g(x,y) = alpha * (f(x,y) - 128) + 128
    """

    verificar_imagem(imagem)

    if not isinstance(alpha, (int, float)):
        raise ValueError("Alpha deve ser numérico.")

    if alpha < 0:
        raise ValueError(
            "Alpha inválido. Para este laboratório, alpha deve ser >= 0."
        )

    largura, altura = imagem.size

    saida = Image.new("L", (largura, altura))

    entrada_pixels = imagem.load()
    saida_pixels = saida.load()

    for y in range(altura):
        for x in range(largura):
            valor = entrada_pixels[x, y]

            novo_valor = alpha * (valor - 128) + 128

            novo_valor = limitar_255(novo_valor)
            novo_valor = arredondar(novo_valor)

            saida_pixels[x, y] = novo_valor

    return saida


# ============================================================
# 3. NEGATIVO
# ============================================================

def negativo(imagem):
    """
    g(x,y) = 255 - f(x,y)
    """

    verificar_imagem(imagem)

    largura, altura = imagem.size

    saida = Image.new("L", (largura, altura))

    entrada_pixels = imagem.load()
    saida_pixels = saida.load()

    for y in range(altura):
        for x in range(largura):
            valor = entrada_pixels[x, y]

            novo_valor = 255 - valor

            saida_pixels[x, y] = novo_valor

    return saida


# ============================================================
# 4. LIMIARIZAÇÃO BINÁRIA
# ============================================================

def limiarizacao(imagem, T):
    """
    g(x,y) =
        0,   se f(x,y) < T
        255, se f(x,y) >= T
    """

    verificar_imagem(imagem)

    if not isinstance(T, int):
        raise ValueError("O limiar T deve ser um número inteiro.")

    if T < 0 or T > 255:
        raise ValueError(
            "Limiar inválido. T deve estar entre 0 e 255."
        )

    largura, altura = imagem.size

    saida = Image.new("L", (largura, altura))

    entrada_pixels = imagem.load()
    saida_pixels = saida.load()

    for y in range(altura):
        for x in range(largura):
            valor = entrada_pixels[x, y]

            if valor < T:
                saida_pixels[x, y] = 0
            else:
                saida_pixels[x, y] = 255

    return saida


# ============================================================
# 5. HISTOGRAMA MANUAL
# ============================================================

def calcular_histograma(imagem):
    """
    Cria manualmente um vetor com 256 posições.

    histograma[i] = quantidade de pixels com intensidade i.
    """

    verificar_imagem(imagem)

    histograma = [0] * 256

    largura, altura = imagem.size
    pixels = imagem.load()

    for y in range(altura):
        for x in range(largura):
            intensidade = pixels[x, y]

            if intensidade < 0 or intensidade > 255:
                raise ValueError(
                    f"Intensidade inválida encontrada: {intensidade}"
                )

            histograma[intensidade] += 1

    return histograma


def salvar_histograma_csv(histograma, caminho):
    if len(histograma) != 256:
        raise ValueError(
            "O histograma deve possuir exatamente 256 posições."
        )

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("intensidade,quantidade\n")

        for intensidade in range(256):
            quantidade = histograma[intensidade]

            arquivo.write(
                f"{intensidade},{quantidade}\n"
            )


# ============================================================
# IMAGEM SINTÉTICA
# ============================================================

def criar_imagem_sintetica():
    """
    Cria uma imagem 8x8 contendo intensidades conhecidas.
    Ela serve para conferência manual dos resultados.
    """

    valores = [
        [0, 32, 64, 96, 128, 160, 192, 255],
        [0, 32, 64, 96, 128, 160, 192, 255],
        [10, 50, 80, 100, 120, 140, 200, 240],
        [10, 50, 80, 100, 120, 140, 200, 240],
        [20, 40, 60, 80, 100, 120, 140, 160],
        [30, 60, 90, 120, 150, 180, 210, 240],
        [5, 70, 135, 145, 180, 220, 250, 255],
        [15, 75, 125, 175, 200, 225, 245, 255],
    ]

    altura = len(valores)
    largura = len(valores[0])

    imagem = Image.new("L", (largura, altura))
    pixels = imagem.load()

    for y in range(altura):
        for x in range(largura):
            pixels[x, y] = valores[y][x]

    return imagem


# ============================================================
# TESTES MANUAIS
# ============================================================

def testar_imagem_sintetica():
    print("\n=== TESTES DA IMAGEM SINTÉTICA ===")

    imagem = criar_imagem_sintetica()

    # --------------------------------------------------------
    # Brilho
    # --------------------------------------------------------

    brilho_negativo = ajustar_brilho(imagem, -60)
    brilho_positivo = ajustar_brilho(imagem, 60)

    assert brilho_negativo.getpixel((0, 0)) == 0
    assert brilho_negativo.getpixel((4, 0)) == 68

    assert brilho_positivo.getpixel((0, 0)) == 60
    assert brilho_positivo.getpixel((7, 0)) == 255

    print("Brilho negativo: OK")
    print("Brilho positivo: OK")
    print("Saturação do brilho: OK")

    # --------------------------------------------------------
    # Contraste
    # --------------------------------------------------------

    contraste_05 = ajustar_contraste(imagem, 0.5)
    contraste_10 = ajustar_contraste(imagem, 1.0)
    contraste_15 = ajustar_contraste(imagem, 1.5)

    # Para 128, o valor permanece 128
    assert contraste_05.getpixel((4, 0)) == 128
    assert contraste_10.getpixel((4, 0)) == 128
    assert contraste_15.getpixel((4, 0)) == 128

    # alpha = 1 deve reproduzir a imagem original
    for y in range(imagem.height):
        for x in range(imagem.width):
            assert contraste_10.getpixel((x, y)) == imagem.getpixel((x, y))

    print("Contraste alpha=0.5: OK")
    print("Contraste alpha=1.0: OK")
    print("Contraste alpha=1.5: OK")

    # --------------------------------------------------------
    # Negativo
    # --------------------------------------------------------

    imagem_negativa = negativo(imagem)

    assert imagem_negativa.getpixel((0, 0)) == 255
    assert imagem_negativa.getpixel((7, 0)) == 0

    print("Negativo: OK")

    # --------------------------------------------------------
    # Limiarização
    # --------------------------------------------------------

    limiar_100 = limiarizacao(imagem, 100)
    limiar_180 = limiarizacao(imagem, 180)

    assert limiar_100.getpixel((0, 0)) == 0
    assert limiar_100.getpixel((4, 0)) == 255

    assert limiar_180.getpixel((4, 0)) == 0
    assert limiar_180.getpixel((6, 0)) == 255

    print("Limiar T=100: OK")
    print("Limiar T=180: OK")

    # --------------------------------------------------------
    # Histograma
    # --------------------------------------------------------

    hist = calcular_histograma(imagem)

    total = 0

    for intensidade in range(256):
        total += hist[intensidade]

    assert total == imagem.width * imagem.height

    print("Histograma manual: OK")
    print("Total de pixels no histograma:", total)

    print("Todos os testes sintéticos passaram.")


# ============================================================
# PROCESSAMENTO DA IMAGEM REAL
# ============================================================

def processar_imagem(caminho):
    print("\n============================================")
    print("PROCESSAMENTO DA IMAGEM")
    print("============================================")

    imagem = carregar_imagem(caminho)

    nome_base = os.path.splitext(
        os.path.basename(caminho)
    )[0]

    print("Imagem:", caminho)
    print("Tamanho:", imagem.size)
    print("Modo:", imagem.mode)

    # --------------------------------------------------------
    # Histograma original
    # --------------------------------------------------------

    hist_original = calcular_histograma(imagem)

    salvar_histograma_csv(
        hist_original,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_original.csv"
        )
    )

    # --------------------------------------------------------
    # 1. Brilho negativo
    # --------------------------------------------------------

    img_brilho_neg = ajustar_brilho(imagem, -60)

    caminho_saida = os.path.join(
        PASTA_SAIDA,
        f"{nome_base}_brilho_menos_60.png"
    )

    salvar_imagem(img_brilho_neg, caminho_saida)

    hist = calcular_histograma(img_brilho_neg)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_brilho_menos_60.csv"
        )
    )

    # --------------------------------------------------------
    # 1. Brilho positivo
    # --------------------------------------------------------

    img_brilho_pos = ajustar_brilho(imagem, 60)

    caminho_saida = os.path.join(
        PASTA_SAIDA,
        f"{nome_base}_brilho_mais_60.png"
    )

    salvar_imagem(img_brilho_pos, caminho_saida)

    hist = calcular_histograma(img_brilho_pos)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_brilho_mais_60.csv"
        )
    )

    # --------------------------------------------------------
    # 2. Contraste alpha = 0.5
    # --------------------------------------------------------

    img_contraste_05 = ajustar_contraste(imagem, 0.5)

    salvar_imagem(
        img_contraste_05,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_contraste_05.png"
        )
    )

    # --------------------------------------------------------
    # 2. Contraste alpha = 1.0
    # --------------------------------------------------------

    img_contraste_10 = ajustar_contraste(imagem, 1.0)

    salvar_imagem(
        img_contraste_10,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_contraste_10.png"
        )
    )

    # --------------------------------------------------------
    # 2. Contraste alpha = 1.5
    # --------------------------------------------------------

    img_contraste_15 = ajustar_contraste(imagem, 1.5)

    salvar_imagem(
        img_contraste_15,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_contraste_15.png"
        )
    )

    hist = calcular_histograma(img_contraste_15)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_contraste_15.csv"
        )
    )

    # --------------------------------------------------------
    # 3. Negativo
    # --------------------------------------------------------

    img_negativo = negativo(imagem)

    salvar_imagem(
        img_negativo,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_negativo.png"
        )
    )

    hist = calcular_histograma(img_negativo)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_negativo.csv"
        )
    )

    # --------------------------------------------------------
    # 4. Limiar T = 100
    # --------------------------------------------------------

    img_limiar_100 = limiarizacao(imagem, 100)

    salvar_imagem(
        img_limiar_100,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_limiar_100.png"
        )
    )

    hist = calcular_histograma(img_limiar_100)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_limiar_100.csv"
        )
    )

    # --------------------------------------------------------
    # 4. Limiar T = 180
    # --------------------------------------------------------

    img_limiar_180 = limiarizacao(imagem, 180)

    salvar_imagem(
        img_limiar_180,
        os.path.join(
            PASTA_SAIDA,
            f"{nome_base}_limiar_180.png"
        )
    )

    hist = calcular_histograma(img_limiar_180)

    salvar_histograma_csv(
        hist,
        os.path.join(
            PASTA_HIST,
            f"{nome_base}_limiar_180.csv"
        )
    )

    print("\nProcessamento concluído.")
    print("Imagens salvas em:", PASTA_SAIDA)
    print("Histogramas salvos em:", PASTA_HIST)


# ============================================================
# MAIN
# ============================================================

def main():
    criar_pastas()

    # Testes obrigatórios com imagem sintética
    testar_imagem_sintetica()

    # Salva a imagem sintética para inspeção visual
    imagem_sintetica = criar_imagem_sintetica()

    salvar_imagem(
        imagem_sintetica,
        os.path.join(
            PASTA_SAIDA,
            "sintetica.png"
        )
    )

    # Histograma da imagem sintética
    hist_sintetica = calcular_histograma(imagem_sintetica)

    salvar_histograma_csv(
        hist_sintetica,
        os.path.join(
            PASTA_HIST,
            "sintetica.csv"
        )
    )

    # Verifica se existe uma imagem real
    caminho_imagem = os.path.join(
        PASTA_ENTRADA,
        "imagem.png"
    )

    if os.path.exists(caminho_imagem):
        processar_imagem(caminho_imagem)
    else:
        print(
            "\nNenhuma imagem real encontrada."
        )
        print(
            "Coloque uma imagem em:"
        )
        print(
            "entrada/imagem.png"
        )


if __name__ == "__main__":
    main()
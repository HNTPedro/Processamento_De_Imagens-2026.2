import cv2
import numpy
import argparse
import sys

def inspect(imagem):
    if imagem is None: raise ValueError("Imagem nao carregou.")

    largura = imagem.shape[1]
    altura = imagem.shape[0]
    if len(imagem.shape) == 3: canais = imagem.shape[2]
    else: canais = 1
    tipo = imagem.dtype
    qtdPixels = largura * altura
    print(f"width={largura}")
    print(f"height={altura}")
    print(f"channels={canais}")
    print(f"pixels={qtdPixels}")
    print(f"type={tipo}")
    if canais == 1:
        valMax = int(imagem[0, 0])
        valMin = int(imagem[0, 0])
        somaPixel = 0
        for i in range(altura):
            for j in range(largura):
                px = int(imagem[i, j])
                if px > valMax: valMax = px
                if px < valMin: valMin = px
                somaPixel += px        
        mediaInt = somaPixel/qtdPixels
        print(f"min={valMin}")
        print(f"max={valMax}")
        print(f"mean={mediaInt:.2f}")

    else:
        valMax = [int(imagem[0, 0, 0]), int(imagem[0, 0, 1]), int(imagem[0, 0, 2])]
        valMin = [int(imagem[0, 0, 0]), int(imagem[0, 0, 1]), int(imagem[0, 0, 2])]
        somaPixel = [0, 0, 0]
        for i in range(altura):
            for j in range(largura):
                for k in range(canais):
                    px = int(imagem[i, j, k])
                    if px > valMax[k]: valMax[k] = px
                    if px < valMin[k]: valMin[k] = px
                    somaPixel[k] += px
        nomeCanal = ['b', 'g', 'r']
        for i in range(3):
            print(f"min_{nomeCanal[i]}={valMin[i]}")
            print(f"max_{nomeCanal[i]}={valMax[i]}")
            print(f"mean_{nomeCanal[i]}={somaPixel[i] / qtdPixels:.2f}")

def copy(imagem):
    if imagem is None: raise ValueError("Imagem nao carregou.")
    imagemNova = numpy.zeros(imagem.shape, dtype=imagem.dtype)
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    if len(imagem.shape) == 3:
        canais = imagem.shape[2]
        for i in range(altura):
            for j in range(largura):
                for k in range(canais):
                    imagemNova[i, j, k] = imagem[i, j, k]
    else:
        for i in range(altura):
            for j in range(largura):
                imagemNova[i, j] = imagem[i, j]

    return imagemNova

def channel_b(imagem):
    if imagem is None or len(imagem.shape) < 3: raise ValueError("A imagem deve ter 3 canais") 
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros(imagem.shape, dtype=imagem.dtype)
    for i in range(altura):
        for j in range(largura):
            imagemNova[i, j, 0] = imagem[i, j, 0]

    return imagemNova

def channel_g(imagem):
    if imagem is None or len(imagem.shape) < 3: raise ValueError("A imagem deve ter 3 canais")
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros(imagem.shape, dtype=imagem.dtype)
    for i in range(altura):
        for j in range(largura):
            imagemNova[i, j, 1] = imagem[i, j, 1]

    return imagemNova

def channel_r(imagem):
    if imagem is None or len(imagem.shape) < 3: raise ValueError("A imagem deve ter 3 canais")
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros(imagem.shape, dtype=imagem.dtype)
    for i in range(altura):
        for j in range(largura):
            imagemNova[i, j, 2] = imagem[i, j, 2]

    return imagemNova

def grayscale_average(imagem):
    if imagem is None or len(imagem.shape) < 3: raise ValueError("A imagem deve ter 3 canais")
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros((altura, largura), dtype=imagem.dtype)
    for i in range(altura):
        for j in range(largura):
            b = int(imagem[i, j, 0])
            g = int(imagem[i, j, 1])
            r = int(imagem[i, j, 2])
            imagemNova[i, j] = (r+g+b)//3

    return imagemNova

def grayscale_weighted(imagem):
    if imagem is None or len(imagem.shape) < 3: raise ValueError("A imagem deve ter 3 canais")
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros((altura, largura), dtype=imagem.dtype)
    for i in range(altura):
        for j in range(largura):
            b = int(imagem[i, j, 0])
            g = int(imagem[i, j, 1])
            r = int(imagem[i, j, 2])
            imagemNova[i, j] = int(0.299*r+0.587*g+0.114*b)

    return imagemNova

def quantize(imagem, niveis):
    if imagem is None: raise ValueError("Imagem nao carregou.")
    if len(imagem.shape) == 3: imagem = grayscale_weighted(imagem)
    if niveis is None or niveis<=1 or niveis>256: 
        raise ValueError("Niveis devem estar entre 2 e 256")
    largura = imagem.shape[1]
    altura = imagem.shape[0]
    imagemNova = numpy.zeros((altura, largura), dtype=imagem.dtype)
    fator = 256//niveis
    escala=255/(niveis-1)
    for i in range(altura):
        for j in range(largura):
            px = int(imagem[i, j])
            bloco = min(px//fator, niveis-1)
            imagemNova[i, j] = int(bloco*escala)
            
    return imagemNova

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=False)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--levels", type=int, required=False)
    args=parser.parse_args()
    imagem = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)
    if imagem is None: 
        print(f"Erro: Nao foi possivel ler '{args.input}'")
        sys.exit(1)
    try:
        operacao = args.operation.lower()
        if operacao == "inspect":
            inspect(imagem)
            sys.exit(0)
        if not args.output:
            print("Erro: A operacao exige --output")
            sys.exit(1)

        if operacao == "copy":
            resposta = copy(imagem)
        elif operacao == "channel_b":
            resposta = channel_b(imagem)
        elif operacao == "channel_g":
            resposta = channel_g(imagem)
        elif operacao == "channel_r":
            resposta = channel_r(imagem)
        elif operacao == "grayscale_average":
            resposta = grayscale_average(imagem)
        elif operacao == "grayscale_weighted":
            resposta = grayscale_weighted(imagem)
        elif operacao == "quantize":
            if args.levels is None:
                print("Erro: quantize exige --levels")
                sys.exit(1)
            resposta = quantize(imagem, args.levels)
        else:
            print(f"Erro: Operacao '{operacao}' invalida")
            sys.exit(1)

        cv2.imwrite(args.output, resposta)
        sys.exit(0)

    except Exception as e:
        print(f"Erro na execucao: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

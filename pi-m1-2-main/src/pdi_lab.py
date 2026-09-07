import argparse
import os
import sys
from PIL import Image

# ==========================================
# 1. FUNÇÕES DE I/O E UTILITÁRIOS
# ==========================================

def resolve_input_path(input_arg: str) -> str:
    """
    Resolve o caminho da imagem de entrada.
    Permite passar apenas o nome da imagem (ex: 'foto.png') 
    ou o caminho completo. Procurará em 'images/input/' por padrão.
    """
    if os.path.exists(input_arg):
        return input_arg
    
    # Tenta buscar dentro do diretório padrão images/input/
    default_path = os.path.join("images", "input", input_arg)
    if os.path.exists(default_path):
        return default_path

    sys.stderr.write(f"Erro: Imagem nao encontrada em '{input_arg}' nem em '{default_path}'.\n")
    sys.exit(1)


def load_image_gray(path: str) -> tuple[list[list[int]], int, int]:
    """Lê uma imagem, converte para escala de cinza e retorna (matriz, width, height)."""
    resolved_path = resolve_input_path(path)
    try:
        with Image.open(resolved_path) as img:
            img_gray = img.convert("L")
            width, height = img_gray.size
            pixels_flat = list(img_gray.getdata())

            # Converte lista plana para matriz 2D (height x width)
            matrix = [
                pixels_flat[y * width : (y + 1) * width]
                for y in range(height)
            ]
            return matrix, width, height
    except Exception as e:
        sys.stderr.write(f"Erro ao abrir imagem '{resolved_path}': {e}\n")
        sys.exit(1)


def save_image_gray(matrix: list[list[int]], path: str) -> None:
    """Salva uma matriz 2D em formato de imagem em escala de cinza."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        height = len(matrix)
        width = len(matrix[0]) if height > 0 else 0

        flat_data = bytearray()
        for y in range(height):
            for x in range(width):
                val = int(round(matrix[y][x]))
                clamped = max(0, min(255, val))
                flat_data.append(clamped)

        img = Image.frombytes("L", (width, height), bytes(flat_data))
        img.save(path)
    except Exception as e:
        sys.stderr.write(f"Erro ao salvar imagem em '{path}': {e}\n")
        sys.exit(1)


def save_histogram_csv(hist: list[int], path: str) -> None:
    """Salva o histograma em formato CSV (intensidade,quantidade)."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("intensidade,quantidade\n")
            for intensity, count in enumerate(hist):
                f.write(f"{intensity},{count}\n")
    except Exception as e:
        sys.stderr.write(f"Erro ao salvar histograma CSV em '{path}': {e}\n")
        sys.exit(1)


# ==========================================
# 2. OPERAÇÕES MANUAIS DE INTENSIDADE
# ==========================================

def clamp_pixel(value: float) -> int:
    """Garante que o valor do pixel esteja entre [0, 255]."""
    return max(0, min(255, int(round(value))))


def apply_brightness(matrix: list[list[int]], b: int) -> list[list[int]]:
    """g(x,y) = f(x,y) + b"""
    height, width = len(matrix), len(matrix[0])
    out = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            out[y][x] = clamp_pixel(matrix[y][x] + b)
    return out


def apply_contrast(matrix: list[list[int]], alpha: float) -> list[list[int]]:
    """g(x,y) = alpha * (f(x,y) - 128) + 128"""
    if alpha < 0:
        sys.stderr.write("Erro: Alpha de contraste deve ser nao-negativo.\n")
        sys.exit(1)

    height, width = len(matrix), len(matrix[0])
    out = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            val = alpha * (matrix[y][x] - 128.0) + 128.0
            out[y][x] = clamp_pixel(val)
    return out


def apply_negative(matrix: list[list[int]]) -> list[list[int]]:
    """g(x,y) = 255 - f(x,y)"""
    height, width = len(matrix), len(matrix[0])
    out = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            out[y][x] = 255 - matrix[y][x]
    return out


def apply_threshold(matrix: list[list[int]], t: int) -> list[list[int]]:
    """Limiarizacao binaria."""
    if not (0 <= t <= 255):
        sys.stderr.write(f"Erro: Limiar T ({t}) deve estar entre 0 e 255.\n")
        sys.exit(1)

    height, width = len(matrix), len(matrix[0])
    out = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            out[y][x] = 255 if matrix[y][x] >= t else 0
    return out


def calculate_histogram(matrix: list[list[int]]) -> list[int]:
    """Calcula manualmente o histograma de 256 posicoes."""
    hist = [0] * 256
    height, width = len(matrix), len(matrix[0])
    for y in range(height):
        for x in range(width):
            val = clamp_pixel(matrix[y][x])
            hist[val] += 1
    return hist


# ==========================================
# 3. INTERFACE DE LINHA DE COMANDO (CLI)
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="PDI Lab M1.2 - Transformacoes de Intensidade")

    parser.add_argument(
        "--input", required=True, 
        help="Nome da imagem na pasta input (ex: foto.png) ou caminho completo."
    )
    parser.add_argument(
        "--output", required=True, 
        help="Caminho do arquivo de saída (imagem ou CSV)."
    )
    parser.add_argument(
        "--operation", required=True,
        choices=["brightness", "contrast", "negative", "threshold", "histogram"],
        help="Operação solicitada"
    )
    parser.add_argument("--value", type=int, default=None, help="Valor de brilho (b)")
    parser.add_argument("--alpha", type=float, default=None, help="Valor de contraste (alpha)")
    parser.add_argument("--threshold", type=int, default=None, help="Valor de limiar (T)")

    args = parser.parse_args()

    # Carrega imagem resolvendo a busca dentro da pasta de input
    matrix, _, _ = load_image_gray(args.input)
    op = args.operation

    if op == "brightness":
        if args.value is None:
            sys.stderr.write("Erro: Parâmetro --value é obrigatório para brilho.\n")
            sys.exit(1)
        res = apply_brightness(matrix, args.value)
        save_image_gray(res, args.output)

    elif op == "contrast":
        if args.alpha is None:
            sys.stderr.write("Erro: Parâmetro --alpha é obrigatório para contraste.\n")
            sys.exit(1)
        res = apply_contrast(matrix, args.alpha)
        save_image_gray(res, args.output)

    elif op == "negative":
        res = apply_negative(matrix)
        save_image_gray(res, args.output)

    elif op == "threshold":
        if args.threshold is None:
            sys.stderr.write("Erro: Parâmetro --threshold é obrigatório para limiarização.\n")
            sys.exit(1)
        res = apply_threshold(matrix, args.threshold)
        save_image_gray(res, args.output)

    elif op == "histogram":
        hist = calculate_histogram(matrix)
        save_histogram_csv(hist, args.output)

    sys.exit(0)


if __name__ == "__main__":
    main()
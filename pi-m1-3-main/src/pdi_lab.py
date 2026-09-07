import argparse
import math
import os
import sys
from PIL import Image

# ==========================================
# 1. FUNÇÕES DE I/O E UTILITÁRIOS
# ==========================================

def resolve_input_path(input_arg: str) -> str:
    """Resolve o caminho da imagem de entrada permitindo busca em images/input/."""
    if os.path.exists(input_arg):
        return input_arg
    
    default_path = os.path.join("images", "input", input_arg)
    if os.path.exists(default_path):
        return default_path

    sys.stderr.write(f"Erro: Imagem nao encontrada em '{input_arg}' nem em '{default_path}'.\n")
    sys.exit(1)


def load_image_gray(path: str) -> tuple[list[list[int]], int, int]:
    """Lê a imagem, converte para escala de cinza e retorna matriz 2D de pixels."""
    resolved_path = resolve_input_path(path)
    try:
        with Image.open(resolved_path) as img:
            img_gray = img.convert("L")
            width, height = img_gray.size
            pixels_flat = list(img_gray.getdata())

            matrix = [
                pixels_flat[y * width : (y + 1) * width]
                for y in range(height)
            ]
            return matrix, width, height
    except Exception as e:
        sys.stderr.write(f"Erro ao abrir imagem '{resolved_path}': {e}\n")
        sys.exit(1)


def save_image_gray(matrix: list[list[float]], path: str) -> None:
    """Salva uma matriz 2D (int ou float) aplicando arredondamento e saturação no intervalo [0, 255]."""
    try:
        output_dir = os.path.dirname(os.path.abspath(path))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

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


def load_kernel_file(path: str) -> list[list[float]]:
    """Carrega e valida um kernel de arquivo .txt com dimensões e valores."""
    if not os.path.exists(path):
        sys.stderr.write(f"Erro: Arquivo de kernel nao encontrado: {path}\n")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            sys.stderr.write("Erro: Arquivo de kernel vazio.\n")
            sys.exit(1)

        # Primeira linha: linhas colunas
        header = lines[0].split()
        if len(header) != 2:
            sys.stderr.write("Erro: Cabecalho do kernel invalido (esperado: 'linhas colunas').\n")
            sys.exit(1)

        rows, cols = int(header[0]), int(header[1])

        if rows != cols:
            sys.stderr.write(f"Erro: Kernel nao quadrado ({rows}x{cols}).\n")
            sys.exit(1)

        if rows % 2 == 0:
            sys.stderr.write(f"Erro: Kernel de dimensao par ({rows}x{cols}).\n")
            sys.exit(1)

        kernel = []
        for line in lines[1:]:
            row_vals = [float(v) for v in line.split()]
            if row_vals:
                kernel.append(row_vals)

        if len(kernel) != rows or any(len(r) != cols for r in kernel):
            sys.stderr.write("Erro: Quantidade de valores no kernel incompativel com o cabecalho.\n")
            sys.exit(1)

        return kernel
    except Exception as e:
        sys.stderr.write(f"Erro ao ler arquivo de kernel '{path}': {e}\n")
        sys.exit(1)


# ==========================================
# 2. IMPLEMENTAÇÃO MANUAL DE CONVOLUÇÃO
# ==========================================

def get_pixel_value(matrix: list[list[int]], y: int, x: int, border: str) -> float | None:
    """Acessa pixel respeitando a estratégia de borda: 'copy' ou 'replicate'."""
    height = len(matrix)
    width = len(matrix[0])

    if 0 <= y < height and 0 <= x < width:
        return float(matrix[y][x])

    if border == "copy":
        return None
    elif border == "replicate":
        clamp_y = max(0, min(height - 1, y))
        clamp_x = max(0, min(width - 1, x))
        return float(matrix[clamp_y][clamp_x])
    else:
        sys.stderr.write(f"Erro: Estrategia de borda invalida '{border}'.\n")
        sys.exit(1)


def apply_convolution(
    matrix: list[list[int]], 
    kernel: list[list[float]], 
    border: str = "replicate"
) -> list[list[float]]:
    """Aplica convolução bidimensional genérica sobre a imagem."""
    height = len(matrix)
    width = len(matrix[0])
    k_size = len(kernel)
    pad = k_size // 2

    output = [[0.0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            acc = 0.0
            border_missing = False

            for ky in range(k_size):
                for kx in range(k_size):
                    # Coordenada correspondente na imagem com rotação implícita
                    img_y = y + (pad - ky)
                    img_x = x + (pad - kx)

                    px = get_pixel_value(matrix, img_y, img_x, border)

                    if px is None:
                        border_missing = True
                        break
                    acc += px * kernel[ky][kx]

                if border_missing:
                    break

            if border_missing and border == "copy":
                output[y][x] = float(matrix[y][x])
            else:
                output[y][x] = acc

    return output


# ==========================================
# 3. OPERAÇÕES ESPECÍFICAS
# ==========================================

def apply_laplacian_enhancement(
    matrix: list[list[int]], 
    kernel: list[list[float]], 
    border: str = "replicate"
) -> tuple[list[list[float]], list[list[float]]]:
    """Retorna (laplaciano_bruto, imagem_realçada)."""
    lap = apply_convolution(matrix, kernel, border)
    height, width = len(matrix), len(matrix[0])

    enhanced = [[0.0] * width for _ in range(height)]

    # Se centro do kernel Laplaciano for negativo (ex: -4), subtraímos para realçar
    center_val = kernel[len(kernel) // 2][len(kernel) // 2]
    sign = -1.0 if center_val < 0 else 1.0

    for y in range(height):
        for x in range(width):
            enhanced[y][x] = float(matrix[y][x]) + sign * lap[y][x]

    return lap, enhanced


def apply_sobel(
    matrix: list[list[int]], 
    kx: list[list[float]], 
    ky: list[list[float]], 
    border: str = "replicate"
) -> tuple[list[list[float]], list[list[float]], list[list[float]], list[list[float]]]:
    """Retorna (Gx, Gy, magnitude_aproximada, magnitude_euclidiana)."""
    gx = apply_convolution(matrix, kx, border)
    gy = apply_convolution(matrix, ky, border)

    height, width = len(matrix), len(matrix[0])
    mag_approx = [[0.0] * width for _ in range(height)]
    mag_euclidean = [[0.0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            val_gx = gx[y][x]
            val_gy = gy[y][x]

            mag_approx[y][x] = abs(val_gx) + abs(val_gy)
            mag_euclidean[y][x] = math.sqrt(val_gx**2 + val_gy**2)

    return gx, gy, mag_approx, mag_euclidean


# ==========================================
# 4. INTERFACE DE LINHA DE COMANDO (CLI)
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="PDI Lab M1.3 - Convolucao e Filtragem Espacial")

    parser.add_argument("--input", required=True, help="Imagem de entrada.")
    parser.add_argument("--output", required=True, help="Imagem ou diretorio de saida.")
    parser.add_argument(
        "--operation", required=True,
        choices=[
            "convolution", "mean_filter", "weighted_mean", 
            "laplacian", "sobel"
        ],
        help="Operacao solicitada"
    )
    parser.add_argument("--kernel", default=None, help="Caminho do arquivo de kernel (.txt)")
    parser.add_argument(
        "--border", default="replicate", choices=["copy", "replicate"],
        help="Estrategia de tratamento de borda"
    )

    args = parser.parse_args()

    matrix, _, _ = load_image_gray(args.input)
    op = args.operation

    if op == "convolution":
        if not args.kernel:
            sys.stderr.write("Erro: Argumento --kernel eh obrigatorio para 'convolution'.\n")
            sys.exit(1)
        kernel = load_kernel_file(args.kernel)
        res = apply_convolution(matrix, kernel, args.border)
        save_image_gray(res, args.output)

    elif op == "mean_filter":
        kernel = load_kernel_file(args.kernel or "kernels/mean_3x3.txt")
        res = apply_convolution(matrix, kernel, args.border)
        save_image_gray(res, args.output)

    elif op == "weighted_mean":
        kernel = load_kernel_file(args.kernel or "kernels/weighted_mean_3x3.txt")
        res = apply_convolution(matrix, kernel, args.border)
        save_image_gray(res, args.output)

    elif op == "laplacian":
        kernel = load_kernel_file(args.kernel or "kernels/laplacian_3x3.txt")
        lap_raw, enhanced = apply_laplacian_enhancement(matrix, kernel, args.border)
        
        # Salva imagem realçada
        save_image_gray(enhanced, args.output)

    elif op == "sobel":
        kx = load_kernel_file("kernels/sobel_x_3x3.txt")
        ky = load_kernel_file("kernels/sobel_y_3x3.txt")
        gx, gy, mag_app, mag_euc = apply_sobel(matrix, kx, ky, args.border)

        # Se output for diretótio ou arquivo base
        if args.output.endswith(".png") or args.output.endswith(".jpg"):
            base_dir = os.path.dirname(args.output)
            save_image_gray(mag_euc, args.output)
        else:
            base_dir = args.output
            os.makedirs(base_dir, exist_ok=True)
            save_image_gray(gx, os.path.join(base_dir, "sobel_gx.png"))
            save_image_gray(gy, os.path.join(base_dir, "sobel_gy.png"))
            save_image_gray(mag_app, os.path.join(base_dir, "sobel_mag_approx.png"))
            save_image_gray(mag_euc, os.path.join(base_dir, "sobel_mag_euclidean.png"))

    sys.exit(0)


if __name__ == "__main__":
    main()
import os
import sys
import pytest

# Garante que o src está no caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.pdi_lab import (
    apply_convolution,
    apply_laplacian_enhancement,
    apply_sobel,
    load_kernel_file,
)


@pytest.fixture
def identity_kernel():
    return [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]


@pytest.fixture
def sample_matrix():
    return [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]


def test_identity_convolution(sample_matrix, identity_kernel):
    res = apply_convolution(sample_matrix, identity_kernel, border="replicate")
    assert res == sample_matrix


def test_mean_filter_impulse():
    # Matriz impulso
    matrix = [
        [0, 0, 0],
        [0, 9, 0],
        [0, 0, 0],
    ]
    mean_kernel = [[1 / 9] * 3 for _ in range(3)]
    res = apply_convolution(matrix, mean_kernel, border="replicate")

    # O valor 9 deve se espalhar igualmente (1.0 por célula)
    assert round(res[1][1], 2) == 1.0


def test_border_strategies(sample_matrix, identity_kernel):
    res_replicate = apply_convolution(sample_matrix, identity_kernel, border="replicate")
    res_copy = apply_convolution(sample_matrix, identity_kernel, border="copy")
    assert res_replicate == res_copy


def test_sobel_gradient():
    # Degrau vertical (transição de 0 para 255 na coluna central)
    matrix = [
        [0, 255, 255],
        [0, 255, 255],
        [0, 255, 255],
    ]
    kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    gx, gy, mag_app, mag_euc = apply_sobel(matrix, kx, ky, border="replicate")

    # A magnitude de Gx deve detectar a borda vertical fortemente
    assert abs(gx[1][1]) > 0
    
    # Gy deve ser 0 pois não há variação de tom no sentido horizontal
    assert gy[1][1] == 0

    # A magnitude total calculada deve ser positiva e refletir a transição
    assert mag_euc[1][1] > 0
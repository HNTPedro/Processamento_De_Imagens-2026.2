import pytest
from src.pdi_lab import (
    apply_brightness,
    apply_contrast,
    apply_negative,
    apply_threshold,
    calculate_histogram,
)

@pytest.fixture
def sample_matrix():
    # Matriz sintética 2x2 para testes manuais
    return [[0, 100], [200, 255]]


def test_brightness_positive(sample_matrix):
    res = apply_brightness(sample_matrix, 30)
    assert res == [[30, 130], [230, 255]]  # O valor 255 saturou no limite superior


def test_brightness_negative(sample_matrix):
    res = apply_brightness(sample_matrix, -50)
    assert res == [[0, 50], [150, 205]]  # O valor 0 saturou no limite inferior


def test_contrast_reduction(sample_matrix):
    # alpha = 0.5: (val - 128)*0.5 + 128
    res = apply_contrast(sample_matrix, 0.5)
    assert res == [[64, 114], [164, 192]]


def test_contrast_expansion(sample_matrix):
    # alpha = 1.5
    res = apply_contrast(sample_matrix, 1.5)
    assert res == [[0, 86], [236, 255]]  # 0 e 255 saturaram


def test_negative(sample_matrix):
    res = apply_negative(sample_matrix)
    assert res == [[255, 155], [55, 0]]


def test_threshold(sample_matrix):
    res = apply_threshold(sample_matrix, 128)
    assert res == [[0, 0], [255, 255]]


def test_histogram(sample_matrix):
    hist = calculate_histogram(sample_matrix)
    assert len(hist) == 256
    assert hist[0] == 1
    assert hist[100] == 1
    assert hist[200] == 1
    assert hist[255] == 1
    assert sum(hist) == 4
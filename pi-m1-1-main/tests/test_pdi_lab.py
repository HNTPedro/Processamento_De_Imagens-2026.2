import numpy
import pytest
from src.pdi_lab.__main__ import (
    copy,
    channel_b,
    channel_g,
    channel_r,
    grayscale_average,
    grayscale_weighted,
    quantize,
    main
)

def test_testeSintetico():
    imagemTeste = numpy.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [100, 100, 100]]], dtype=numpy.uint8)
    copia = copy(imagemTeste)
    assert numpy.array_equal(imagemTeste, copia)
    assert numpy.array_equal(channel_b(imagemTeste)[:, :, 0], [[255, 0], [0, 100]])
    assert numpy.array_equal(channel_g(imagemTeste)[:, :, 1], [[0, 255], [0, 100]])
    assert numpy.array_equal(channel_r(imagemTeste)[:, :, 2], [[0, 0], [255, 100]])
    assert grayscale_average(imagemTeste)[0, 0] == 85
    assert grayscale_weighted(imagemTeste)[0, 0] == 29
    quant2 = quantize(grayscale_weighted(imagemTeste), 2)
    assert all(val in [0, 255] for val in numpy.unique(quant2))

def test_testeNiveis(monkeypatch):
    monkeypatch.setattr("sys.argv", [
        "pdi_lab.py", "--input", "images/input/test.png",
        "--output", "images/output/quant_1.png",
        "--operation", "quantize", "--levels", "1"
    ])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0

def test_testeImagemNone(monkeypatch):
    monkeypatch.setattr("sys.argv", [
        "pdi_lab.py", "--input", "images/input/arquivo_que_nao_existe.png",
        "--operation", "inspect"
    ])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0

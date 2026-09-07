Esta entrega é referente ao Laboratório M1.1 de Processamento de Imagens.

A implementação foi realizada em Python.

**Dependências:**

    opencv-python
    numpy
    pytest

**Preparação do Ambiente (Windows | Linux):**

Com venv (criar e ativar)

Windows:

    python -m venv venv
    .\venv\Scripts\activate  

Linux:

    python3 -m venv venv
    source venv/bin/activate

Instalar Dependências 
            
    pip install --upgrade pip
            
    pip install -r requirements.txt
  
**Execução:**

Feita via terminal utilizando o módulo, com a sintaxe geral:

python src/pdi_lab/__main__.py --input <caminho_entrada> [--output <caminho_saida>] --operation <operacao> [--levels <n_niveis>]

Comandos:

Inspecionar Imagem

    python src/pdi_lab/__main__.py --input images/input/imagem.png --operation inspect

Cópia Manual

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/copy.png --operation copy 

Isolar Canal Azul

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/channel_b.png --operation channel_b

Isolar Canal Verde

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/channel_g.png --operation channel_g

Isolar Canal Vermelho

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/channel_r.png --operation channel_r

Conversão Manual para níveis de Cinza (Média)

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/gray_avg.png --operation grayscale_average

Conversão Manual para níveis de Cinza (Ponderada)

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/gray_weighted.png --operation grayscale_weighted

Quantização (2 | 4 | 8 | 16)

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/quant_2.png --operation quantize --levels 2

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/quant_4.png --operation quantize --levels 4

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/quant_8.png --operation quantize --levels 8

    python src/pdi_lab/__main__.py --input images/input/imagem.png --output images/output/quant_16.png --operation quantize --levels 16


Executar Testes Automatizados

    python -m pytest

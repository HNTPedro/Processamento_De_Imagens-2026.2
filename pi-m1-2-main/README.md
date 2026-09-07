Esta entrega é referente ao Laboratório M1.2 de Processamento de Imagens.

A implementação foi realizada em Python.

**Dependências:**

    pillow
    pytest

Instalar Dependências 
            
    pip install --upgrade pip
            
    pip install -r requirements.txt
  
**Execução:**

Comandos:

# Ajuste de Brilho

Brilho Positivo (b = 30):
    
    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/bright_pos.png \
  --operation brightness \
  --value 30


Brilho Negativo (b = -30):

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/bright_neg.png \
  --operation brightness \
  --value -30


# Ajuste de Contraste

Contraste Reduzido (alpha = 0.5):
    
    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/contrast_05.png \
  --operation contrast \
  --alpha 0.5


Contraste Identidade (alpha = 1.0):

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/contrast_10.png \
  --operation contrast \
  --alpha 1.0


Contraste Ampliado (alpha = 1.5):

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/contrast_15.png \
  --operation contrast \
  --alpha 1.5


# Negativo

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/negative.png \
  --operation negative


# Limiarização Binária

Limiar baixo (T = 100):

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/thresh_100.png \
  --operation threshold \
  --threshold 100


Limiar alto (T = 180):

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/thresh_180.png \
  --operation threshold \
  --threshold 180


# Histograma (Geração dos arquivos CSV)

Histograma da Imagem Original:

    python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output results/histogram_orig.csv \
  --operation histogram


Histograma após Brilho Positivo:

    python src/pdi_lab.py \
  --input images/output/bright_pos.png \
  --output results/histogram_bright_pos.csv \
  --operation histogram


Histograma após Contraste Ampliado:

    python src/pdi_lab.py \
  --input images/output/contrast_15.png \
  --output results/histogram_contrast_15.csv \
  --operation histogram



# Executar os testes automatizados 

    python -m pytest

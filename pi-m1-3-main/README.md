Esta entrega é referente ao Laboratório M1.3 de Processamento de Imagens.

A implementação foi realizada em Python.

**Dependências:**

    pillow
    pytest

Instalar Dependências 
            
    pip install --upgrade pip
            
    pip install -r requirements.txt
  
**Execução:**

Comandos:

# Convolução Genérica com Kernel Identidade

  python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/identity.png \
  --operation convolution \
  --kernel kernels/identity_3x3.txt \
  --border replicate

# Filtro de Média 3x3

  python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/mean_3x3.png \
  --operation mean_filter \
  --kernel kernels/mean_3x3.txt \
  --border replicate 

# Filtro de Média 5x5

  python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/mean_5x5.png \
  --operation mean_filter \
  --kernel kernels/mean_5x5.txt \
  --border replicate

# Laplaciano e Realce

  python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/laplacian_enhanced.png \
  --operation laplacian \
  --border replicate

# Filtro de Sobel 
  python src/pdi_lab.py \
  --input images/input/imagem.png \
  --output images/output/sobel_magnitude.png \
  --operation sobel \
  --border replicate

# Executar os testes automatizados 

    python -m pytest

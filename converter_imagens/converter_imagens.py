import os
from PIL import Image

converter = [
    ('lg', (1999,1125)), 
    ('', (1920,1080)), 
    ('thumb@2x', (1070,602)), 
    ('md', (991,557)), 
    ('sm', (767,431)), 
    ('xs', (575,323)), 
    ('thumb', (535,301)), 
    ('placehold', (230,129))
]

def eh_imagem(nome_arquivo):
    if nome_arquivo.endswith('png') or nome_arquivo.endswith('jpg'):
        return True
    return False

def reduzir_tamanho_imagens(input_dir, output_dir, ext='.jpg'):
    lista_de_arquivos = [nome for nome in os.listdir(input_dir) if eh_imagem(nome)]
    for nome in lista_de_arquivos:
        imagem = Image.open(os.path.join(input_dir, nome)).convert('RGB')
        nome_antigo = os.path.splitext(nome)[0]
        for x in range(len(converter)):
            redimensionada = imagem.resize(converter[x][1])
            nome_novo = nome_antigo  + '_' + converter[x][0]
            redimensionada.save(os.path.join(output_dir, nome_novo + ext))

if __name__ == "__main__":
    diretorio = '/home/nilson/Documentos/imagens'

    reduzir_tamanho_imagens(diretorio, diretorio+'/convertida')

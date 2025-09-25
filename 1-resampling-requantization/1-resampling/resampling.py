from PIL import Image

def real_size_in(im, dpi):
    # A função im.size retorna (largura, altura) em pixels
    # A fórmula retorna (largura, altura) em polegadas
    return [dim / dpi for dim in im.size]

def resampling(im, old_dpi, new_dpi):
    # Calcula o tamanho físico atual em polegadas
    physical_size = real_size_in(im, old_dpi)
    
    # Calcula a nova resolução em pixels para manter o tamanho físico
    new_pixel_dims = [int(physical_size[0] * new_dpi), int(physical_size[1] * new_dpi)]
    
    # Redimensiona a imagem com um filtro de alta qualidade
    return im.resize(tuple(new_pixel_dims), Image.Resampling.LANCZOS)
    
def cut(im):
    # Corta a imagem para extrair o 6º quadrante de uma grade 4x4
    w, h = im.size
    box = (w/4, h/4, w/2, h/2)
    # Converte para inteiros para a função crop
    box = tuple(map(int, box))
    return im.crop(box)

def main():
    try:
        im = Image.open("resampling.tif")
    except FileNotFoundError:
        print("Erro: Arquivo 'resampling.tif' não encontrado.")
        return

    # --- Sugestão 1: Ler DPI do arquivo ---
    dpi = im.info.get('dpi', (72, 72))[0] # Padrão de 72 se não encontrar

    print("- Imagem Original")
    print(f"Definição: {im.size} | Formato: {im.format} | Modo: {im.mode} | DPI: {dpi}")
    print("-" * 20)

    # --- Sugestão 2: Cortar ANTES de reamostrar ---
    im_cortada = cut(im)
    im_cortada.show() # Mostra o corte inicial

    print("(Digite 0 para parar)")
    while True:
        try:
            # --- Sugestão 3: Tratamento de erro na entrada ---
            new_dpi_str = input("Reamostrar para qual DPI? ")
            new_dpi = int(new_dpi_str)

            if new_dpi == 0:
                break
            
            # Aplica a reamostragem apenas na imagem já cortada
            im_reamostrada = resampling(im_cortada, dpi, new_dpi)
            im_reamostrada.show()
            
        except ValueError:
            print("Por favor, digite um número inteiro.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

if __name__ == "__main__":
    main()
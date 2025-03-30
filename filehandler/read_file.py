def fileread(file: str):
    try:
        with open(file, 'r', encoding='utf-8') as prueba:
            contenido: str = prueba.read()

            for char in contenido:
                print(char)
    except FileNotFoundError:
        print(f"El archivo %s no fue encontrado.", file)
    except Exception as e:
        print(f"Ocurrio un error inesperado! %v", e)


import os, time
user_folder = os.path.expanduser("~")
documents_folder = os.path.join(user_folder, "Documentos")
honeypots_folder = os.path.join(documents_folder, "honeypots")
cont = 0
def change_extension(path, old_ext, new_ext):
    for filename in os.listdir(path):
        if filename.endswith(old_ext):
            base = os.path.splitext(filename)[0]
            os.rename(os.path.join(path, filename), os.path.join(path, base + new_ext))

# Exemplo de uso
change_extension(honeypots_folder, '.txt', '.md')
while True:
    cont += 1
    print(cont)
    time.sleep(3)

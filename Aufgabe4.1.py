import os

path_value = os.environ.get('PATH')

if path_value:
    print("Der Inhalt der Umgebungsvariable 'PATH' ist:")
    for path in path_value.split(os.pathsep):
        print(f"  - {path}")
else:
    print("Die Umgebungsvariable 'PATH' konnte nicht gefunden werden.")
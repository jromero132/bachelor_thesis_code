# Implementación de la Tesis de Licenciatura en Ciencia de la Computación

## A modo general
Nombre y apellidos: José Ariel Romero Costa \
Institución: Facultad de Matemática y Computación de la Universidad de La Habana \
Grupo: C-512 \
Correo de MatCom: j.romero@estudiantes.matcom.uh.cu \
Correo de contacto: josea132.romero@gmail.com \
Tema de tesis: Generación Automática de Ontologías \
Tutor: MSc. Juan Pablo Consuegra Ayala \
Dirección del repositorio: https://github.com/jromero132/bachelor_thesis

## Implementación

### Docker
Para ejecutar la implementación se recomienda el uso de `Docker` y `DockerCompose` además de seguir los siguientes pasos:

1. Instalar `Docker`: \
https://docs.docker.com/engine/install/
2. Instalar `DockerCompose`: \
https://docs.docker.com/compose/install/
3. Clonar el repositorio de la implementación ejecutando el comando: \
`git clone https://github.com/jromero132/bachelor_thesis_code`
4. Entrar al directorio de la implementación recién clonada ejecutando el comando: \
`cd bachelor_thesis_code/`
5. Una vez dentro del directorio, ejecutar el comando: \
`docker-compose up`

Esto lleva a cabo las acciones necesarias para ejecutar la implementación, llevando a cabo la creación de una imagen de `Docker` y posteriormente ejecutarla, resultando en un contenedor.

Una vez corrida la implementación, esta guarda un archivo `knowledge_graph.png` con el resultado del grafo de conocimiento en una foto. Esta puede ser extraída del contenedor mediante el comando: \
`docker cp <container_id>:code/knowledge_graph.png <destination_path>`

Esto copia la imagen en el *path* de destino `<destination_path>`. Tener en cuenta que `<container_id>` es el id del contenedor específico de esta implementación y puede verse a través del comando: \
`docker container ls`

### Archivos de código
La implementación fue hecha en `python` y  el archivo inicial a ejecutar es `main.py`. Este requiere de un parámetro, el *path* que contiene los archivos de texto y de anotación a los que se les desea construir el grafo de conocimiento. A modo general, el comando de ejecución es: \
`python main.py <path>`

En caso de omitir este *path*, la implementación asume que se desea construir el grafo de conocimiento de todo el corpus usado y también genera la imagen para este.

Si se desea realizar este proceso con un corpus específico, el cual puede tener, por ejemplo, una única oración para probar, los pasos a seguir son:

1. Copiar la carpeta de nombre `<name>` para el directorio conteniendo la implementación
2. En la última línea del archivo `Dockerfile`, la cual es: \
`CMD ["python", "main.py"]` \
agregar  el nombre de la nueva carpeta, resultando: \
`CMD ["python", "main.py", "<name>"]`

De esta forma, una vez vuelto a ejecutar `docker-compose up`, se llega al mismo resultado que se ha venido describiendo.
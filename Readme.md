## Ejecución del juego

python pacman-game-qlearning.py

### 1. Crear el entorno virtual
Asegúrate de estar en la raíz del proyecto y ejecuta el siguiente comando:
```bash
# Con la consila de GitBash
# Crear el entorno virtual
$ python -m venv venv

# Activar el entorno virtual
$ source venv/Scripts/activate
```

## Instalación de dependencias
```bash
$ python -m pip install -r requirements.txt
```
## Ejecución del juego con botones
```bash
$ python pacman-game-qlearning-manual.py
```

## Detalles Tecnicos

- 1. Entrenamiento:
- 1.1. Pac-Man empieza en la esquina superior izquierda.
- 1.2. Explora el tablero durante varios episodios (partidas simuladas).
- 1.3. Cada vez que se mueve, actualiza la Q-Table con la fórmula.
- 1.4. Poco a poco aprende qué movimientos llevan a la meta y cuáles son malos (muros).
- 2. Ejecución automática:
- 2.1. Una vez entrenado, Pac-Man usa la Q-Table.
- 2.2. En cada estado, elige la acción con mayor valor Q(s,a).
- 2.3. Así sigue el camino “óptimo” hacia la meta.
- 3. Modo paso a paso (manual):
- 3.1. En vez de moverse solo, tú presionas un botón.
- 3.2. El juego consulta la Q-Table y muestra la acción que Pac-Man tomaría.
- 3.3. Se actualiza la posición y se imprime en la consola.

# pip install PyOpengl
# pip install PyOpengl_accelerate
# pip install pygame
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

#Configurações do cubo
#coordenadas dos vertices
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
#indices dos vertices
faces = (
    (0, 1, 2, 3), (4, 5, 7, 6), (0, 4, 6, 3),
    (1, 5, 7, 2), (0, 1, 5, 4), (3, 2, 7, 6)
)
#cor das faces do cubo
cores = (
    (1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1), (1,0,1)
)

#Translação (movimentar)
#Rotação (rotacionar)
#Escalonamento (redimensionar)

def desenha_cubo():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(cores[i])
        for indice_vertice in face:
            glVertex3fv(vertices[indice_vertice])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("cubo estatico")

    #configuração 3D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    #configuração 3D [Visão]
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.0, 0.2, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #Deslocamento no espaço 3D
        glTranslate(0.0, 0.0, -5.0)
        #Rotaciona o cubo no espaço 3D
        glRotate(45, 1, 1, 1)
        #Redimensiona o cubo no espaço 3D
        glScale(0.5, 0.5, 0.5)
        desenha_cubo()
        pygame.display.flip()
        pygame.time.wait(10)
if __name__ == '__main__':
    main()
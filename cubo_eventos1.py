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

def desenha_esfera():
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor(.8, .2, .8) #roxo
    gluSphere(quadric, 0.5, 32, 32)
    gluDeleteQuadric(quadric)

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

    # variaveis do cubo
    pos_x = 0
    pos_y = 0
    angulo_z = 0

    # variaveis da esfera
    esfera_rotacao_y = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #checa as teclas pressionadas
        keys = pygame.key.get_pressed()

        print(f'(x, y): ({pos_x}, {pos_y})')

        #verifica as teclas pressionadas
        if keys[pygame.K_LEFT]:
            print('ESQUERDA')
            if pos_x > -2:
                pos_x -= 0.01
        if keys[pygame.K_RIGHT]:
            print('DIREITA')
            if pos_x < 2:
                pos_x += 0.01
        if keys[pygame.K_UP]:
            print('CIMA')
            if pos_y < 1.35:
                pos_y += 0.01
        if keys[pygame.K_DOWN]:
            print('BAIXO')
            if pos_y > -1.35:
                pos_y -= 0.01
        if keys[pygame.K_q]:
            print ('Tecla Q')
            angulo_z -= 1
        if keys[pygame.K_e]:
            print('Tecla E')
            angulo_z += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        #camera(fixa)
        gluLookAt(0, 0, 0.5, 0, 0, 0, 0, 1, 0)

        # atualiza a rotação da esfera
        esfera_rotacao_y += 2

        #salva o estado da matrix [cubo]
        glPushMatrix()
        #Deslocamento no espaço 3D
        glTranslate(pos_x, pos_y, -5.0)
        #Rotaciona o cubo no espaço 3D
        glRotate( angulo_z, 1, 1, 1)
        #Redimensiona o cubo no espaço 3D
        glScale(0.5, 0.5, 0.5)
        desenha_cubo()
        #Restaura o estado da matriz [cubo]
        glPopMatrix()

        #Salva o estado da matriz [esfera]
        glPushMatrix()
        glRotatef(esfera_rotacao_y, 0, 1, 0)
        glTranslatef(2, 0, 0)
        # desenha a esfera
        desenha_esfera()
        #Restaura o estado da matriz [esfera]
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)
if __name__ == '__main__':
    main()
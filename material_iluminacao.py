# pip install PyOpenGL
# pip install PyOpenGL_accelerate
# pip install pygame

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

vertices = (
    (1,-1,-1),  (1,1,-1),  (-1,1,-1),
    (-1,-1,-1), (1,-1, 1), (1,1,1),
    (-1,-1,1),  (-1,1,1)
)
#vetor perpendicular a face, apontam para fora do cubo
normals = (
    (0,0,-1), (0,0,1),
    (-1,0,0), (1,0,0),
    (0,-1,0), (-1,0,0)
)

faces = (
    (0,1,2,3), (4,5,7,6), (0,4,6,3),
    (1,5,7,2), (0,1,5,4), (3,2,7,6)
)

def desenha_cubo():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])

        for vertice in face:
            glVertex3fv(vertices[vertice])
    glEnd()

def desenha_esfera():
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)

    material_ambiente_esfera = (0.2, 0.1, 0.2, 1.0)
    material_diffuse_esfera = (0.8, 0.2, 0.8, 1.0)
    #ambient_oclusion
    # como o objeto projeta as sombras na cena
    glMaterialfv(GL_FRONT,
                 GL_AMBIENT,
                 material_ambiente_esfera)
    #diffuse
    # como o objeto lida com a luz direta
    glMaterialfv(GL_FRONT,
                 GL_DIFFUSE,
                 material_diffuse_esfera)
    gluSphere(quadric, 0.5, 32, 32)
    gluDeleteQuadric(quadric)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Iluminação e materiais')

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_LIGHTING) #habilita iluminação
    glEnable(GL_LIGHT0) #habilita luz 0

    #propriedades da luz
    luz_posicao = (5.0, 5.0, 5.0, 1.0)
    luz_ambiente = (0.2, 0.2, 0.2, 1.0)
    luz_difusa = (1.0, 1.0, 1.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)

    #Configuração do material
    #reflete o ambiente
    mat_ambiente = (0.2, 0.1, 0.1, 1.0)
    #reflete a luz
    mat_difuso = (0.8, 0.2, 0.2, 1.0)
    #reflete o brilho
    mat_especular = (1.0, 1.0, 1.0, 1.0)
    mat_brilho = 50.0

    glClearColor(0.1, 0.0, 0.2, 1.0)

    #variaveis de estado
    obj_pos_x, obj_pos_y, obj_pos_z = 0.0,0.0,0.0
    obj_rot_y = 0.0
    obj_scale = 1.0
    esfera_rot = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        esfera_rot += 2.0
        #renderizando
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0,
                  0.0, 0.0, 0.0, 1.0, 0.0)
        #render do cubo
        glPushMatrix()
        #Aplicando os materiais no cubo
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_difuso)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_especular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_brilho)

        glTranslate(obj_pos_x, obj_pos_y, obj_pos_z)
        glRotate(obj_rot_y, 0.0, 1.0, 0.0)
        glScalef(obj_scale, obj_scale, obj_scale)

        desenha_cubo()
        glPopMatrix()

        #renderiza a esfera
        glPushMatrix()
        glRotate(esfera_rot, 0.0,1.0, 0.0)
        glTranslate(2.0, 0.0, 0.0)
        desenha_esfera()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()





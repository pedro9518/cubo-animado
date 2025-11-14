# pip install PyOpengl
# pip install PyOpengl_accelerate
# pip install pygame
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math

#configurações dos modelos

# Coordenadas dos vertices do cubo (Lua)
vertices_cubo = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
# Indices dos vertices que formam as faces
faces_cubo = (
    (0, 1, 2, 3), (4, 5, 7, 6), (0, 4, 6, 3),
    (1, 5, 7, 2), (0, 1, 5, 4), (3, 2, 7, 6)
)


def desenha_planeta_bicolor():
    """ Desenha uma esfera com metade azul e metade verde, girando em seu eixo Y. """
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)

    #desenha a metade azul (frontal)
    glClipPlane(GL_CLIP_PLANE0, (1.0, 0.0, 0.0, 0.0))  # Plano em x=0, corta o lado negativo de X
    glEnable(GL_CLIP_PLANE0)
    glColor3f(0.2, 0.4, 0.8)  # Cor azul
    gluSphere(quadric, 1.0, 32, 32)
    glDisable(GL_CLIP_PLANE0)

    #desenha a metade verde (traseira)
    glClipPlane(GL_CLIP_PLANE1, (-1.0, 0.0, 0.0, 0.0))  # Plano em x=0, corta o lado positivo de X
    glEnable(GL_CLIP_PLANE1)
    glColor3f(0.0, 0.7, 0.0)  # Cor verde
    gluSphere(quadric, 1.0, 32, 32)
    glDisable(GL_CLIP_PLANE1)

    gluDeleteQuadric(quadric)


def desenha_lua():
    """ Desenha um cubo cinza (Lua) """
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.7, 0.7)  # Cor cinza claro
    for face in faces_cubo:
        for indice_vertice in face:
            glVertex3fv(vertices_cubo[indice_vertice])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sistema Planetário Bicolor com Wrap")

    #configuração da câmera e perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    fov_y = 45
    aspect_ratio = (display[0] / display[1])
    z_near = 0.1
    z_far = 50.0
    gluPerspective(fov_y, aspect_ratio, z_near, z_far)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.1, 1)

    #variáveis de controle e posição

    pos_z_sistema = -10.0

    #planeta
    planeta_velocidade_rotacao = 1.0
    planeta_auto_rotacao = 0

    #lua
    lua_velocidade_orbita = 1.0
    lua_orbita_rotacao = 0
    lua_distancia_orbita = 2.5

    #sistema (planeta + lua)
    sistema_pos_x = 0.0
    sistema_velocidade_x = 0.02

    #cálculo do limite da tela para o "wrap"
    largura_visivel = 2.0 * math.tan(math.radians(fov_y / 2.0)) * abs(pos_z_sistema) * aspect_ratio
    # adiciona uma margem para a esfera sair completamente
    limite_tela_x = largura_visivel / 2.0 + 1.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #verificação de teclas pressionadas
        keys = pygame.key.get_pressed()

        #controle da auto-rotação do planeta
        if keys[pygame.K_LEFT]:
            planeta_velocidade_rotacao -= 0.1
        if keys[pygame.K_RIGHT]:
            planeta_velocidade_rotacao += 0.1

        #controle da obita da lua
        if keys[pygame.K_DOWN]:
            lua_velocidade_orbita -= 0.1
            if lua_velocidade_orbita < 0:
                lua_velocidade_orbita = 0
        if keys[pygame.K_UP]:
            lua_velocidade_orbita += 0.1

        #atualiza rotações
        planeta_auto_rotacao += planeta_velocidade_rotacao
        lua_orbita_rotacao += lua_velocidade_orbita

        #atualiza movimento horizontal do sistema
        sistema_pos_x += sistema_velocidade_x

        #lógica do "Screen Wrap"
        if sistema_pos_x > limite_tela_x:
            sistema_pos_x = -limite_tela_x

        #renderização
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        #câmera (fixa, olhando para a origem)
        gluLookAt(0, 0, 0,
                  0, 0, -1,
                  0, 1, 0)

        #nível do sistema
        glPushMatrix()
        try:
            glTranslate(sistema_pos_x, 0, pos_z_sistema)

            #nível do planeta
            glPushMatrix()
            try:
                #autorotação do planeta no eixo Y
                glRotatef(planeta_auto_rotacao, 0, 1, 0)
                desenha_planeta_bicolor()
            finally:
                glPopMatrix()

            glPushMatrix()
            try:
                glRotatef(lua_orbita_rotacao, 0, 1, 0)
                glTranslate(lua_distancia_orbita, 0, 0)
                glScale(0.3, 0.3, 0.3)
                desenha_lua()
            finally:
                glPopMatrix()

        finally:
            glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
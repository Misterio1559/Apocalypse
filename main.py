import ctypes
import pygame
import configparser
from Interface import Interface, draw
import Game

if __name__ == '__main__':
    user32 = ctypes.windll.user32
    size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    interface = Interface(size)
    pygame.init()
    a = Game
    smert = a
    game_screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Апокалипсис")
    interface.main_menu(game_screen)
    while interface.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interface.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                interface.get_click(event.pos, game_screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and interface.menu == 3:
                interface.volume += 1
                if interface.volume >= 100:
                    interface.volume = 100
                interface.settings_update(game_screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and interface.menu == 3:
                interface.volume -= 1
                if interface.volume < 0:
                    interface.volume = 0
                interface.settings_update(game_screen)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                interface.get_button('Esc', game_screen)
            if smert == 1:
                interface.get_button('Esc', game_screen)
        if interface.running:
            pygame.display.flip()
    pygame.quit()

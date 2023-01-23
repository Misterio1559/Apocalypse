import pygame
import time
from Game import Game
import Particals


def draw(obj, scr, x, y, col='white', size=50):  # Рисовка текста по введённым данным
    font = pygame.font.Font(None, size)
    text = font.render(str(obj), True, col)
    scr.blit(text, (x, y))


class Interface:  # Интерфейс, здесь происходят те, или иные действия при нажатии на элементы
    def __init__(self, size):
        self.size = size
        self.menu = 0  # Тип текущего меню
        self.sprites = pygame.sprite.Group()
        self.running = True
        self.music = pygame.mixer.music
        self.round = None
        self.rules_text = ['    - Я смотрю вы новенький! Чтож. Ознакомлю с правилами.',
                           'Со старта, каждому игроку выдаётся 8 карт: 5 - юниты, 3 - усилители.',
                           'Игроки кладут 3 карты юнитов на поле, а другие две оставляют в резерве.',
                           'Карты усилителей, так-же не видны. Кстати, усилители на то и усилители,',
                           'Что усиливают ваши карты, но будте на чеку,',
                           'они могут сделать и хорошо и плохо сразу! Вернёмся к юнитам.',
                           'У каждой карты юнитов имеются несколько показателей:',
                           'Здоровье, Атака, Наносимая радиация,',
                           'Радиация со старта.',
                           'Если здоровье карты упадёт ниже 1, карта погибнет.',
                           'Если радиация карты окажется выше 7, то карта так-же погибнет.',
                           'У некоторых карт есть свои особенности, так что аккуратнее!',
                           'Цель игры - оставить противника без юнитов.',
                           'Приятной игры!',
                           '', '', '', 'Нажмите Esc чтобы выйти']
        self.volume = 100

    def main_menu(self, screen):  # Загрузка главного меню
        size = self.size
        self.music.load("Round.mp3")  # Загрузка музыки
        self.music.play(-1)

        self.music.set_volume(self.volume / 100)
        fone = pygame.transform.scale(pygame.image.load('fone.png'), size)  # Загрузка фона
        fone_ex = fone.get_rect()

        button = pygame.image.load('button.png')  # Загрузка элементов в главном меню
        button.set_colorkey((255, 255, 255))
        button_ex = button.get_rect(bottomright=(size[0] // 1.725, size[1] // 2.2))
        button_ex1 = button.get_rect(bottomright=(size[0] // 1.725, size[1] // 1.45))
        button_ex2 = button.get_rect(bottomright=(size[0] // 1.725, size[1] // 1.08))

        main = pygame.image.load("Main.png")  # Загрузка главной надписи
        main.set_colorkey((200, 100, 200))
        main_ex = button.get_rect(bottomright=(size[0] // 2.05, size[1] // 3.5))

        screen.blit(fone, fone_ex)  # А теперь всё это проявим
        screen.blit(main, main_ex)
        screen.blit(button, button_ex)
        screen.blit(button, button_ex1)
        screen.blit(button, button_ex2)

        draw("Начать игру", screen, size[0] // 1.725 - 239, size[1] // 2.2 - 100, 'black')  # Напишем текст в рамки
        draw("Правила", screen, size[0] // 1.725 - 210, size[1] // 1.45 - 120, 'black')
        draw("игры", screen, size[0] // 1.725 - 180, size[1] // 1.45 - 80, 'black')
        draw("Настройки", screen, size[0] // 1.725 - 230, size[1] // 1.08 - 100, 'gray')

        pygame.display.flip()  # Отобразим
        button.set_colorkey((255, 255, 255))  # Уберём фон у того, что явно не надо

    def rules(self, screen):  # Правила игры
        size = self.size
        fone_rules = pygame.transform.scale(pygame.image.load('rules_fone.jpg'), size)  # Фон под рассказывание правил
        fone_ex = fone_rules.get_rect()
        screen.blit(fone_rules, fone_ex)
        space, text = 0, ''  # А теперь начнём печатать, предусмотрены кнопки Esc (Выход из меню правил)
        # и Пробела (Печатает текст сразу)
        to_return = False
        flag = True
        draw("Нажмите пробел чтобы ускорить анимацию", screen, size[0] // 7 * 5, size[1] // 7 * 6, 'white', size=20)
        for i in self.rules_text:
            for x in i:
                while i == 'Если здоровье карты упадёт ниже 1, карта погибнет.' and flag:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:  # При выходе - делает выход
                            self.running = False
                            return
                        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                            screen.blit(fone_rules, fone_ex)
                            space = 0
                            flag = False
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:  # При выходе - делает выход
                        self.running = False
                        return
                    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:  # Пробел
                        draw(i, screen, size[0] // 8, size[1] // 8 + space, 'white', size=40)
                        pygame.display.flip()
                        time.sleep(0.1)
                        to_return = True
                if to_return:
                    continue
                text += x
                draw(text, screen, size[0] // 8, size[1] // 8 + space, 'white', size=40)
                pygame.display.flip()
                time.sleep(0.1)
            to_return = False
            text = ''
            space += 45

    def onStart(self, screen):
        size = self.size
        self.music.load("Round.mp3")
        self.music.play(-1)
        self.music.set_volume(self.volume)
        self.round = Game(screen, size)
        round_is = True
        self.menu = 1
        while round_is:  # Сам процесс игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if self.round.turn == 99:
                    screen.fill((0, 0, 0))
                    self.round.sprites.update()
                    self.round.sprites.draw(screen)
                    time.sleep(5)
                    self.main_menu(screen)
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.get_click(event.pos, screen)
            screen.fill((0, 0, 0))
            self.round.sprites.update()
            self.round.sprites.draw(screen)
            pygame.display.flip()
        pygame.display.flip()

    def match_pos(self, pos, sp):
        for i in sp:
            if i[0] <= pos[0] <= i[0] + 400 and i[1] <= pos[1] <= i[1] + 200:
                return i[2]
        return False

    def get_click(self, pos, screen):  # При нажатии курсором
        size = self.size
        if self.menu == 0:
            if size[0] // 1.725 - 270 < pos[0] < size[0] // 1.725 and \
                    size[1] // 2.2 - 168 < pos[1] < size[1] // 2.2:
                self.onStart(screen)
                self.menu = 1
            elif size[0] // 1.725 - 270 < pos[0] < size[0] // 1.725 and \
                    size[1] // 1.45 - 168 < pos[1] < size[1] // 1.45:
                self.rules(screen)
                self.menu = 2
            elif size[0] // 1.725 - 270 < pos[0] < size[0] // 1.725 and \
                    size[1] // 1.08 - 168 < pos[1] < size[1] // 1.08:
                self.settings(screen)
                self.menu = 3
        elif self.menu == 1:
            if self.round.turn == 1 and not self.round.click_selected and \
                    self.match_pos(pos, self.round.coord_sp[0]):
                if self.match_pos(pos, self.round.coord_sp[0]).name == "Deleted":
                    return
                for i in Particals.create_particles(pos, screen):
                    self.round.sprites.add(i)
                self.round.selected_card = self.match_pos(pos, self.round.coord_sp[0])
                self.round.click_selected = True
            elif self.round.turn == 1 and self.round.click_selected and \
                    self.match_pos(pos, self.round.coord_sp[1]):
                if self.match_pos(pos, self.round.coord_sp[1]).name == "Deleted":
                    return
                self.round.attack(screen, self.round.selected_card, self.match_pos(pos, self.round.coord_sp[1]))
                self.round.selected_card = None
                for i in Particals.create_particles_bad(pos, screen):
                    self.round.sprites.add(i)
                self.round.click_selected = False
            elif self.round.turn == 0 and not self.round.click_selected and \
                    self.match_pos(pos, self.round.coord_sp[1]):
                if self.match_pos(pos, self.round.coord_sp[1]).name == "Deleted":
                    return
                self.round.selected_card = self.match_pos(pos, self.round.coord_sp[1])
                for i in Particals.create_particles(pos, screen):
                    self.round.sprites.add(i)
                self.round.click_selected = True
            elif self.round.turn == 0 and self.round.click_selected and \
                    self.match_pos(pos, self.round.coord_sp[0]):
                if self.match_pos(pos, self.round.coord_sp[0]).name == "Deleted":
                    return
                self.round.attack(screen, self.round.selected_card, self.match_pos(pos, self.round.coord_sp[0]))
                for i in Particals.create_particles_bad(pos, screen):
                    self.round.sprites.add(i)
                self.round.selected_card = None
                self.round.click_selected = False

    def get_button(self, b, screen):  # При нажатии кнопки
        if self.menu == 2 and b == 'Esc':
            self.menu = 0
            self.main_menu(screen)
        if self.menu == 3 and b == 'Esc':
            self.menu = 0
            self.main_menu(screen)

    def settings(self, screen):  # Загрузка настроек
        size = self.size
        fone = pygame.image.load('res.png')  # Загрузка элементов в главном меню
        fone = pygame.transform.scale(fone, (size[0] // 7 * 5, size[1] // 7 * 5))
        fone_ex = fone.get_rect(bottomright=(size[0] // 7 * 6 + 5 - 10, size[1] // 7 * 6.2))
        screen.blit(fone, fone_ex)
        draw("Музыка", screen, size[0] // 7 * 1.5, size[1] // 7 * 2, 'white')
        draw("Настройки", screen, size[0] // 7 * 3, size[1] // 7 * 1.5, 'white')
        draw("Нажмите Esc чтобы покинуть меню и подтвердить изменения", screen, size[0] // 7 * 4,
             size[1] // 7 * 5.8, 'white', size=20)
        self.settings_update(screen)

    def settings_update(self, screen):
        size = self.size
        pygame.draw.line(screen, 'white', (size[0] // 7 * 2.4, size[1] // 7 * 2 + 15),
                         (size[0] // 7 * 4.42, size[1] // 7 * 2 + 15), 10)
        pygame.draw.line(screen, 'black', (size[0] // 7 * 2.5 + self.volume * size[0] // 400, size[1] // 7 * 2 + 15),
                         (size[0] // 7 * 2.5 + self.volume * size[0] // 400, size[1] // 7 * 2 + 15), 10)
        pygame.draw.rect(screen, 'gray', (size[0] // 7 * 4.52, size[1] // 7 * 2, 95, 35))
        draw(f"{self.volume}%", screen, size[0] // 7 * 4.52, size[1] // 7 * 2, 'white')

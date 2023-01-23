import pygame
import sqlite3
import random
from time import sleep


def draw(obj, scr, x, y, col='white', size=50):  # Рисовка текста по введённым данным
    font = pygame.font.Font(None, size)
    text = font.render(str(obj), True, col)
    scr.blit(text, (x, y))


class Card_mob(pygame.sprite.Sprite):  # Карта моба (юнита)
    def __init__(self, sp, ind):
        super().__init__()
        self.name = sp[0]
        self.hp = sp[2]
        self.maxhp = sp[2]
        self.rare = sp[1]
        self.dmg = sp[3]
        self.rad = sp[4]
        self.cur_rad = sp[5]
        self.joke = sp[6]
        self.info = sp[7]
        self.id = ind
        im = pygame.transform.scale(pygame.image.load("card.png"), (400, 200))
        draw(f'{self.name} | {self.cur_rad}/7 Рад', im, x=20, y=20, size=40)
        draw(f'{self.hp} ОЗ {self.dmg} Ат {self.rad} Рад      |{self.rare}.', im, x=20, y=50, size=30)
        draw(f'{self.joke}!', im, x=20, y=85, size=30)
        draw(f'{self.info}', im, x=20, y=120, size=30)
        self.image = im
        self.rect = im.get_rect()

    def updating(self):  # Оно должно красиво вывестись на экран в следствии своей работы карточку-моба
        im = pygame.transform.scale(pygame.image.load("card.png"), (400, 200))
        draw(f'{self.name} | {self.cur_rad}/7 Рад', im, x=20, y=20, size=40)
        draw(f'{self.hp} ОЗ {self.dmg} Ат {self.rad} Рад      |{self.rare}.', im, x=20, y=50, size=30)
        draw(f'{self.joke}!', im, x=20, y=85, size=30)
        draw(f'{self.info}', im, x=20, y=120, size=30)
        self.image = im

    def on_damage(self, x, y):  # Оно должно красиво вывести на экран анимацию получения урона
        pass

# class Card_boost:  # Карта буста
# def __init__(self, sp):
# self.name = sp[0]
# self.rare = sp[1]
# self.joke = sp[2]
# self.info = sp[3]

# def printing(self, x, y, screen):  # Оно должно красиво вывести на экран в следствии своей работы карточку-буст
# pass

# def using(self, x, y):  # Оно должно красиво вывести на экран использование карты-буста над юнитом
# pass


class Game:  # Сама игра и её внутренние составляющие
    def __init__(self, screen, size):
        self.turn = 1  # чей ход
        db = sqlite3.connect('cards.db')  # Загружаем базу данных с картами
        cur = db.cursor()
        deck_mobs = []
        self.dead = 0
        self.sprites = pygame.sprite.Group()
        self.player1_field = []  # Какие карты на поле (у первого игрока)
        self.player2_field = []  # Какие карты на поле (у второго игрока)
        screen.fill((0, 0, 0))
        self.click_selected = False

        result = cur.execute("""SELECT * FROM Cards""").fetchall()  # Формируем колоду юнитов
        for i in result:
            deck_mobs.append(Card_mob(i, random.randint(0, 100000)))
        # deck_boosts = []
        # res = cur.execute("""SELECT * FROM Boosts""").fetchall()  # Формируем колоду бустов
        # for x in res:
        #     deck_boosts.append(Card_boost(x))

        self.player1_hand = [i for i in random.sample(deck_mobs, 3)]  # Рука первого игрока
        # self.player1_hand.append([card for card in random.sample(deck_boosts, 3)])
        # Бусты первого игрока (последний элемент списка (self.player1_hand - бусты в руке)

        self.coord_sp = [[], []]
        self.selected_card = None

        self.player2_hand = [i for i in random.sample(deck_mobs, 3)]  # Рука второго игрока
        # self.player2_hand.append([card for card in random.sample(deck_boosts, 3)])
        # Бусты второго игрока (последний элемент списка (self.player1_hand - бусты в руке)

        x_pos = 1
        for i2 in self.player2_hand:
            self.coord_sp[1].append((size[0] // 10 * x_pos, size[1] * 0.2, i2))
            i2.rect.x = size[0] // 10 * x_pos
            x_pos += 2
            i2.rect.y = size[1] * 0.2
            self.sprites.add(i2)

        x_pos = 1
        for i in self.player1_hand:
            self.coord_sp[0].append((size[0] // 10 * x_pos, size[1] * 0.7, i))
            i.rect.x = size[0] // 10 * x_pos
            x_pos += 2
            i.rect.y = size[1] * 0.7
            self.sprites.add(i)

    # def boost_use(self, card_b, card_m):  # Использование буста на свою карту--
    # x, y = self.card_place(card_m)
    # card_b.using(self, x, y)
    # pass

    def attack(self, screen, card_my, card_other):  # Одна карта атакует другую
        if card_other.name == "Deleted":
            return
        if card_my.name == "Шалфей":  # Если атакует шалфей
            self.turn = random.randint(1, 2)
        else:  # Смена хода
            if self.turn == 1:
                self.turn = 0
            else:
                self.turn = 1
        if card_other.name not in ["Рад. Зомби ", "Задрот"]:
            card_other.cur_rad += card_my.rad

        if card_other.info == "Уворот" and random.randint(1, 2) == 1:
            return

        if card_my.name == "Гоша":
            card_other.hp -= random.randint(2, 7)
        else:
            card_other.hp -= card_my.dmg

        if card_other == "Жук" and card_other.hp <= 0:
            if self.turn == 0:
                for card in self.player1_field:
                    card.cur_rad += 1
            else:
                for card in self.player2_field:
                    card.cur_rad += 1
        card_other.updating()
        if card_other.hp <= 0 or card_other.cur_rad >= 7:
            if card_my.name == "Пожиратель":
                card_my.hp += 2
            if self.turn == 1:
                self.player1_hand.pop(self.player1_hand.index(card_other))
            else:
                self.player2_hand.pop(self.player2_hand.index(card_other))
            card_other.kill()
            card_other.name = "Deleted"
        self.death(screen, self.player2_hand, self.player1_hand)

    def death(self, screen, player2_hand, player1_hand):
        c = 0
        v = 0
        for i in player2_hand:
            if i.name == 'Delete':
                c += 1
            else:
                c += 0
        for j in player1_hand:
            if j.name == 'Delete':
                v += 1
            else:
                v += 0
        if c == len(player2_hand) or v == len(player1_hand):
            draw('GAME OVER', screen, x=100, y=185, size=400)
            self.turn = 99
            pygame.display.flip()
        else:
            pass

import pygame, random, os
from pygame.locals import *



""" VARIABLES """

FPS = 60
WIDTH = 1080
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
CYAN = (163, 227, 237)
GREEN = (0, 255, 0)


""" INIT """

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '250,100'              # window placement
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))           # window size
pygame.display.set_caption("Blackjack")
screen = pygame.display.get_surface()

font_big = pygame.font.Font("trebucit.ttf", 34)
font_button = pygame.font.Font("COPRGTL.TTF", 28)

background = "background.jpg"
random.seed()
card_sprites = pygame.image.load(os.path.join("deck.png")).convert_alpha()
dealers_cards = []
players_cards = []
buttons = []

deck = ["s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13",
        "h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13",
        "d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","d11","d12","d13",
        "c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13"]



""" CLASSES """

class Card:

    def __init__(self, target, facing, value, suite, position):
        self.target = target
        self.facing = facing            # when its dealers turn, change value of this
        self.value = value
        self.suite = suite
        self.position = position        # just x value, y fixed by dealer/player
        (self.x, self.y) = position     # as cards are added to table, move them closer: card.x -= 20
        self.draw()

    def draw(self):
        # choose sprite
        if self.facing == "down":
            self.card_sprite = card_sprites.subsurface(4*98, 4*144, 98, 144)

        else:
            self.card_sprite = card_sprites.subsurface((self.value-1)*98, (self.suite-1)*144, 98, 144)

        # position
        self.rect = self.card_sprite.get_rect()
        self.rect.topleft = self.position

        # blit sprite
        window.blit(self.card_sprite, self.rect)



class Button:

    def __init__(self, name, position):
        self.name = name                # button name
        self.hilite = False
        (self.x, self.y) = position
        self.pos = position
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_text()
        # Border
        self.surface = pygame.Surface((150, 40))
        self.surface.set_alpha(100)
        pygame.draw.rect(self.surface, BLACK, pygame.Rect((0, 0, self.x, self.y)), 1)
        pygame.draw.line(self.surface, WHITE, (1, 1), (self.x - 2, 1))
        pygame.draw.line(self.surface, WHITE, (1, 1), (1, self.y - 2))
        pygame.draw.line(self.surface, DARKGRAY, (1, self.y - 1), (self.x - 1, self.y - 1))
        pygame.draw.line(self.surface, DARKGRAY, (self.x - 1, 1), (self.x - 1, self.y - 1))
        pygame.draw.line(self.surface, GRAY, (2, self.y - 2), (self.x - 2, self.y - 2))
        pygame.draw.line(self.surface, GRAY, (self.x - 2, 2), (self.x - 2, self.y - 2))
        window.blit(self.surface, (self.x-10, self.y-5))
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.text, self.rect)

    def set_text(self):
        self.text = font_button.render(self.name, True, self.get_color())
        self.shadow = font_button.render(self.name, True, BLACK)

    def get_color(self):
        if self.hilite == True:
            return GREEN
        else:
            return CYAN

    def set_rect(self):
        self.set_text()
        #self.rect = self.text.get_rect()
        self.rect = pygame.Rect(self.x, self.y, 150, 40)    #fixed button size
        self.rect.topleft = self.pos
        #self.shadow_rect = self.text.get_rect()
        self.shadow_rect = pygame.Rect(self.x, self.y, 150, 40)
        self.shadow_rect.topleft = self.pos
        self.shadow_rect.move_ip(2, 3)    



""" FUNCTIONS """

def draw_text(message, font, color, position):
    text = font.render(message, True, color)
    shadow = font.render(message, True, BLACK)
    rect = text.get_rect()
    rect.topleft = position
    shadow_rect = text.get_rect()
    shadow_rect.topleft = position
    shadow_rect.move_ip(2, 3)
    window.blit(shadow, shadow_rect)
    window.blit(text, rect)


def deal_card(target, facing):

    global deck, dealers_cards, players_cards

    card_str = random.choice(deck)
    if card_str[0] == "s":
        suite = 1
    elif card_str[0] == "h":
        suite = 2
    elif card_str[0] == "d":
        suite = 3
    elif card_str[0] == "c":
        suite = 4
    cardvalue = int(card_str[1:])
    deck.remove(card_str)

    print(card_str)

    # Dealers face down card
    if facing == "down":
        face_down_card = card_str
        dealers_cards.append(Card("dealer", "down", cardvalue, suite, (250, 150)))
        
        # TODO: adjust coords afterwards by: object.x = object.x - 20
        #       so coords dont have to be hardcoded

    elif target == "player":
        players_cards.append(Card("player", "up", cardvalue, suite, (250, 400)))


#def shuffle():                                                 TODO


def handle_mouse_move():                                        # for button hiliting

    for button in buttons:
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.hilite = True
        else:
            button.hilite = False
        


""" MAIN """

def main():

    global buttons

    bg_image = pygame.image.load(os.path.join(background)).convert()


    # TESTING
    deal_card("dealer", "down")
    deal_card("player", "up")
    button1 = Button("Card", (850, 200))
    button2 = Button("Stay", (850, 250))

    buttons.append(button1)
    buttons.append(button2)


    while True:

        fpsClock.tick(FPS)
        window.blit(bg_image, (0, 0))   

        # TESTING
        draw_text("BLACKJACK", font_big, WHITE, (400, 50))
        for button in buttons:
            button.draw()
        for card in dealers_cards:
            card.draw()
        for card in players_cards:
            card.draw()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEMOTION:
                handle_mouse_move()

        pygame.display.update()


if __name__ == "__main__":
	main()

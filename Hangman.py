import pygame
import math
import random

from words import word_list

# setup display
pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  # all capital for constants that should not be changed
win = pygame.display.set_mode((WIDTH, HEIGHT - 64))
pygame.display.set_caption("Hangman Game!")

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# background
background = pygame.image.load("background.jpg")
imagerect = background.get_rect()

# button variables
RADIUS = 20
GAP = 15
letters = []  # [x, y, letter, visibility]
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = HEIGHT * 6 / 10
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# game variables
hangman_status = 0
guessed = []
FPS = 60
play = True
wins = 0
losses = 0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 130, 71)
GREY = (100, 100, 100)
YELLOW = (255, 252, 0)


def new_word():
    global word
    word = random.choice(word_list).upper()


def draw_bw_font(new, x, y):
    text = WORD_FONT.render(new, True, BLACK)
    text_back = WORD_FONT.render(new, True, WHITE)
    for i in range(3):
        for j in range(3):
            win.blit(text_back, (x + i - j, y + i - j))
    win.blit(text, (x, y))


def draw():
    # background
    win.blit(background, imagerect)

    # draw title
    text = TITLE_FONT.render("-- HANGMAN --", True, WHITE)
    margin = 12
    margin_double = 2 * margin
    h = text.get_height()
    w = text.get_width()
    pygame.draw.rect(win, WHITE,
                     ((WIDTH / 2 - w / 2 - margin), (60 - margin), (w + margin_double), (h + margin_double)), 3)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 60))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    draw_bw_font(display_word, WIDTH * 6 / 10, HEIGHT / 3)

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter  # unpacking, splitting up the variable
        if visible:
            pygame.draw.circle(win, WHITE, (x, y), RADIUS, 0)
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # hangman picture
    win.blit(images[hangman_status], (WIDTH * 3 / 10, HEIGHT / 4))
    pygame.display.update()


def display_message(messages, wait_before, wait_after):
    pygame.time.delay(wait_before)
    length = len(messages)
    win.blit(background, imagerect)
    for message in messages:
        text = WORD_FONT.render(message, True, WHITE)
        x = WIDTH / 2 - text.get_width() / 2
        y = HEIGHT / 2 - length * text.get_height() * (1 - messages.index(message))
        win.blit(text, (x, y))
    pygame.display.update()
    pygame.time.delay(wait_after)


def main():
    quit_game = False
    global hangman_status

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            global wins
            wins += 1
            display_message(["You Won!", "The word was: " + word], 1000, 2000)
            run = False

        if hangman_status == 6:
            global losses
            losses += 1
            display_message(["You lost suckerrrr!!!", "The word was: " + word], 1000, 3000)
            run = False
    if quit_game:
        return True
    else:
        return False


def reset_values():
    global word
    global guessed
    global letters
    global hangman_status
    new_word()
    guessed = []
    hangman_status = 0
    for letter in letters:
        letter[3] = True


while play:
    menu = True
    reset_values()
    main_clock = pygame.time.Clock()
    while menu:
        main_clock.tick(FPS)
        display_message(["Click anywhere to play.", "Wins: " + str(wins), "Losses: " + str(losses)], 0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
    if play:
        if main():
            play = False

pygame.quit()

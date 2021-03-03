import pygame, sys
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

RADIUS = 20
GAP = 15

letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i//13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

hangman_status = 0
words = ["HELLO", "PROGRAM", "PYTHON", "WORLD", "COMPUTER", "STRING", "GITHUB", "HANGMAN"]
guessed = []


def menu():
    global guessed

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        win.fill(WHITE)
        text = TITLE_FONT.render("Hangman Game", True, BLACK)
        win.blit(text, (WIDTH/2 - text.get_width() / 2, 20))
        pygame.draw.rect(win, BLACK, (300, 190, 200, 50))
        text = LETTER_FONT.render("Start game", True, WHITE)
        win.blit(text, (WIDTH/2 - text.get_width() / 2, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if m_x > 300 and m_y > 190:
                    if m_x < 500 and m_y < 240:
                        main()


def draw(word):
    win.fill(WHITE)

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    win.blit(text, (400, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def print_message(message):
    pygame.time.delay(800)
    win.fill(WHITE)
    text = WORD_FONT.render(message, True, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)


def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    for i in letters:
        i[3] = True

    guessed.clear()
    word = random.choice(words)
    hangman_status = 0

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    distance = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if distance < RADIUS:
                        letter[3] = False
                        if ltr not in word:
                            if ltr in guessed:
                                continue
                            hangman_status += 1
                        if ltr not in guessed:
                            guessed.append(ltr)
        draw(word)

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            print_message("You Won!")
            break

        if hangman_status == 6:
            print_message("You Lost!")
            break


menu()
pygame.quit()
sys.exit()
import pygame
import random

pygame.init()

# Constantes
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 153, 84)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)


PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20  # Raquette horizontale pour 1 joueur
PADDLE_WIDTH_2, PADDLE_HEIGHT_2 = 20, 100  # Raquette verticale pour 2 joueurs
BALL_SIZE = 20


# Chargement des images de fond
BACKGROUND_IMAGE_MENU = pygame.image.load('background_menu.jpg')
BACKGROUND_IMAGE_GAME = pygame.image.load('background_game.jpg')

# Chargement des polices
font = pygame.font.Font(None, 75)
small_font = pygame.font.Font(None, 50)
tall_font = pygame.font.Font(None, 100)
tall_font1 = pygame.font.Font(None, 150)
tall_font2 = pygame.font.Font(None, 200)
tall_font3 = pygame.font.Font(None, 250)
tall_font4 = pygame.font.Font(None, 300)
tall_font5 = pygame.font.Font(None, 35)
tall_font6 = pygame.font.Font(None, 400)

def draw_text_with_underline(text, font, color, x, y, underline_thickness=5):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    screen.blit(text_surface, text_rect)

    line_start_x = text_rect.left
    line_end_x = text_rect.right
    line_y = text_rect.bottom + 5
    pygame.draw.line(screen, color, (line_start_x, line_y), (line_end_x, line_y), underline_thickness)

def draw_button(text, font, color, rect):
    pygame.draw.rect(screen, color, rect)
    text_obj = font.render(text, True, WHITE)
    screen.blit(text_obj, (rect.x + (rect.width - text_obj.get_width()) // 2, rect.y + (rect.height - text_obj.get_height()) // 2))

def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x - text_obj.get_width() // 2, y - text_obj.get_height() // 2))

# Classe pour la raquette
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y, horizontal=True):
        super().__init__()
        if horizontal:
            self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        else:
            self.image = pygame.Surface((PADDLE_WIDTH_2, PADDLE_HEIGHT_2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.horizontal = horizontal

    def move(self, offset):
        if self.horizontal:
            if 0 <= self.rect.x + offset <= WIDTH - PADDLE_WIDTH:
                self.rect.x += offset
        else:
            if 0 <= self.rect.y + offset <= HEIGHT - PADDLE_HEIGHT_2:
                self.rect.y += offset

# Classe pour la balle
class Ball(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 50))
        self.speed_x = random.choice((-5, 5))
        self.speed_y = random.choice((-5, 5))

        # Ajuster la vitesse selon la difficulté
        if difficulty == "facile":
            self.speed_x *= 0.75
            self.speed_y *= 0.75
        elif difficulty == "moyen":
            self.speed_x *= 1
            self.speed_y *= 1
        elif difficulty == "difficile":
            self.speed_x *= 1.15
            self.speed_y *= 1.15
        elif difficulty == "très difficile":
            self.speed_x *= 1.299999
            self.speed_y *= 1.299999

    def update(self, is_double_mode=False):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def update(self, is_double_mode=False):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # En mode 1 joueur, si la balle touche le sol, le jeu se termine
        if not is_double_mode and self.rect.bottom >= HEIGHT:
            return True

        if not is_double_mode:
            if self.rect.top <= 0:
                self.speed_y = -self.speed_y
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speed_x = -self.speed_x
        else:
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                return True

            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.speed_y = -self.speed_y

        return False


# Fonction pour redémarrer une nouvelle partie (1 joueur)
def replay_single(difficulty, best_score):
    paddle = Paddle(RED, WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, horizontal=True)
    ball = Ball(difficulty)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle, ball)

    score = 0
    game_over = False
    paused = False

    pygame.mouse.set_visible(False)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, score
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-10)
            if keys[pygame.K_RIGHT]:
                paddle.move(10)

            result = ball.update()
            if result:
                game_over = True
                if score > best_score:
                    best_score = score

            if ball.rect.colliderect(paddle.rect):
                ball.speed_y = -ball.speed_y
                score += 1

            screen.blit(BACKGROUND_IMAGE_GAME, (0, 0))
            all_sprites.draw(screen)
            draw_text(f"Score: {score}", small_font, YELLOW, WIDTH // 2, 30)
        else:
            draw_text("PAUSE", tall_font6, YELLOW, WIDTH // 2, HEIGHT // 2.7)
            draw_text("Appuyez sur Espace pour reprendre", font, YELLOW, WIDTH // 2, HEIGHT // 1.5)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return True, score

# Fonction pour redémarrer une nouvelle partie (2 joueurs)
def replay_double(difficulty):
    paddle1 = Paddle(RED, 50, HEIGHT // 2 - PADDLE_HEIGHT_2 // 2, horizontal=False)
    paddle2 = Paddle(GREEN, WIDTH - 70, HEIGHT // 2 - PADDLE_HEIGHT_2 // 2, horizontal=False)
    ball = Ball(difficulty)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle1, paddle2, ball)

    score1 = 0
    score2 = 0
    game_over = False
    paused = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score1, score2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, score
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                paddle1.move(-10)
            if keys[pygame.K_w]:
                paddle1.move(10)
            if keys[pygame.K_UP]:
                paddle2.move(-10)
            if keys[pygame.K_DOWN]:
                paddle2.move(10)

            result = ball.update(is_double_mode=True)
            if result:
                game_over = True

            if ball.rect.colliderect(paddle1.rect):
                ball.speed_x = -ball.speed_x
                score1 += 1
            if ball.rect.colliderect(paddle2.rect):
                ball.speed_x = -ball.speed_x
                score2 += 1

            screen.blit(BACKGROUND_IMAGE_GAME, (0, 0))
            all_sprites.draw(screen)
            screen.blit(ball.image, ball.rect)
            draw_text(f"Score Joueur 1: {score1}", small_font, YELLOW, WIDTH // 2, 30)
            draw_text(f"Score Joueur 2: {score2}", small_font, YELLOW, WIDTH // 2, HEIGHT - 30)

        else:
            draw_text("PAUSE", tall_font6, YELLOW, WIDTH // 2, HEIGHT // 2.7)
            draw_text("Appuyez sur Espace pour reprendre", font, YELLOW, WIDTH // 2, HEIGHT // 1.5)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return True, score1, score2

# Écran de sélection de difficulté
def difficulty_menu():
    menu_running = True
    easy_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 80)
    medium_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 80)
    hard_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 80)
    very_hard_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 200, 300, 80)

    while menu_running:
        screen.blit(BACKGROUND_IMAGE_MENU, (0, 0))
        draw_text_with_underline(" Choisissez ", font, ORANGE, WIDTH // 2, HEIGHT // 6, underline_thickness=4)
        draw_text_with_underline(" la difficulté : ", font, ORANGE, WIDTH // 2, HEIGHT // 4, underline_thickness=4)
        draw_button("Facile", small_font, GREEN, easy_button)
        draw_button("Moyen", small_font, YELLOW, medium_button)
        draw_button("Difficile", small_font, RED, hard_button)
        draw_button("Très Difficile", small_font, PURPLE, very_hard_button)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return "facile"
                if medium_button.collidepoint(event.pos):
                    return "moyen"
                if hard_button.collidepoint(event.pos):
                    return "difficile"
                if very_hard_button.collidepoint(event.pos):
                    return "très difficile"

def end_screen(score1, score2, is_double_mode):
    end_running = True
    replay_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 120, 300, 80)
    menu_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 240, 300, 80)

    pygame.mouse.set_visible(True)

    while end_running:
        screen.blit(BACKGROUND_IMAGE_MENU, (0, 0))
        draw_text_with_underline("Partie Terminée", tall_font, ORANGE, WIDTH // 2, HEIGHT // 4, underline_thickness=7)

        if is_double_mode:
            draw_text(f"Score Joueur 1: {score1}", small_font, YELLOW, WIDTH // 2, HEIGHT // 2 - 30)
            draw_text(f"Score Joueur 2: {score2}", small_font, YELLOW, WIDTH // 2, HEIGHT // 2 + 30)

            if score1 < score2:
                draw_text("Le joueur 2 a gagné !!!", font, YELLOW, WIDTH // 2, HEIGHT // 2 - 110)
            elif score1 == score2:
                draw_text("Les 2 joueurs sont ex-aequo !!!", font, YELLOW, WIDTH // 2, HEIGHT // 2 - 110)
            else:
                draw_text("Le joueur 1 a gagné !!!", font, YELLOW, WIDTH // 2, HEIGHT // 2 - 110)
        else:
            draw_text(f"Score: {score1}", tall_font, YELLOW, WIDTH // 2, HEIGHT // 2)

        draw_button("Rejouer", small_font, GREEN, replay_button)
        draw_button("Menu principal", small_font, RED, menu_button)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return True, False
                if menu_button.collidepoint(event.pos):
                    return False, True

# Dictionnaire des traductions
translations = {
    "fr": {
        "title": "PONG",
        "single_player": "Jouer seul",
        "double_player": "Jouer à 2",
        "quit": "Quitter",
        "settings": "Paramètres",
        "choose_difficulty": "Choisissez la difficulté :",
        "easy": "Facile",
        "medium": "Moyen",
        "hard": "Difficile",
        "very_hard": "Très Difficile",
        "game_over": "Partie Terminée",
        "replay": "Rejouer",
        "main_menu": "Menu principal²"

    },
    "en": {
        "title": "PONG",
        "single_player": "Play Alone",
        "double_player": "Play 2",
        "quit": "Quit",
        "settings": "Settings",
        "choose_difficulty": "Choose the difficulty:",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "very_hard": "Very Hard",
        "game_over": "Game Over",
        "replay": "Replay",
        "main_menu": "Main Menu"
        #"choisir_une_langue":"choose a language"
    },
    "it": {
        "title": "PONG",
        "single_player": "Giocare da solo",
        "double_player": "Giocare a 2",
        "quit": "Uscire",
        "settings": "Impostazioni",
        "choose_difficulty": "Scegli la difficoltà:",
        "easy": "Facile",
        "medium": "Medio",
        "hard": "Difficile",
        "very_hard": "Molto Difficile",
        "game_over": "Gioco Finito",
        "replay": "Rigiocare",
        "main_menu": "Menu principale"
    },
    "es": {
        "title": "PONG",
        "single_player": "Jugar solo",
        "double_player": "Jugar a 2",
        "quit": "Salir",
        "settings": "Configuraciones",
        "choose_difficulty": "Elige la dificultad:",
        "easy": "Fácil",
        "medium": "Medio",
        "hard": "Difícil",
        "very_hard": "Muy Difícil",
        "game_over": "Juego Terminado",
        "replay": "Repetir",
        "main_menu": "Menú principal"
    },
}

# Variable pour la langue sélectionnée
selected_language = "fr"

# Fonction pour le menu de sélection de langue
def language_menu():
    global selected_language
    menu_running = True
    french_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 80)
    english_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 80)
    italian_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 80)
    spanish_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 200, 300, 80)

    while menu_running:
        screen.blit(BACKGROUND_IMAGE_MENU, (0, 0))
        draw_text_with_underline("Choisissez la langue :", font, ORANGE, WIDTH // 2, HEIGHT // 6, underline_thickness=4)
        draw_button("Français", small_font, GREEN, french_button)
        draw_button("English", small_font, YELLOW, english_button)
        draw_button("Italiano", small_font, RED, italian_button)
        draw_button("Español", small_font, PURPLE, spanish_button)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if french_button.collidepoint(event.pos):
                    selected_language = "fr"
                    return
                if english_button.collidepoint(event.pos):
                    selected_language = "en"
                    return
                if italian_button.collidepoint(event.pos):
                    selected_language = "it"
                    return
                if spanish_button.collidepoint(event.pos):
                    selected_language = "es"
                    return

# Modification de la fonction main_menu
def main_menu():
    menu_running = True
    solo_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 80)
    double_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 80)
    parametre_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 120, 300, 80)
    language_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 220, 300, 80)
    quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 320, 300, 80)

    pygame.mouse.set_visible(True)

    while menu_running:
        screen.blit(BACKGROUND_IMAGE_MENU, (0, 0))
        draw_text_with_underline(translations[selected_language]["title"], tall_font1, ORANGE, WIDTH // 2, HEIGHT // 4, underline_thickness=8)
        draw_button(translations[selected_language]["single_player"], small_font, GREEN, solo_button)
        draw_button(translations[selected_language]["double_player"], small_font, YELLOW, double_button)
        draw_button(translations[selected_language]["settings"], small_font, GRAY, parametre_button)
        draw_button("Choisir la langue", small_font, PURPLE, language_button)
        draw_button(translations[selected_language]["quit"], small_font, RED, quit_button)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo_button.collidepoint(event.pos):
                    return "jouer_seul"
                if double_button.collidepoint(event.pos):
                    return "jouer_2"
                if parametre_button.collidepoint(event.pos):
                    return "Paramètres"
                if language_button.collidepoint(event.pos):
                    language_menu()
                if quit_button.collidepoint(event.pos):
                    return False

running = True
while running:
    result = main_menu()
    if not result:
        break

    if result == "jouer_seul":
        best_score = 0
        difficulty = difficulty_menu()
        if difficulty is None:
            break
        game_over, score = replay_single(difficulty, best_score)

        while game_over:
            rejouer, retour_menu = end_screen(score, 0, is_double_mode=False)
            if retour_menu:
                break
            if rejouer:
                game_over, score = replay_single(difficulty, best_score)

    elif result == "jouer_2":
        difficulty = difficulty_menu()
        if difficulty is None:
            break
        game_over, score1, score2 = replay_double(difficulty)

        while game_over:
            rejouer, retour_menu = end_screen(score1, score2, is_double_mode=True)
            if retour_menu:
                break
            if rejouer:
                game_over, score1, score2 = replay_double(difficulty)

pygame.quit()
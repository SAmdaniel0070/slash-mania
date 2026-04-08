import pygame
import random
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# ================== CONFIG ==================
WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slash Mania")
clock = pygame.time.Clock()

# ================== PATHS ==================
BASE_DIR = os.path.dirname(__file__)

FONT_PATH = os.path.join(BASE_DIR, "font", "PressStart2P-Regular.ttf")
IMG_DIR = os.path.join(BASE_DIR, "images")
SND_DIR = os.path.join(BASE_DIR, "sounds")

# ================== LOAD SOUNDS ==================
throw_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "throw.mp3"))
slash_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "slash sound of knife.mp3"))
bomb_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "bomb.mp3"))

pygame.mixer.music.load(os.path.join(SND_DIR, "main bg loop.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_muted = False

# ================== LOAD IMAGES ==================
menu_bg = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "background.png")),
    (WIDTH, HEIGHT)
)

game_bg = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "background.png")),
    (WIDTH, HEIGHT)
)

knife = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "knife.png")),
    (70, 70)
)

bomb_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "bommb.png")),
    (90, 90)
)

mute_icon = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "mute.png")),
    (45, 45)
)

unmute_icon = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_DIR, "unmute.png")),
    (45, 45)
)

fruit_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "apple.png")), (90, 90)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "banana.png")), (90, 90)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "watermelon.png")), (90, 90))
]

# ================== FONTS ==================
title_font = pygame.font.Font(FONT_PATH, 50)
button_font = pygame.font.Font(FONT_PATH, 20)
score_font = pygame.font.Font(FONT_PATH, 16)

pygame.mouse.set_visible(False)

# ================== VARIABLES ==================
game_state = "menu"
score = 0
combo = 0

spawn_timer = 0
spawn_delay = 50

fruits = []
bombs = []

throw_count = 0
next_bomb_throw = random.randint(3, 4)

# ================== BUTTONS ==================
start_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 60)
restart_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 80, 300, 60)
mute_btn = pygame.Rect(WIDTH - 65, 15, 50, 50)

# ================== FUNCTIONS ==================

def draw_panel(x, y, w, h, alpha=180):
    panel = pygame.Surface((w, h))
    panel.set_alpha(alpha)
    panel.fill((0, 0, 0))
    screen.blit(panel, (x, y))


def reset_game():
    global score, combo, spawn_delay, throw_count, next_bomb_throw
    score = 0
    combo = 0
    spawn_delay = 50
    throw_count = 0
    next_bomb_throw = random.randint(3, 4)
    fruits.clear()
    bombs.clear()


def spawn_fruit():
    img = random.choice(fruit_images)
    fruits.append([img, random.randint(100, WIDTH-100), HEIGHT, random.uniform(-3,3), random.uniform(-20,-18)])
    throw_sound.play()


def spawn_bomb():
    bombs.append([random.randint(100, WIDTH-100), HEIGHT, random.uniform(-3,3), random.uniform(-18,-14)])


def toggle_music():
    global music_muted
    music_muted = not music_muted
    pygame.mixer.music.set_volume(0 if music_muted else 0.5)


# ================== GAME LOOP ==================

running = True
while running:
    clock.tick(FPS)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_x, mouse_y, 20, 20)

    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

            if mute_btn.collidepoint(event.pos):
                toggle_music()

    # ================== MENU ==================
    if game_state == "menu":
        screen.blit(menu_bg, (0, 0))

        draw_panel(WIDTH//2 - 260, HEIGHT//2 - 170, 520, 120)

        title = title_font.render("SLASH MANIA", True, (255, 80, 80))
        screen.blit(title, (WIDTH//2 - 270, HEIGHT//2 - 150))

        pygame.draw.rect(screen, (255, 200, 0), start_btn)
        screen.blit(button_font.render("START GAME", True, (0,0,0)), (WIDTH//2 - 110, HEIGHT//2 + 18))

        if click and start_btn.collidepoint(mouse_x, mouse_y):
            game_state = "playing"

    # ================== GAME ==================
    elif game_state == "playing":
        screen.blit(game_bg, (0, 0))

        spawn_timer += 1

        if spawn_timer > spawn_delay:
            spawn_timer = 0
            throw_count += 1

            for _ in range(random.randint(2,4)):
                spawn_fruit()

            if throw_count >= next_bomb_throw:
                spawn_bomb()
                throw_count = 0
                next_bomb_throw = random.randint(3,4)

        # Fruits
        for f in fruits[:]:
            f[4] += 0.5
            f[1] += f[3]
            f[2] += f[4]

            rect = pygame.Rect(f[1], f[2], 90, 90)

            if f[2] > HEIGHT:
                fruits.remove(f)
                combo = 0

            elif mouse_rect.colliderect(rect):
                fruits.remove(f)
                combo += 1
                score += combo
                slash_sound.play()

            else:
                screen.blit(f[0], (f[1], f[2]))

        # Bombs
        for b in bombs[:]:
            b[3] += 0.5
            b[0] += b[2]
            b[1] += b[3]

            rect = pygame.Rect(b[0], b[1], 70, 70)

            if b[1] > HEIGHT:
                bombs.remove(b)

            elif mouse_rect.colliderect(rect):
                bomb_sound.play()
                game_state = "game_over"

            else:
                screen.blit(bomb_image, (b[0], b[1]))

        # UI
        draw_panel(5, 5, 150, 30)
        draw_panel(5, 40, 150, 30)

        screen.blit(score_font.render(f"SCORE: {score}", True, (255,255,255)), (10,10))
        screen.blit(score_font.render(f"COMBO: x{combo}", True, (255,200,0)), (10,45))

    # ================== GAME OVER ==================
    elif game_state == "game_over":
        screen.blit(game_bg, (0, 0))

        draw_panel(0, 0, WIDTH, HEIGHT, 200)

        text = title_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 150))

        screen.blit(button_font.render(f"SCORE: {score}", True, (255,255,255)), (WIDTH//2 - 100, HEIGHT//2 - 20))

        pygame.draw.rect(screen, (0,255,150), restart_btn)
        screen.blit(button_font.render("SLICE AGAIN", True, (0,0,0)), (WIDTH//2 - 120, HEIGHT//2 + 100))

        if click and restart_btn.collidepoint(mouse_x, mouse_y):
            reset_game()
            game_state = "playing"

    # ================== UI ==================
    screen.blit(mute_icon if music_muted else unmute_icon, (WIDTH - 60, 20))
    screen.blit(knife, (mouse_x, mouse_y))

    pygame.display.update()

pygame.quit()
import pygame
from forest_fire_cellular_automaton import forest

pygame.init()

height = 400
width = 400
scale = 2

genesis_probability = 0.005
f = 1 / 100.0
combustion_probability = genesis_probability * f

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

padding = 10
bar_height = 15
bar_spacing = 10
text_spacing = 5
label_width = 95
panel_gap = 5


def create_forest():
    return forest(
        int(width / scale),
        int(height / scale),
        genesis_probability,
        combustion_probability,
        1
    )


def draw_bar(surface, font, label, ratio, color, y, total_width):
    label_text = font.render(label, True, (255, 255, 255))
    surface.blit(label_text, (padding, y - 2))

    bar_x = padding + label_width
    bar_width = total_width - bar_x - padding
    pygame.draw.rect(surface, (70, 70, 70), (bar_x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (140, 140, 140), (bar_x, y, bar_width, bar_height), 1)

    fill_width = int(bar_width * ratio)
    if fill_width > 0:
        pygame.draw.rect(surface, color, (bar_x, y, fill_width, bar_height))

    percent_text = font.render(f"{ratio * 100:.1f}%", True, (220, 220, 220))
    percent_rect = percent_text.get_rect()
    percent_rect.midright = (bar_x + bar_width - 6, y + bar_height // 2)
    surface.blit(percent_text, percent_rect)

    return y + bar_height + bar_spacing


sample_text = font.render("Sample", True, (255, 255, 255))
text_height = sample_text.get_height()
bars_total_height = 3 * bar_height + 2 * bar_spacing
text_total_height = 2 * text_height + text_spacing
ui_height = padding * 2 + bars_total_height + panel_gap + text_total_height + padding

total_height = height + ui_height
surface = pygame.display.set_mode((width, total_height))
pygame.display.set_caption("Forest Fire Model")

sherwood_forest = create_forest()
running = True
paused = False
fps = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                fps = min(120, fps + 5)
            elif event.key == pygame.K_DOWN:
                fps = max(1, fps - 5)
            elif event.key == pygame.K_r:
                sherwood_forest = create_forest()

    if not paused:
        sherwood_forest.update()

    surface.fill((0, 0, 0))

    for row in range(len(sherwood_forest.automaton_array)):
        for column in range(len(sherwood_forest.automaton_array[row])):
            state = sherwood_forest.automaton_array[row][column]

            if state == 0:
                color = (0, 0, 0)
            elif state == 1:
                color = (0, 255, 0)
            elif state == 2:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)

            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(scale * column, scale * row, scale, scale)
            )

    pygame.draw.rect(surface, (25, 25, 25), (0, height, width, ui_height))
    pygame.draw.line(surface, (90, 90, 90), (0, height), (width, height), 1)

    alive, burning, dead, total = sherwood_forest.count_states()
    if total > 0:
        alive_ratio = alive / total
        burning_ratio = burning / total
        dead_ratio = dead / total
    else:
        alive_ratio = 0
        burning_ratio = 0
        dead_ratio = 0

    y = height + padding
    y = draw_bar(surface, font, "Alive", alive_ratio, (0, 255, 0), y, width)
    y = draw_bar(surface, font, "Burning", burning_ratio, (255, 0, 0), y, width)
    y = draw_bar(surface, font, "Dead", dead_ratio, (90, 90, 90), y, width)

    y += panel_gap

    stats_text = font.render(
        f"Speed: {fps}   Paused: {'Yes' if paused else 'No'}",
        True,
        (255, 255, 255)
    )
    surface.blit(stats_text, (padding, y))
    y += text_height + text_spacing

    controls_text = font.render(
        "Space: pause/resume   Up/Down: speed   R: reset",
        True,
        (255, 255, 255)
    )
    surface.blit(controls_text, (padding, y))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

import pygame
import sys
import random
import math

# -----------------------------
# Optimal Thief - Full HD Version
# -----------------------------

pygame.init()
pygame.display.set_caption("Optimal Thief")

# -----------------------------
# Display settings
# -----------------------------
FULLSCREEN = False  # Change to True for actual fullscreen

if FULLSCREEN:
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    WIDTH, HEIGHT = 1920, 1080
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

CLOCK = pygame.time.Clock()

# Colors
BG = (18, 18, 24)
PANEL = (28, 30, 40)
CARD = (38, 42, 56)
CARD_HOVER = (50, 56, 74)
CARD_SELECTED = (74, 120, 84)
TEXT = (235, 235, 240)
SUBTEXT = (180, 185, 195)
ACCENT = (255, 201, 87)
DANGER = (220, 80, 80)
SUCCESS = (90, 200, 120)
BUTTON = (70, 110, 200)
BUTTON_HOVER = (90, 130, 220)
OUTLINE = (95, 100, 120)
WHITE = (255, 255, 255)

# Fonts optimized for Full HD
TITLE_FONT = pygame.font.SysFont("arial", 68, bold=True)
HEADER_FONT = pygame.font.SysFont("arial", 40, bold=True)
FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 22)
TINY_FONT = pygame.font.SysFont("arial", 18)
CREDIT_FONT = pygame.font.SysFont("arial", 22, bold=True)

# Layout constants
MARGIN = 42
GAP = 34
PANEL_PAD = 24
PANEL_RADIUS = 18

# Puzzle sets
PUZZLES = [
    {
        "capacity": 10,
        "items": [
            {"name": "Gold Ring", "weight": 2, "value": 6},
            {"name": "Laptop", "weight": 5, "value": 10},
            {"name": "Painting", "weight": 6, "value": 12},
            {"name": "Watch", "weight": 3, "value": 7},
        ],
    },
    {
        "capacity": 12,
        "items": [
            {"name": "Necklace", "weight": 4, "value": 9},
            {"name": "Tablet", "weight": 3, "value": 7},
            {"name": "Camera", "weight": 5, "value": 11},
            {"name": "Silver Coin Set", "weight": 2, "value": 5},
            {"name": "Rare Book", "weight": 4, "value": 8},
        ],
    },
    {
        "capacity": 11,
        "items": [
            {"name": "Ruby Crown", "weight": 6, "value": 14},
            {"name": "Pearl Bracelet", "weight": 3, "value": 8},
            {"name": "Antique Clock", "weight": 5, "value": 10},
            {"name": "Diamond Brooch", "weight": 2, "value": 6},
            {"name": "Mini Safe", "weight": 4, "value": 9},
        ],
    },
]


def wrap_text(text, font, max_width):
    words = text.split(" ")
    if not words:
        return [""]

    lines = []
    current = words[0]

    for word in words[1:]:
        test = current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def draw_text(surface, text, font, color, x, y, max_width=None, line_gap=4):
    if max_width is None:
        rendered = font.render(text, True, color)
        surface.blit(rendered, (x, y))
        return y + rendered.get_height()

    lines = wrap_text(text, font, max_width)
    yy = y
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, yy))
        yy += font.get_linesize() + line_gap
    return yy - line_gap


def draw_credit(surface):
    credit_text = "Made by Badar Khalid"
    rendered = CREDIT_FONT.render(credit_text, True, ACCENT)
    rect = rendered.get_rect(topright=(surface.get_width() - 40, 30))
    surface.blit(rendered, rect)


def draw_panel(surface, rect):
    pygame.draw.rect(surface, PANEL, rect, border_radius=PANEL_RADIUS)
    pygame.draw.rect(surface, OUTLINE, rect, 2, border_radius=PANEL_RADIUS)


def draw_item_list(surface, items, x, y, width, height, font, color, empty_text="No items."):
    if not items:
        draw_text(surface, empty_text, font, color, x, y, max_width=width)
        return

    line_height = font.get_linesize() + 6
    yy = y
    bottom = y + height

    for item in items:
        line = f"- {item['name']} (W:{item['weight']} V:{item['value']})"
        wrapped = wrap_text(line, font, width)
        needed = len(wrapped) * line_height

        if yy + needed > bottom:
            if yy + font.get_linesize() <= bottom:
                surface.blit(font.render("...", True, color), (x, yy))
            break

        for wrapped_line in wrapped:
            surface.blit(font.render(wrapped_line, True, color), (x, yy))
            yy += line_height


class Button:
    def __init__(self, rect, text, bg=BUTTON, hover=BUTTON_HOVER, fg=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg = bg
        self.hover = hover
        self.fg = fg

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mouse_pos) else self.bg
        pygame.draw.rect(surface, color, self.rect, border_radius=13)
        pygame.draw.rect(surface, OUTLINE, self.rect, 2, border_radius=13)

        txt = FONT.render(self.text, True, self.fg)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class ItemCard:
    def __init__(self, item):
        self.item = item
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.selected = False

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        color = CARD_SELECTED if self.selected else CARD_HOVER if hovered else CARD
        pygame.draw.rect(surface, color, self.rect, border_radius=16)
        pygame.draw.rect(surface, OUTLINE, self.rect, 2, border_radius=16)

        checkbox_size = 30
        box_x = self.rect.x + 20
        box_y = self.rect.y + 20
        box = pygame.Rect(box_x, box_y, checkbox_size, checkbox_size)
        pygame.draw.rect(surface, WHITE, box, 2, border_radius=6)

        if self.selected:
            pygame.draw.line(surface, ACCENT, (box.x + 6, box.y + 15), (box.x + 12, box.y + 22), 4)
            pygame.draw.line(surface, ACCENT, (box.x + 12, box.y + 22), (box.x + 24, box.y + 8), 4)

        text_x = self.rect.x + 66
        name_y = self.rect.y + 12
        meta_y = self.rect.y + 58

        draw_text(surface, self.item["name"], HEADER_FONT, TEXT, text_x, name_y, max_width=self.rect.width - 90)
        draw_text(
            surface,
            f"Weight: {self.item['weight']}    Value: {self.item['value']}",
            FONT,
            SUBTEXT,
            text_x,
            meta_y,
            max_width=self.rect.width - 90,
        )

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = not self.selected
            return True
        return False


def compute_best_solution(items, capacity):
    n = len(items)
    best_value = -1
    best_weight = 0
    best_mask = 0

    for mask in range(1 << n):
        total_weight = 0
        total_value = 0

        for i in range(n):
            if mask & (1 << i):
                total_weight += items[i]["weight"]
                total_value += items[i]["value"]

        if total_weight <= capacity:
            if total_value > best_value:
                best_value = total_value
                best_weight = total_weight
                best_mask = mask
            elif total_value == best_value and total_weight < best_weight:
                best_weight = total_weight
                best_mask = mask

    chosen = []
    for i in range(n):
        if best_mask & (1 << i):
            chosen.append(items[i])

    return {
        "value": best_value,
        "weight": best_weight,
        "items": chosen,
    }


def get_selected_totals(cards):
    total_weight = sum(card.item["weight"] for card in cards if card.selected)
    total_value = sum(card.item["value"] for card in cards if card.selected)
    selected_items = [card.item for card in cards if card.selected]
    return total_weight, total_value, selected_items


def start_new_round():
    puzzle = random.choice(PUZZLES)
    items = puzzle["items"]
    capacity = puzzle["capacity"]
    best = compute_best_solution(items, capacity)

    cards = [ItemCard(item) for item in items]

    return {
        "capacity": capacity,
        "items": items,
        "cards": cards,
        "best": best,
    }


def make_result(selected_weight, selected_value, selected_items, capacity, best):
    overweight = selected_weight > capacity
    near_best_threshold = math.ceil(best["value"] * 0.85)

    if overweight:
        return {
            "win": False,
            "title": "Caught! Your bag was too heavy.",
            "message": "You exceeded the bag capacity.",
            "selected_weight": selected_weight,
            "selected_value": selected_value,
            "selected_items": selected_items,
        }

    if selected_value == best["value"]:
        return {
            "win": True,
            "title": "Perfect Heist!",
            "message": "You found the optimal combination.",
            "selected_weight": selected_weight,
            "selected_value": selected_value,
            "selected_items": selected_items,
        }

    if selected_value >= near_best_threshold:
        return {
            "win": True,
            "title": "Nice Job!",
            "message": "Your selection is valid and near the best possible value.",
            "selected_weight": selected_weight,
            "selected_value": selected_value,
            "selected_items": selected_items,
        }

    return {
        "win": False,
        "title": "Not Quite Optimal",
        "message": "Your bag was valid, but the value was too low.",
        "selected_weight": selected_weight,
        "selected_value": selected_value,
        "selected_items": selected_items,
    }


def layout_title_ui(start_button):
    sw, sh = SCREEN.get_size()

    button_w, button_h = 280, 72
    start_button.set_rect(((sw - button_w) // 2, sh - 120, button_w, button_h))

    panel_top = 220
    panel_bottom = start_button.rect.y - 36
    panel = pygame.Rect(80, panel_top, sw - 160, panel_bottom - panel_top)

    return {"panel": panel}


def layout_play_ui(round_data, confirm_button):
    sw, sh = SCREEN.get_size()

    content_top = 170
    content_bottom_margin = 36
    content_h = sh - content_top - content_bottom_margin

    left_w = int((sw - MARGIN * 2 - GAP) * 0.62)
    right_w = sw - MARGIN * 2 - GAP - left_w

    left_panel = pygame.Rect(MARGIN, content_top, left_w, content_h)
    right_panel = pygame.Rect(left_panel.right + GAP, content_top, right_w, content_h)

    inner = left_panel.inflate(-PANEL_PAD * 2, -PANEL_PAD * 2)
    cards_top = inner.y + 60
    cards_area_h = inner.bottom - cards_top
    card_gap = 18
    n = len(round_data["cards"])

    if n > 0:
        max_card_h = 130
        min_card_h = 92
        card_h = (cards_area_h - card_gap * (n - 1)) // n
        card_h = max(min_card_h, min(max_card_h, card_h))
        total_used = n * card_h + (n - 1) * card_gap
        start_y = cards_top + max(0, (cards_area_h - total_used) // 2)

        for i, card in enumerate(round_data["cards"]):
            y = start_y + i * (card_h + card_gap)
            card.set_rect((inner.x, y, inner.width, card_h))

    right_inner = right_panel.inflate(-PANEL_PAD * 2, -PANEL_PAD * 2)
    button_w, button_h = 220, 68
    confirm_y = right_inner.bottom - 140
    confirm_button.set_rect((right_inner.centerx - button_w // 2, confirm_y, button_w, button_h))

    return {
        "left_panel": left_panel,
        "right_panel": right_panel,
    }


def layout_result_ui(play_again_button, quit_button):
    sw, sh = SCREEN.get_size()

    content_top = 210
    buttons_y = sh - 115
    footer_y = buttons_y - 58
    panels_h = footer_y - content_top - 24

    panel_gap = 42
    left_w = (sw - 2 * 70 - panel_gap) // 2
    right_w = left_w

    left_panel = pygame.Rect(70, content_top, left_w, panels_h)
    right_panel = pygame.Rect(left_panel.right + panel_gap, content_top, right_w, panels_h)

    button_gap = 30
    play_w, play_h = 220, 60
    quit_w, quit_h = 170, 60
    total_buttons_w = play_w + button_gap + quit_w
    start_x = (sw - total_buttons_w) // 2

    play_again_button.set_rect((start_x, buttons_y, play_w, play_h))
    quit_button.set_rect((start_x + play_w + button_gap, buttons_y, quit_w, quit_h))

    return {
        "left_panel": left_panel,
        "right_panel": right_panel,
        "footer_y": footer_y,
    }


def draw_title_screen(start_button, layout):
    SCREEN.fill(BG)
    draw_credit(SCREEN)

    draw_text(SCREEN, "Optimal Thief", TITLE_FONT, ACCENT, 80, 60)
    draw_text(
        SCREEN,
        "Pick the best combination of items without exceeding your bag's capacity.",
        FONT,
        TEXT,
        80,
        145,
        max_width=1500,
    )

    panel = layout["panel"]
    draw_panel(SCREEN, panel)

    inner_x = panel.x + 32
    y = panel.y + 28

    y = draw_text(SCREEN, "How to Play", HEADER_FONT, TEXT, inner_x, y)
    y += 20

    instructions = [
        "1. Each item has a weight and a value.",
        "2. Click items to add or remove them from your bag.",
        "3. Watch your running total weight and value.",
        "4. Press CONFIRM when you are done.",
        "5. If your total weight is above capacity, you lose.",
        "6. If your set is the best or near the best, you win.",
        "7. The game also shows the true best answer found by brute force.",
    ]

    for line in instructions:
        y = draw_text(SCREEN, line, FONT, SUBTEXT, inner_x + 12, y, max_width=panel.width - 64)
        y += 12

    y += 8
    draw_text(
        SCREEN,
        "Learning topic: Knapsack Problem, optimization, and brute-force thinking.",
        SMALL_FONT,
        ACCENT,
        inner_x,
        y,
        max_width=panel.width - 64,
    )

    start_button.draw(SCREEN)


def draw_game_screen(round_data, confirm_button, layout):
    SCREEN.fill(BG)
    draw_credit(SCREEN)

    draw_text(SCREEN, "Optimal Thief", TITLE_FONT, ACCENT, 60, 48)
    draw_text(SCREEN, "Choose the items you want to steal.", FONT, SUBTEXT, 62, 125)

    left_panel = layout["left_panel"]
    right_panel = layout["right_panel"]

    draw_panel(SCREEN, left_panel)
    draw_panel(SCREEN, right_panel)

    draw_text(SCREEN, "Items", HEADER_FONT, TEXT, left_panel.x + 24, left_panel.y + 18)

    for card in round_data["cards"]:
        card.draw(SCREEN)

    inner = right_panel.inflate(-PANEL_PAD * 2, -PANEL_PAD * 2)
    capacity = round_data["capacity"]
    total_weight, total_value, selected_items = get_selected_totals(round_data["cards"])

    y = inner.y
    y = draw_text(SCREEN, "Bag Status", HEADER_FONT, TEXT, inner.x, y)
    y += 24

    y = draw_text(SCREEN, f"Capacity: {capacity}", FONT, ACCENT, inner.x, y)
    y += 22

    weight_color = DANGER if total_weight > capacity else TEXT
    y = draw_text(SCREEN, f"Total Weight: {total_weight}", FONT, weight_color, inner.x, y)
    y += 14
    y = draw_text(SCREEN, f"Total Value: {total_value}", FONT, SUCCESS, inner.x, y)
    y += 28

    bar_bg = pygame.Rect(inner.x, y, inner.width, 30)
    pygame.draw.rect(SCREEN, CARD, bar_bg, border_radius=15)

    fill_ratio = min(total_weight / capacity, 1.0) if capacity > 0 else 0
    fill_w = int(bar_bg.width * fill_ratio)
    fill_color = DANGER if total_weight > capacity else ACCENT

    pygame.draw.rect(
        SCREEN,
        fill_color,
        (bar_bg.x, bar_bg.y, fill_w, bar_bg.height),
        border_radius=15,
    )
    pygame.draw.rect(SCREEN, OUTLINE, bar_bg, 2, border_radius=15)

    y = bar_bg.bottom + 34
    y = draw_text(SCREEN, "Selected Items:", FONT, TEXT, inner.x, y)
    y += 16

    list_bottom = confirm_button.rect.y - 28
    list_height = max(60, list_bottom - y)

    draw_item_list(
        SCREEN,
        selected_items,
        inner.x + 10,
        y,
        inner.width - 16,
        list_height,
        SMALL_FONT,
        SUBTEXT,
        empty_text="No items selected yet.",
    )

    confirm_button.draw(SCREEN)

    draw_text(
        SCREEN,
        "Try to maximize value without going over capacity.",
        TINY_FONT,
        SUBTEXT,
        inner.x,
        confirm_button.rect.bottom + 16,
        max_width=inner.width,
    )


def draw_result_screen(result, round_data, play_again_button, quit_button, layout):
    SCREEN.fill(BG)
    draw_credit(SCREEN)

    title_color = SUCCESS if result["win"] else DANGER
    draw_text(SCREEN, result["title"], TITLE_FONT, title_color, 70, 55)
    draw_text(SCREEN, result["message"], FONT, TEXT, 72, 140, max_width=1600)

    left = layout["left_panel"]
    right = layout["right_panel"]
    footer_y = layout["footer_y"]

    draw_panel(SCREEN, left)
    draw_panel(SCREEN, right)

    inner_left = left.inflate(-22, -22)
    y = inner_left.y

    y = draw_text(SCREEN, "Your Selection", HEADER_FONT, TEXT, inner_left.x, y)
    y += 22

    y = draw_text(
        SCREEN,
        f"Weight: {result['selected_weight']} / {round_data['capacity']}",
        FONT,
        DANGER if result["selected_weight"] > round_data["capacity"] else TEXT,
        inner_left.x,
        y,
    )
    y += 14
    y = draw_text(SCREEN, f"Value: {result['selected_value']}", FONT, SUCCESS, inner_left.x, y)
    y += 26
    y = draw_text(SCREEN, "Items:", FONT, TEXT, inner_left.x, y)
    y += 14

    draw_item_list(
        SCREEN,
        result["selected_items"],
        inner_left.x + 10,
        y,
        inner_left.width - 16,
        inner_left.bottom - y,
        SMALL_FONT,
        SUBTEXT,
        empty_text="No items chosen.",
    )

    best = round_data["best"]
    inner_right = right.inflate(-22, -22)
    y = inner_right.y

    y = draw_text(SCREEN, "Best Answer (Brute Force)", HEADER_FONT, TEXT, inner_right.x, y)
    y += 22
    y = draw_text(SCREEN, f"Best Weight: {best['weight']}", FONT, TEXT, inner_right.x, y)
    y += 14
    y = draw_text(SCREEN, f"Best Value: {best['value']}", FONT, ACCENT, inner_right.x, y)
    y += 26
    y = draw_text(SCREEN, "Best Items:", FONT, TEXT, inner_right.x, y)
    y += 14

    draw_item_list(
        SCREEN,
        best["items"],
        inner_right.x + 10,
        y,
        inner_right.width - 16,
        inner_right.bottom - y,
        SMALL_FONT,
        SUBTEXT,
        empty_text="No best items.",
    )

    draw_text(
        SCREEN,
        "This is the knapsack idea: find the highest-value set that fits.",
        SMALL_FONT,
        ACCENT,
        70,
        footer_y,
        max_width=1650,
    )

    play_again_button.draw(SCREEN)
    quit_button.draw(SCREEN)


def main():
    state = "title"

    start_button = Button((0, 0, 280, 72), "Start Heist")
    confirm_button = Button((0, 0, 220, 68), "Confirm")
    play_again_button = Button((0, 0, 220, 60), "Play Again")
    quit_button = Button((0, 0, 170, 60), "Quit", bg=(120, 70, 70), hover=(145, 85, 85))

    round_data = None
    result = None

    while True:
        # First layout pass so button rects exist before clicks
        if state == "title":
            current_layout = layout_title_ui(start_button)
        elif state == "play" and round_data is not None:
            current_layout = layout_play_ui(round_data, confirm_button)
        elif state == "result" and round_data is not None and result is not None:
            current_layout = layout_result_ui(play_again_button, quit_button)
        else:
            current_layout = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if state == "title":
                if start_button.clicked(event):
                    round_data = start_new_round()
                    result = None
                    state = "play"

            elif state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in round_data["cards"]:
                        if card.handle_click(event.pos):
                            break

                if confirm_button.clicked(event):
                    total_weight, total_value, selected_items = get_selected_totals(round_data["cards"])
                    result = make_result(
                        total_weight,
                        total_value,
                        selected_items,
                        round_data["capacity"],
                        round_data["best"],
                    )
                    state = "result"

            elif state == "result":
                if play_again_button.clicked(event):
                    round_data = start_new_round()
                    result = None
                    state = "play"
                elif quit_button.clicked(event):
                    pygame.quit()
                    sys.exit()

        # Recalculate layout AFTER possible state changes
        if state == "title":
            current_layout = layout_title_ui(start_button)
            draw_title_screen(start_button, current_layout)

        elif state == "play" and round_data is not None:
            current_layout = layout_play_ui(round_data, confirm_button)
            draw_game_screen(round_data, confirm_button, current_layout)

        elif state == "result" and round_data is not None and result is not None:
            current_layout = layout_result_ui(play_again_button, quit_button)
            draw_result_screen(result, round_data, play_again_button, quit_button, current_layout)

        pygame.display.flip()
        CLOCK.tick(60)


if __name__ == "__main__":
    main()
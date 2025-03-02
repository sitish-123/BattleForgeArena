import pygame
import pygame.gfxdraw
from typing import List, Tuple


class MenuButton:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color=(100, 100, 100),
                 hover_color=(130, 130, 130)):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_clicked = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.corner_radius = 15

    def draw_rounded_rect(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int],
                          corner_radius: int):
        if corner_radius < 0:
            corner_radius = 0
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def update(self):
        self.scale += (self.target_scale - self.scale) * 0.2
        width = self.original_rect.width * self.scale
        height = self.original_rect.height * self.scale
        x = self.original_rect.centerx - width / 2
        y = self.original_rect.centery - height / 2
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        self.update()
        self.draw_rounded_rect(surface, self.rect, self.current_color, int(self.corner_radius * self.scale))
        scaled_font = pygame.font.Font(None, int(36 * self.scale))
        text_surface = scaled_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
                self.target_scale = 1.1
            else:
                self.current_color = self.color
                self.target_scale = 1.0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                self.current_color = tuple(max(0, c - 30) for c in self.color)
                self.target_scale = 0.95
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
            if self.rect.collidepoint(event.pos):
                self.target_scale = 1.1
                return True
        return False


class ArenaCard:
    def __init__(self, x: float, y: float, screen_width: int, screen_height: int, image_path: str, name: str):
        self.card_height = int(screen_height * 0.6)
        self.card_width = int(self.card_height * 16 / 10)
        self.image_height = int(self.card_height * 0.82)
        self.image_width = int(self.card_width * 0.9)

        self.original_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        self.rect = self.original_rect.copy()
        self.name = name

        try:
            self.image = pygame.image.load(image_path)
        except pygame.error:
            self.image = pygame.Surface((self.image_width, self.image_height))
            self.image.fill((60, 60, 60))
            font = pygame.font.Font(None, 36)
            text = font.render("Image Not Found", True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.image_width / 2, self.image_height / 2))
            self.image.blit(text, text_rect)

        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))

        self.selected = False
        self.scale = 0.8
        self.target_scale = 1.0
        self.x_offset = 0
        self.hover_scale = 1.1
        self.normal_scale = 1.0
        self.animation_speed = 0.2
        self.corner_radius = 15

    def create_rounded_mask(self, width: int, height: int, radius: int) -> pygame.Surface:
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
        return mask

    def apply_rounded_corners(self, surface: pygame.Surface, radius: int) -> pygame.Surface:
        mask = self.create_rounded_mask(surface.get_width(), surface.get_height(), radius)
        result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        result.blit(surface, (0, 0))
        result.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return result

    def handle_hover(self, mouse_pos: Tuple[int, int]):
        if self.rect.collidepoint(mouse_pos):
            self.target_scale = self.hover_scale
        else:
            self.target_scale = self.normal_scale

    def update(self, scroll_offset: int):
        self.scale += (self.target_scale - self.scale) * self.animation_speed
        width = self.original_rect.width * self.scale
        height = self.original_rect.height * self.scale
        x = self.original_rect.centerx - width / 2 + scroll_offset
        y = self.original_rect.centery - height / 2
        self.rect = pygame.Rect(x, y, width, height)
        self.x_offset = scroll_offset

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(surface, (30, 30, 30), shadow_rect, border_radius=self.corner_radius)

        # Card background
        pygame.draw.rect(surface, (60, 60, 60), self.rect, border_radius=self.corner_radius)

        # Image
        scaled_width = int(self.image_width * self.scale)
        scaled_height = int(self.image_height * self.scale)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        rounded_image = self.apply_rounded_corners(scaled_image, int(self.corner_radius * self.scale))

        image_rect = rounded_image.get_rect(
            centerx=self.rect.centerx,
            centery=self.rect.centery - scaled_height * 0.05
        )
        surface.blit(rounded_image, image_rect)

        # Text
        shadow_text = font.render(self.name, True, (0, 0, 0))
        text_surface = font.render(self.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom - 20)

        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        surface.blit(shadow_text, shadow_rect)
        surface.blit(text_surface, text_rect)

        if self.selected:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, width=5, border_radius=self.corner_radius)


class MenuManager:
    run=False
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = "main_menu"
        self.selected_arena = None
        self.scroll_offset = 0
        self.target_scroll = 0
        self.scroll_speed = 0.2
        self.elastic_bound = 100
        self.dragging = False
        self.last_mouse_x = 0
        self.run=False

        # Initialize main menu buttons
        self.main_buttons = [
            MenuButton(300, 200, 200, 50, "Start Game", (52, 152, 219)),
            MenuButton(300, 300, 200, 50, "Options", (46, 204, 113)),
            MenuButton(300, 400, 200, 50, "Quit", (231, 76, 60)),
            MenuButton(300, 500, 200, 50, "Arena", (142, 68, 173))
        ]

        # Initialize arena cards
        self.arena_cards: List[ArenaCard] = []
        self.load_arena_cards()

        # Navigation buttons for arena selection
        self.back_button = MenuButton(20, 20, 100, 40, "Back", (231, 76, 60))
        self.select_button = MenuButton(screen_width - 120, 20, 100, 40, "Select", (46, 204, 113))

    def load_arena_cards(self):
        arena_data = [
            ("assets/Background/bg1/stack1.jpg", "Forest Arena"),
            ("assets/Background/bg2/stack2.jpg", "Desert Arena"),
            ("assets/Background/bg3/stack3.jpg", "Ice Arena")
        ]

        card_spacing = int(self.screen_width * 0.1)
        for i, (image_path, name) in enumerate(arena_data):
            x = i * (self.screen_width * 0.8 + card_spacing)
            y = self.screen_height // 2 - int(self.screen_height * 0.3)
            self.arena_cards.append(ArenaCard(x, y, self.screen_width, self.screen_height, image_path, name))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.state == "main_menu":
            for button in self.main_buttons:
                if button.handle_event(event):
                    if button.text=="Start Game":
                        self.run=True
                    if button.text == "Quit":
                        return False
                    elif button.text == "Arena":
                        self.state = "arena_selection"
                        # Reset scroll position when entering arena selection
                        self.scroll_offset = 0
                        self.target_scroll = 0
                        self.dragging = False

        elif self.state == "arena_selection":
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            # Handle navigation buttons with proper effects
            self.back_button.handle_event(event)
            self.select_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.rect.collidepoint(mouse_pos):
                    self.state = "main_menu"
                    return True
                elif self.select_button.rect.collidepoint(mouse_pos):
                    for card in self.arena_cards:
                        if card.selected:
                            self.selected_arena = card.name
                            self.state = "main_menu"
                            return True

            # Handle card selection and dragging
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                self.dragging = True
                self.last_mouse_x = event.pos[0]

                # Check for card selection
                for card in self.arena_cards:
                    if card.rect.collidepoint(mouse_pos):
                        for c in self.arena_cards:
                            c.selected = False
                        card.selected = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                # Only scroll if dragging (left mouse button is held down)
                if self.dragging and mouse_buttons[0]:  # Check if left mouse button is still pressed
                    dx = event.pos[0] - self.last_mouse_x
                    self.target_scroll += dx
                    self.last_mouse_x = event.pos[0]
                else:
                    # If mouse button was released without us catching it, stop dragging
                    self.dragging = False

            elif event.type == pygame.MOUSEWHEEL:
                self.target_scroll += event.y * 50

            # Update hover states
            for card in self.arena_cards:
                card.handle_hover(mouse_pos)

        return True

    def update(self):
        if self.state == "main_menu":
            for button in self.main_buttons:
                button.update()

        elif self.state == "arena_selection":
            # Update navigation buttons
            self.back_button.update()
            self.select_button.update()

            # Update scroll position
            card_width_with_spacing = self.screen_width * 0.9
            max_scroll = self.elastic_bound
            min_scroll = -((len(self.arena_cards) - 1) * card_width_with_spacing) - self.elastic_bound

            if self.target_scroll > max_scroll:
                self.target_scroll += (max_scroll - self.target_scroll) * 0.2
            elif self.target_scroll < min_scroll:
                self.target_scroll += (min_scroll - self.target_scroll) * 0.2

            self.scroll_offset += (self.target_scroll - self.scroll_offset) * self.scroll_speed

            # Update cards
            for card in self.arena_cards:
                card.update(self.scroll_offset)


    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        if self.state == "main_menu":
            for button in self.main_buttons:
                button.draw(surface, font)

        elif self.state == "arena_selection":
            # Draw arena cards
            for card in reversed(self.arena_cards):
                card.draw(surface, font)

            # Draw navigation buttons
            self.back_button.draw(surface, font)
            self.select_button.draw(surface, font)


def main():
    pygame.init()
    pygame.display.set_caption("Game Menu")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    menu_manager = MenuManager(800, 600)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = menu_manager.handle_event(event)

        menu_manager.update()

        screen.fill((40, 40, 40))
        menu_manager.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
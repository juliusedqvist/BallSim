import pygame
import random
import math

pygame.init()

win_width = 1000
win_height = 1000
border_start = 100
border_bottom = 900
radius = 10
density = 1

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Ball simulation')


class Char:

    def __init__(self, x, y, radius, x_vel, y_vel):  # Official character variables
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw_char(self, color):  # Get the character on board
        pygame.draw.circle(win, (color[0], color[1], color[2]), (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def check_collision(self):
        if self.x > border_bottom - self.radius:
            self.x = border_bottom - self.radius
            self.x_vel = -self.x_vel
        if self.x < border_start + self.radius:
            self.x = border_start + self.radius
            self.x_vel = -self.x_vel
        if self.y > border_bottom - self.radius:
            self.y = border_bottom - self.radius
            self.y_vel = -self.y_vel
        if self.y < border_start + self.radius:
            self.y = border_start + self.radius
            self.y_vel = -self.y_vel


class Ball(Char):

    def collision_balls(self, other_balls):
        for other in other_balls:
            if self != other:  # Avoid self-collision
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < (self.radius + other.radius):
                    self.collide(other, other_balls)
                    return True
        return False  # No collision

    def collide(self, other, other_balls):

        self.x_vel = (self.x_vel * (self.radius ** 2 * math.pi) / density + other.x_vel * (
                other.radius ** 2 * math.pi) / density) / (self.radius ** 2 * math.pi + other.radius ** 2 * math.pi)
        self.y_vel = (self.y_vel * (self.radius ** 2 * math.pi) / density + other.x_vel * (
                other.radius ** 2 * math.pi) / density) / (self.radius ** 2 * math.pi + other.radius ** 2 * math.pi)
        self.radius = math.sqrt(((self.radius ** 2 * math.pi) + (other.radius ** 2 * math.pi)) / math.pi)
        self.x = (self.x + other.x) / 2
        self.y = (self.y + other.y) / 2
        other_balls.remove(other)


def draw_board():
    pygame.draw.line(win, (0, 0, 150), (border_start, border_start), (border_start, border_bottom))
    pygame.draw.line(win, (0, 0, 150), (border_start, border_start), (border_bottom, border_start))
    pygame.draw.line(win, (0, 0, 150), (border_start, border_bottom), (border_bottom, border_bottom))
    pygame.draw.line(win, (0, 0, 150), (border_bottom, border_bottom), (border_bottom, border_start))


class Button:
    def __init__(self, x, y, width, height, text, color, highlight_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.action = action
        self.highlighted = False

    def draw(self):
        pygame.draw.rect(win, self.highlight_color if self.highlighted else self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(text, text_rect)


class Input:
    def __init__(self, x, y, width, height, input_text, color, highlight_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.input_text = input_text
        self.color = color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.active = False

    def draw(self):
        pygame.draw.rect(win, self.highlight_color if self.active or self.highlighted else self.color, self.rect)
        pygame.Rect(705, 50, 100, 50)
        # self.width = max(100, text_surface.get_width() + 10)
        text = font.render(self.input_text, True, (255, 255, 255))
        input_text_rect = text.get_rect(center=self.rect.center)
        win.blit(text, input_text_rect)

    def fill_text(self):
        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        # Fill box
        else:
            self.input_text += event.unicode


# Global variables

paused = True
toggle_velocity_text = False
balls = [Ball(random.randint(border_start + radius, border_bottom - radius),
              random.randint(border_start + radius, border_bottom - radius), radius, (random.random() - 0.5) * 5,
              (random.random() - 0.5) * 5) for i in range(50)]
font = pygame.font.Font(None, 36)
spd = 60

if __name__ == '__main__':

    game = True
    clock = pygame.time.Clock()

    # Define buttons and fields

    start_button = Button(100, 50, 195, 50, "Start", (0, 255, 0), (0, 200, 0), lambda: toggle_simulation(paused))
    show_attributes = Button(300, 50, 195, 50, "Show attributes", (0, 255, 0), (0, 200, 0),
                             lambda: toggle_text(toggle_velocity_text))
    reset = Button(500, 50, 200, 50, "reset", (0, 255, 0), (0, 200, 0), lambda: reset_game(balls, spd))
    stop_button = Button(win_width - 55, 5, 50, 50, "X", (0, 255, 0), (0, 200, 0), lambda: stop_game(game))
    count_field = Input(705, 50, 95, 50, "50", (0, 255, 0), (0, 200, 0))
    speed_field = Input(805, 50, 100, 50, "60", (0, 255, 0), (0, 200, 0))


    def toggle_text(t):
        return not t


    def stop_game(g):
        return not g


    def reset_game(b, s):
        for i in range(len(b)):
            b.pop(0)
        try:
            num = int(count_field.input_text)
        except ValueError:
            num = 50
        for key in range(int(num)):
            b.append(Ball(random.randint(border_start + radius, border_bottom - radius),
                          random.randint(border_start + radius, border_bottom - radius), radius,
                          (random.random() - 0.5) * 5,
                          (random.random() - 0.5) * 5))
        try:
            s = int(speed_field.input_text)
            return s
        except ValueError:
            return s


    def toggle_simulation(p):
        return not p


    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            # Check for meny clicks

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    paused = start_button.action()
                if show_attributes.rect.collidepoint(event.pos):
                    toggle_velocity_text = show_attributes.action()
                if stop_button.rect.collidepoint(event.pos):
                    game = stop_button.action()
                if reset.rect.collidepoint(event.pos):
                    spd = reset.action()

                # Check and empty text fields on click

                if count_field.rect.collidepoint(event.pos):
                    count_field.active = True
                    count_field.input_text = ""
                else:
                    count_field.active = False
                if speed_field.rect.collidepoint(event.pos):
                    speed_field.active = True
                    speed_field.input_text = ""
                else:
                    speed_field.active = False

            # Fill selected text field on keydown

            if event.type == pygame.KEYDOWN and count_field.active:
                count_field.fill_text()
            if event.type == pygame.KEYDOWN and speed_field.active:
                speed_field.fill_text()

        # highlight meny options

        start_button.highlighted = start_button.rect.collidepoint(pygame.mouse.get_pos())
        show_attributes.highlighted = show_attributes.rect.collidepoint(pygame.mouse.get_pos())
        reset.highlighted = reset.rect.collidepoint(pygame.mouse.get_pos())
        stop_button.highlighted = stop_button.rect.collidepoint(pygame.mouse.get_pos())
        count_field.highlighted = count_field.rect.collidepoint(pygame.mouse.get_pos())
        speed_field.highlighted = speed_field.rect.collidepoint(pygame.mouse.get_pos())

        win.fill((0, 0, 0))

        # Draw buttons

        draw_board()
        start_button.draw()
        show_attributes.draw()
        reset.draw()
        stop_button.draw()

        # input box

        count_field.draw()
        speed_field.draw()

        # Render text above input fields

        text1 = font.render("count:", False, "white")
        text1Rect = text1.get_rect()
        text1Rect.center = (750, 30)
        win.blit(text1, text1Rect)

        text2 = font.render("speed:", False, "white")
        text2Rect = text2.get_rect()
        text2Rect.center = (850, 30)
        win.blit(text2, text2Rect)

        # Draw character stuff here

        for i in balls:
            i.draw_char((200, 200, 0))
            if not paused:
                i.move()
                i.check_collision()
                i.collision_balls(balls)

            # Display velocity over each ball
            if toggle_velocity_text:
                velocity_text = font.render(
                    f'Velocity: ({math.sqrt(i.x_vel ** 2 + i.y_vel ** 2):.2f}, Mass: {i.radius ** 2 * math.pi / density:.0f})',
                    True, (255, 255, 255))
                text_rect = velocity_text.get_rect(center=(i.x, i.y - i.radius - 10))
                win.blit(velocity_text, text_rect)

        font = pygame.font.Font(None, 36)

        pygame.display.update()
        clock.tick(spd)

    pygame.quit()

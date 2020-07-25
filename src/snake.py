import pygame
import random

from os import path


def hitscreenedge(x, y, width, height):
    if x < 0:
        return True
    if y < 0:
        return True
    if (x + width) > 500:
        return True
    if (y + height) > 500:
        return True

    return False


LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

COUNTDOWN = 1
PLAYING = 2
DEAD = 3

font = None


class Snake:
    def __init__(self, head_diameter, tailpiece_diameter):

        self.head_diameter = head_diameter
        self.head_radius = head_diameter / 2
        self.tailpiece_diameter = tailpiece_diameter
        self.tailpiece_radius = tailpiece_diameter / 2
        self.display_boxes = False
        self.x = 0
        self.y = 0
        self.length = 0
        self.sections = []
        self.section_boxes = []
        self.speed = 0
        self.direction = None

    def reset(self, xstart, ystart, direction):
        self.x = xstart
        self.y = ystart
        self.length = (self.tailpiece_diameter * 2) + 1
        self.sections = []
        self.new_section(direction)
        self.speed = 2
        self.direction = direction

    def draw_head(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), int(self.head_radius))

        eye_radius = self.head_radius / 4
        pupil_radius = eye_radius / 3
        if self.direction == RIGHT:
            offset = self.head_radius / 2
            pygame.draw.circle(
                win,
                (250, 250, 250),
                (int(self.x + offset), self.y - int(self.head_radius / 3)),
                int(eye_radius),
            )
            pygame.draw.circle(
                win,
                (20, 20, 0),
                (
                    int(self.x + offset + int(eye_radius * 0.7)),
                    self.y - int(self.head_radius / 3),
                ),
                int(pupil_radius),
            )
        elif self.direction == LEFT:
            offset = -self.head_radius / 2
            pygame.draw.circle(
                win,
                (250, 250, 250),
                (int(self.x + offset), self.y - int(self.head_radius / 3)),
                int(eye_radius),
            )
            pygame.draw.circle(
                win,
                (20, 20, 0),
                (
                    int(self.x + offset - int(eye_radius * 0.7)),
                    self.y - int(self.head_radius / 3),
                ),
                int(pupil_radius),
            )
        if self.direction == UP:
            for offset in [-self.head_radius / 2, self.head_radius / 2]:
                pygame.draw.circle(
                    win,
                    (250, 250, 250),
                    (int(self.x + offset), self.y - int(self.head_radius / 3)),
                    int(eye_radius),
                )
                pygame.draw.circle(
                    win,
                    (20, 20, 0),
                    (
                        int(self.x + offset),
                        self.y - int(self.head_radius / 3) - int(eye_radius * 0.7),
                    ),
                    int(pupil_radius),
                )
        elif self.direction == DOWN:
            pygame.draw.circle(
                win, (255, 0, 0), (self.x, self.y), int(self.head_radius)
            )

            for offset in [-self.head_radius / 2, self.head_radius / 2]:
                pygame.draw.circle(
                    win,
                    (250, 250, 250),
                    (int(self.x + offset), self.y + int(self.head_radius / 3)),
                    int(eye_radius),
                )
                pygame.draw.circle(
                    win,
                    (20, 20, 0),
                    (
                        int(self.x + offset),
                        self.y + int(self.head_radius / 3) + int(eye_radius * 0.7),
                    ),
                    int(pupil_radius),
                )

    def update(self, win, font):

        died = False
        self.draw_head(win)

        if self.sections:
            direction = self.sections[0]["direction"]

            self.x += (
                self.speed
                if direction == RIGHT
                else -self.speed
                if direction == LEFT
                else 0
            )
            self.y += (
                self.speed
                if direction == DOWN
                else -self.speed
                if direction == UP
                else 0
            )

            currentx = self.x
            currenty = self.y
            total_length = 0
            self.sections[0]["length"] += self.speed

            current_piece_counter = int(self.head_radius)

            sections_to_remove = []

            section_circles = []
            self.section_boxes = []
            for section in self.sections:
                box_xmin = 1000
                box_xmax = 0
                box_ymin = 1000
                box_ymax = 0

                total_length += section["length"]
                if total_length > self.length:
                    section["length"] -= total_length - self.length

                if section["length"] <= 0:
                    sections_to_remove.append(section)
                else:
                    length = section["length"]
                    stepx = 0
                    stepy = 0
                    if section["direction"] == LEFT:
                        stepx = self.tailpiece_diameter
                        xsection = currentx + current_piece_counter
                        ysection = currenty
                        currentx += length
                    elif section["direction"] == RIGHT:
                        stepx = -self.tailpiece_diameter
                        xsection = currentx - current_piece_counter
                        ysection = currenty
                        currentx -= length
                    elif section["direction"] == UP:
                        stepy = self.tailpiece_diameter
                        xsection = currentx
                        ysection = currenty + current_piece_counter
                        currenty += length
                    elif section["direction"] == DOWN:
                        stepy = -self.tailpiece_diameter
                        xsection = currentx
                        ysection = currenty - current_piece_counter
                        currenty -= length

                    while current_piece_counter < length:
                        pygame.draw.circle(
                            win,
                            (255, 0, 0),
                            (int(xsection), int(ysection)),
                            int(self.tailpiece_radius),
                            1,
                        )
                        section_circles.append((xsection, ysection))

                        if box_xmin > int(xsection - self.tailpiece_radius):
                            box_xmin = int(xsection - self.tailpiece_radius)
                        if box_xmax < int(xsection + self.tailpiece_radius):
                            box_xmax = int(xsection + self.tailpiece_radius)
                        if box_ymin > int(ysection - self.tailpiece_radius):
                            box_ymin = int(ysection - self.tailpiece_radius)
                        if box_ymax < int(ysection + self.tailpiece_radius):
                            box_ymax = int(ysection + self.tailpiece_radius)
                        xsection += stepx
                        ysection += stepy
                        current_piece_counter += self.tailpiece_diameter

                    if box_xmax > 0:
                        self.section_boxes.append(
                            (
                                box_xmin,
                                box_ymin,
                                box_xmax - box_xmin,
                                box_ymax - box_ymin,
                            )
                        )
                    current_piece_counter -= length

            for section in sections_to_remove:
                self.sections.remove(section)

            if self.check_head_collision(section_circles[2:]):
                died = True

            if self.display_boxes:
                for box in self.section_boxes:
                    pygame.draw.rect(win, (0, 255, 0), box, 1)

        text_image = font.render("Score: 0000", True, (50, 200, 50))
        win.blit(
            text_image,
            (400 - text_image.get_width() // 2, 30 - text_image.get_height() // 2),
        )
        return died

    def check_head_collision(self, section_circles):
        min_distance = self.head_radius + self.tailpiece_radius
        for circle in section_circles:
            if (
                abs(self.x - circle[0]) < min_distance
                and abs(self.y - circle[1]) < min_distance
            ):
                return True

        return False

    def collides_with(self, x, y, size):
        # Check head first
        min_distance = self.head_radius + size
        if abs(self.x - x) < min_distance:
            return True
        if abs(self.y - y) < min_distance:
            return True

        # Now check sections
        for box in self.section_boxes:
            if (x + size) < box[0]:
                continue
            if (x - size) > (box[0] + box[2]):
                continue
            if (y + size) < box[1]:
                continue
            if (y - size) > (box[1] + box[3]):
                continue
            return True
        return False

    def new_section(self, direction):
        if self.length:
            self.sections.insert(0, {"length": 0, "direction": direction})

    def possible_to_move(self, desired_direction):
        if self.sections and self.sections[0]["length"] < (
            self.head_radius + self.tailpiece_radius
        ):
            return False

        if desired_direction == LEFT or desired_direction == RIGHT:
            if self.direction != LEFT and self.direction != RIGHT:
                return True
        elif desired_direction == UP or desired_direction == DOWN:
            if self.direction != UP and self.direction != DOWN:
                return True
        return False


FOOD_SIZE = 10


class Food:
    def __init__(self, play_area_size):
        self.play_area_size = play_area_size
        self.active = False
        self.countdown = 5 * 60
        self.position = None

    def update(self, win, snake):
        if self.active:
            pygame.draw.circle(win, (0, 0, 200), self.position, FOOD_SIZE)
        else:
            self.countdown -= 1
            if self.countdown == 0:
                new_x = random.randrange(
                    FOOD_SIZE, self.play_area_size[0] - FOOD_SIZE - 1
                )
                new_y = random.randrange(
                    FOOD_SIZE, self.play_area_size[1] - FOOD_SIZE - 1
                )

                if not snake.collides_with(new_x, new_y, FOOD_SIZE):
                    self.active = True
                    self.position = (new_x, new_y)
                else:
                    # Try again next frame
                    self.countdown = 1


def main_loop(win):
    head_diameter = 64
    tailpiece_diameter = 32

    font = pygame.font.Font(path.join("content", "PixelSplitter-Bold.ttf"), 26)

    run = True
    snake = Snake(head_diameter, tailpiece_diameter)
    food = Food((800, 600))

    directions = {
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
    }

    state = COUNTDOWN
    countdown_to_next_state = (4 * 60) - 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if state == COUNTDOWN:
            seconds = int(countdown_to_next_state / 60)
            if seconds != 0:
                text = str(seconds)
            else:
                text = "GO!"

            text_image = font.render(text, True, (200, 200, 150))
            background = (0, 0, 0)
            # if hitscreenedge(x, y, width, height):
            #    background=(234, 234, 122)
            win.fill(background)
            win.blit(
                text_image,
                (
                    250 - text_image.get_width() // 2,
                    250 - text_image.get_height() // 2,
                ),
            )

            countdown_to_next_state -= 1
            if countdown_to_next_state == 0:
                snake.reset(250, 250, RIGHT)
                state = PLAYING

        elif state == PLAYING:
            for key in directions:
                if keys[key] and snake.possible_to_move(directions[key]):
                    snake.direction = directions[key]
                    snake.new_section(snake.direction)
                    break

            if keys[pygame.K_b]:
                snake.display_boxes = False if snake.display_boxes else True

            background = (0, 0, 0)
            # if hitscreenedge(x, y, width, height):
            #    background=(234, 234, 122)
            win.fill(background)

            if snake.update(win, font):
                state = DEAD
                countdown_to_next_state = (5 * 60) - 1

            food.update(win, snake)

        elif state == DEAD:
            text_image = font.render("DEAD", True, (250, 200, 50))
            background = (0, 0, 0)
            # if hitscreenedge(x, y, width, height):
            #    background=(234, 234, 122)
            win.fill(background)
            win.blit(
                text_image,
                (
                    100 - text_image.get_width() // 2,
                    400 - text_image.get_height() // 2,
                ),
            )

            countdown_to_next_state -= 1
            if countdown_to_next_state == 0:
                countdown_to_next_state = (4 * 60) - 1
                state = COUNTDOWN

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

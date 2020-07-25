import pygame
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

font = None


class Snake:
    def __init__(self, xstart, ystart, head_diameter, tailpiece_diameter):

        self.x = xstart
        self.y = ystart
        self.length = 0
        self.sections = []
        self.head_diameter = head_diameter
        self.head_radius = head_diameter / 2
        self.tailpiece_diameter = tailpiece_diameter
        self.tailpiece_radius = tailpiece_diameter / 2
        self.display_boxes = True

    def draw_head(self, win, direction):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), int(self.head_radius))

        eye_radius = self.head_radius / 4
        pupil_radius = eye_radius / 3
        if direction == RIGHT:
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
        elif direction == LEFT:
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
        if direction == UP:
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
        elif direction == DOWN:
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

    def update(self, win, font, speed, direction):

        self.draw_head(win, direction)

        if self.sections:
            direction = self.sections[0]["direction"]

            self.x += (
                speed if direction == RIGHT else -speed if direction == LEFT else 0
            )
            self.y += speed if direction == DOWN else -speed if direction == UP else 0

            currentx = self.x
            currenty = self.y
            total_length = 0
            self.sections[0]["length"] += speed

            current_piece_counter = int(self.head_radius)

            sections_to_remove = []

            section_circles = []
            section_boxes = []
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
                        section_boxes.append(
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
                text_image = font.render("DEAD", True, (250, 200, 50))
                win.blit(
                    text_image,
                    (
                        100 - text_image.get_width() // 2,
                        400 - text_image.get_height() // 2,
                    ),
                )

            if self.display_boxes:
                for box in section_boxes:
                    pygame.draw.rect(win, (0, 255, 0), box, 1)

        text_image = font.render("Score: 0000", True, (50, 200, 50))
        win.blit(
            text_image,
            (400 - text_image.get_width() // 2, 30 - text_image.get_height() // 2),
        )

    def check_head_collision(self, section_circles):
        min_distance = self.head_radius + self.tailpiece_radius
        for circle in section_circles:
            if (
                abs(self.x - circle[0]) < min_distance
                and abs(self.y - circle[1]) < min_distance
            ):
                return True

        return False

    def new_section(self, direction):
        if self.length:
            self.sections.insert(0, {"length": 0, "direction": direction})

    def possible_to_move(self, current_direction, desired_direction):
        if self.sections and self.sections[0]["length"] < (
            self.head_radius + self.tailpiece_radius
        ):
            return False

        if desired_direction == LEFT or desired_direction == RIGHT:
            if current_direction != LEFT and current_direction != RIGHT:
                return True
        elif desired_direction == UP or desired_direction == DOWN:
            if current_direction != UP and current_direction != DOWN:
                return True
        return False


def main_loop(win):
    width = 8
    height = 8
    speed = 0
    head_diameter = 64
    tailpiece_diameter = 32

    font = pygame.font.Font(path.join("content", "PixelSplitter-Bold.ttf"), 26)

    # image = pygame.image.load('./content/snakehead.jpg')
    # head = pygame.transform.scale(image, (width, height))

    run = True
    direction = None
    snake = Snake(250, 250, head_diameter, tailpiece_diameter)

    directions = {
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
    }
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        for key in directions:
            if keys[key] and snake.possible_to_move(direction, directions[key]):
                direction = directions[key]
                snake.new_section(direction)
                break

        if keys[pygame.K_b]:
            snake.display_boxes = False if snake.display_boxes else True

        if keys[pygame.K_SPACE]:
            snake.length += snake.tailpiece_diameter

            if not snake.sections:
                snake.new_section(direction)

        if not speed and direction:
            speed = 2

        background = (0, 0, 0)
        # if hitscreenedge(x, y, width, height):
        #    background=(234, 234, 122)
        win.fill(background)

        snake.update(win, font, speed, direction)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

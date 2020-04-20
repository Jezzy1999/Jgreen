import pygame

def hitscreenedge(x, y, width, height):
    if x < 0:
        return True
    if y < 0:
        return True
    if (x + width) > 500:
        return True
    if (y + height) > 500:
        return True

    return  False

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

class Snake():

    def __init__(self, head_diameter, tailpiece_diameter):

        self.length = 0
        self.sections = []
        self.head_diameter = head_diameter
        self.head_radius = head_diameter / 2
        self.tailpiece_diameter = tailpiece_diameter
        self.tailpiece_radius = tailpiece_diameter / 2

    def update(self, win, x, y, speed):
        pygame.draw.circle(win, (255,0,0), (x, y), int(self.head_radius), 1)

        if self.sections:

            currentx = x
            currenty = y
            initial_radius = int(self.head_radius)
            total_length = 0
            self.sections[0]["length"] += speed

            piece_counter = 0
            sections_to_remove = []
            for section in self.sections:
                total_length += section["length"]
                if total_length > self.length:
                    section["length"] -= (total_length - self.length)
    
                if section["length"] <= 0:
                    sections_to_remove.append(section)
                else:
                    length = section["length"]
                    stepx = 0
                    stepy = 0
                    if section["direction"] == LEFT:
                        stepx = self.tailpiece_diameter
                        xsection = currentx + initial_radius
                        ysection = currenty
                        currentx += length
                    elif section["direction"] == RIGHT:
                        stepx = -self.tailpiece_diameter
                        xsection = currentx - initial_radius
                        ysection = currenty
                        currentx -= length
                    elif section["direction"] == UP:
                        stepy = self.tailpiece_diameter
                        xsection = currentx
                        ysection = currenty + initial_radius
                        currenty += length
                    elif section["direction"] == DOWN:
                        stepy = -self.tailpiece_diameter
                        xsection = currentx 
                        ysection = currenty - initial_radius
                        currenty -= length

                    while (piece_counter + self.tailpiece_diameter) < length:
                        pygame.draw.circle(
                            win,
                            (255, 0, 0),
                            (int(xsection + (stepx / 2)), int(ysection + (stepy / 2))), 
                            int(self.tailpiece_radius),
                            1
                        )
                        xsection += stepx
                        ysection += stepy
                        piece_counter += self.tailpiece_diameter

                    piece_counter -= length
                    initial_radius = 0

            for section in sections_to_remove:
                self.sections.remove(section)

    def new_section(self, x, y, direction):
        if self.length:
            self.sections.insert(0, {
                "length":0,
                "direction":direction
            })

def main_loop(win):
    x = 250
    y = 250
    width = 8
    height = 8
    speed = 0
    head_diameter = 16
    tailpiece_diameter = 8

    image = pygame.image.load('./content/snakehead.jpg')
    head = pygame.transform.scale(image, (width, height))

    run = True
    direction = None
    snake = Snake(head_diameter, tailpiece_diameter)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if direction != LEFT and direction != RIGHT:
                direction = LEFT
                snake.new_section(x, y, direction)

        if keys[pygame.K_RIGHT]:
            if direction != LEFT and direction != RIGHT:
                direction = RIGHT
                snake.new_section(x, y, direction)

        if keys[pygame.K_UP]:
            if direction != UP and direction != DOWN:
                direction = UP
                snake.new_section(x, y, direction)

        if keys[pygame.K_DOWN]:
            if direction != UP and direction != DOWN:
                direction = DOWN
                snake.new_section(x, y, direction)

        if keys[pygame.K_SPACE]:
            snake.length += speed

            if not snake.sections:
                snake.new_section(x, y, direction)

        if not speed and direction:
            speed = 2

        x += speed if direction == RIGHT else -speed if direction == LEFT else 0
        y += speed if direction == DOWN else -speed if direction == UP else 0

        background=(0, 0, 0)
        if hitscreenedge(x, y, width, height):
            background=(234, 234, 122)
        win.fill(background)

        snake.update(win, x, y, speed)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

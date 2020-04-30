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

    def update(self, win, speed):

        pygame.draw.circle(win, (255,0,0), (self.x, self.y), int(self.head_radius), 1)

        if self.sections:
            direction = self.sections[0]["direction"]

            self.x += speed if direction == RIGHT else -speed if direction == LEFT else 0
            self.y += speed if direction == DOWN else -speed if direction == UP else 0

            currentx = self.x
            currenty = self.y
            total_length = 0
            self.sections[0]["length"] += speed

            current_piece_counter = int(self.head_radius)

            sections_to_remove = []
            section_boxes = []
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
                        xsection = currentx + current_piece_counter
                        ysection = currenty
                        currentx += length
                        section_boxes.append(
                            (xsection, 
                             ysection - self.tailpiece_radius, 
                             length, 
                             self.tailpiece_diameter
                        ))
                    elif section["direction"] == RIGHT:
                        stepx = -self.tailpiece_diameter
                        xsection = currentx - current_piece_counter
                        ysection = currenty
                        currentx -= length
                        section_boxes.append((
                            xsection - length,
                            ysection - self.tailpiece_radius, 
                            length,
                            self.tailpiece_diameter
                        ))
                    elif section["direction"] == UP:
                        stepy = self.tailpiece_diameter
                        xsection = currentx
                        ysection = currenty + current_piece_counter
                        currenty += length
                        section_boxes.append((
                            xsection - self.tailpiece_radius,
                            ysection,
                            self.tailpiece_diameter,
                            length
                        ))
                    elif section["direction"] == DOWN:
                        stepy = -self.tailpiece_diameter
                        xsection = currentx 
                        ysection = currenty - current_piece_counter
                        currenty -= length
                        section_boxes.append((
                            xsection - self.tailpiece_radius,
                            ysection - length,
                            self.tailpiece_diameter,
                            length
                        ))

                    while (current_piece_counter < length):
                        pygame.draw.circle(
                            win,
                            (255, 0, 0),
                            (int(xsection), int(ysection)), 
                            int(self.tailpiece_radius),
                            1
                        )
                        xsection += stepx
                        ysection += stepy
                        current_piece_counter += self.tailpiece_diameter

                    current_piece_counter -= length

            for section in sections_to_remove:
                self.sections.remove(section)

            if self.display_boxes:
                for box in section_boxes:
                    pygame.draw.rect(win, 
                        (0,255,0),
                        box,
                        1
                    )

    def new_section(self, direction):
        if self.length:
            self.sections.insert(0, {
                "length":0,
                "direction":direction
            })

def main_loop(win):
    width = 8
    height = 8
    speed = 0
    head_diameter = 64
    tailpiece_diameter = 32

    image = pygame.image.load('./content/snakehead.jpg')
    head = pygame.transform.scale(image, (width, height))

    run = True
    direction = None
    snake = Snake(250, 250, head_diameter, tailpiece_diameter)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if direction != LEFT and direction != RIGHT:
                direction = LEFT
                snake.new_section(direction)

        if keys[pygame.K_RIGHT]:
            if direction != LEFT and direction != RIGHT:
                direction = RIGHT
                snake.new_section(direction)

        if keys[pygame.K_UP]:
            if direction != UP and direction != DOWN:
                direction = UP
                snake.new_section(direction)

        if keys[pygame.K_DOWN]:
            if direction != UP and direction != DOWN:
                direction = DOWN
                snake.new_section(direction)

        if keys[pygame.K_b]:
            snake.display_boxes = False if snake.display_boxes else True

        if keys[pygame.K_SPACE]:
            snake.length += snake.tailpiece_diameter

            if not snake.sections:
                snake.new_section(direction)

        if not speed and direction:
            speed = 4

        background=(0, 0, 0)
        #if hitscreenedge(x, y, width, height):
        #    background=(234, 234, 122)
        win.fill(background)

        snake.update(win, speed)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

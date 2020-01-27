import pygame

def hitscreenedge():
    if x < 0:
        return True
    if y < 0:
        return True
    if (x + width) > 500:
        return True
    if (y + height) > 500:
        return True

    return  False

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")

x = 250
y = 250
width = 40
height = 60
velx = 0
vely = 0

image = pygame.image.load(r'C:\Users\j0s3p\PycharmProjects\Jgreen\snake head.jpg')
head = pygame.transform.scale(image, (width, height))

run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if not velx == 5:
            velx = -5
            vely = 0

    if keys[pygame.K_RIGHT]:
        if not velx == -5:
            velx = 5
            vely = 0

    if keys[pygame.K_UP]:
        if not vely == 5:
            vely = -5
            velx = 0

    if keys[pygame.K_DOWN]:
        if not vely == -5:
            vely = 5
            velx = 0

    x += velx
    y += vely

    background=(0, 0, 0)
    if hitscreenedge():
        background=(234, 234, 122)
    win.fill(background)

    xbody = x
    ybody = y

    if velx == -5:
        xbody= x + width
        ybody= y

    if velx == 5:
        xbody = x-width
        ybody = y

    if vely == 5:
        xbody = x
        ybody = y - height
    if vely == -5:
        xbody = x
        ybody = y + height

    pygame.draw.rect(win, (255, 0, 0), (xbody, ybody, width, height))

    win.blit(head, (x, y))
    pygame.display.update()

pygame.quit()

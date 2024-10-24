import pygame , sys , os , math

# pygame setup
pygame.init()
WIDTH,HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

track_img = pygame.image.load(os.path.join("assets","track_assets","track.png"))

#this function will return the positions of the tiles and the background image
def background(background_name):
    path = os.path.join("assets","Background_Tiles",background_name)
    background_img =  pygame.image.load(path).convert_alpha()
    _,_,width,height = background_img .get_rect()
    positions = []
    for i in range(WIDTH//width+1):
        for j in range(HEIGHT//height+1):
            positions.append((i*width,j*height))
    return positions , background_img

def draw_background():
    #you can change the background by choosing one of these names :
    #"Grass_Tile.png" or "Soil_Tile.png"
    positions , background_img = background("Grass_Tile.png")
    for pos in positions:
        screen.blit(background_img,pos)

class Car():
    #you can change the background by choosing one of these names :
    #"WhiteStrip.png" , "GreenStrip.png" , "BlueStrip.png" , "PinkStrip.png"
    path = os.path.join("assets","car_assets","BlueStrip.png")
    car_img = pygame.image.load(path).convert_alpha()
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = self.car_img.get_rect(center=(self.x, self.y))
        self.car_speed = 0
        self.accelaration = 0.1
        self.max_speed = 7
        self.angle = 0
        self.rotation_speed = 3

    def move(self):
        press = pygame.key.get_pressed()

        # Rotate left (Q) or right (D)
        if press[pygame.K_q]:
            self.angle += self.rotation_speed
        if press[pygame.K_d]:
            self.angle -= self.rotation_speed

        # Move forward (Z) based on current angle
        if press[pygame.K_z]:
            if self.car_speed < self.max_speed:
                self.car_speed += self.accelaration
            else:
                self.car_speed = self.max_speed
        else:
            if self.car_speed > 0:
                self.car_speed -= self.accelaration

        # Convert angle to radians and calculate the x, y movement
        radians = math.radians(self.angle)
        self.rect.x += self.car_speed * math.cos(radians)
        self.rect.y -= self.car_speed * math.sin(radians)
             
    def update_car(self):
        self.move()
        self.draw()
        
    def draw(self):
        rotated_img = pygame.transform.rotate(self.car_img,self.angle)
        rotated_rect = rotated_img.get_rect(center=(self.rect.center))
        screen.blit(rotated_img,rotated_rect)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

car = Car(200,100)

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_background()
        screen.blit(track_img,(0,0))
        car.update_car()
        pygame.display.flip()

        clock.tick(60) # limits FPS to 60

if __name__ == "__main__":
    main()
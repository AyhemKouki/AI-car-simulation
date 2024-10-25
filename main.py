import pygame , sys , os , math

# pygame setup
pygame.init()
WIDTH,HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

track_img = pygame.image.load(os.path.join("assets","track_assets","track.png"))

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
        self.alive = True

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

    def radar(self):
        
        radar_angles_list = [-60,-30,0,30,60]
        
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        for radar_angle in radar_angles_list:
            radar_length = 0
            angle_radians = math.radians(self.angle + radar_angle)
            while radar_length < 200:
                # Calculate new position for radar point
                x = int(self.rect.centerx + radar_length * math.cos(angle_radians))
                y = int(self.rect.centery - radar_length * math.sin(angle_radians))
            
                # Stop radar if it hits black or goes out of bounds
                if (0 <= x < WIDTH and 0 <= y < HEIGHT):
                    if screen.get_at((x, y)) == pygame.Color(20, 174, 92 , 255):  # Check for color
                        break
                else:
                    break

                radar_length += 1

            #draw the radar
            pygame.draw.line(screen,(255,255,255),self.rect.center,(x,y),2)
            pygame.draw.circle(screen,(255,255,255),(x,y),4)
    
    def collision(self):
                                            #GET HEADLIGHT COLLISION POINTS
        angle_radians = math.radians(self.angle)

        #Offset Calculation for the Front of the Car
        #27 is half the the length of the car image
        front_offset_x = 27 * math.cos(angle_radians)
        front_offset_y = -27 * math.sin(angle_radians)

        #Placing the Collision Points at the Headlights
        right_headlight = (int(self.rect.centerx + front_offset_x + math.sin(angle_radians) * 12),
                           int(self.rect.centery + front_offset_y + math.cos(angle_radians) * 12))
        
        left_headlight = (int(self.rect.centerx + front_offset_x - math.sin(angle_radians) * 12),
                          int(self.rect.centery + front_offset_y - math.cos(angle_radians) * 12))
        
        # Draw collision points for visualization

        #if you uncomment the two lines below , the color detection in the CHECK COLLISION section will not work \
        # because it will detect the headlight colors instead of the background color

        #pygame.draw.circle(screen, (195, 255, 0), right_headlight, 3)  # Right headlight in blue
        #pygame.draw.circle(screen, (195, 255, 0), left_headlight, 3)   # Left headlight in red

                                            #CHECK COLLISION
        right_x, right_y = right_headlight
        left_x, left_y = left_headlight
    
        # Ensure the coordinates are within bounds before checking pixel color
        if 0 <= right_x < WIDTH and 0 <= right_y < HEIGHT and screen.get_at(right_headlight) == pygame.Color(20, 174, 92, 255) : 
            self.alive = False
            print("Collision detected at right headlight!")
            
        if (0 <= left_x < WIDTH and 0 <= left_y < HEIGHT and 
            (screen.get_at(left_headlight) == pygame.Color(20, 174, 92, 255))):
            self.alive = False
            print("Collision detected at left headlight!")
        
    def update_car(self):
        self.move()
        self.radar()
        self.collision()
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

        screen.blit(track_img,(0,0))
        car.update_car()
        pygame.display.flip()

        clock.tick(60) # limits FPS to 60

if __name__ == "__main__":
    main()
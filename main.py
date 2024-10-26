import pygame , sys , os , math , neat

# pygame setup
pygame.init()
WIDTH,HEIGHT = 1280,720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("AI-CAR-SIMULATION")
clock = pygame.time.Clock()

track_img = pygame.image.load(os.path.join("assets","track_assets","track2.png"))

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
        self.rotation_speed = 5
        self.alive = True
        self.radar_distances = []
        self.timer = 0

    def move_ai(self,output):

        if output[0] > 0.5:
            self.angle += self.rotation_speed
        if output[1] > 0.5:
            self.angle -= self.rotation_speed

        if output[2] > 0.5 and self.car_speed < self.max_speed:
            self.car_speed += self.accelaration
        elif self.car_speed > 0:
            self.car_speed -= self.accelaration

        # Convert angle to radians and calculate the x, y movement
        radians = math.radians(self.angle)
        self.rect.x += self.car_speed * math.cos(radians)
        self.rect.y -= self.car_speed * math.sin(radians)

    def radar(self):
        
        radar_angles_list = [-60,-30,0,30,60]
        
        x = int(self.rect.centerx)
        y = int(self.rect.centery)

        self.radar_distances = []

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
            self.radar_distances.append(radar_length)

            #draw the radar
            pygame.draw.line(screen,(255,255,255),self.rect.center,(x,y),1)
            pygame.draw.circle(screen,(255,255,255),(x,y),2)
    
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
        if (0 <= right_x < WIDTH and 0 <= right_y < HEIGHT and 
            (screen.get_at(right_headlight) == pygame.Color(20, 174, 92, 255))): 
            self.alive = False
            
        if (0 <= left_x < WIDTH and 0 <= left_y < HEIGHT and 
            (screen.get_at(left_headlight) == pygame.Color(20, 174, 92, 255))):
            self.alive = False
        
    def update_car(self,output):
        self.move_ai(output)
        self.radar()
        self.collision()

        # if i put self.car_speed == 0 some cars will not be deleted even if they dont move
        # self.accelaration = 0.1
        if self.car_speed < 0.1:
            self.timer += 1 / 60  #60 FPS 
        else:
            self.timer = 0  # reset if the car moves
        # Mark the car as dead if idle for more than 3 seconds
        if self.timer > 1:
            self.alive = False

        self.draw()
        
    def draw(self):
        rotated_img = pygame.transform.rotate(self.car_img,self.angle)
        rotated_rect = rotated_img.get_rect(center=(self.rect.center))
        screen.blit(rotated_img,rotated_rect)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

#Fitness Function
def eval_genomes(genomes, config):
    # Initialize a list to hold all cars for this generation
    cars = []
    nets = []
    genomes_list = []

    # Create a car, neural network, and genome entry for each genome
    for genome_id , genome in genomes:
        car = Car(300,100)
        cars.append(car)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genomes_list.append(genome)

        genome.fitness = 0 #evaluation with fitness

    run = True
    while run and len(cars) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(track_img,(0,0))


        for i , car in enumerate(cars):
            # Increase fitness if the car stay alive
            if car.car_speed > 0:
                genomes_list[i].fitness += 1
            else:
                genomes_list[i].fitness -= 1
            
            # Check for collision and remove the car if it crashes
            if not car.alive:
                cars.pop(i)
                nets.pop(i)
                genomes_list.pop(i)
                continue
            car.radar()  # Calculate radar distances
            # Get the output from the neural network for the car’s radar distances
            output = nets[i].activate(car.radar_distances)
            car.update_car(output)  # Update car with NEAT output

        
        pygame.display.flip()
        clock.tick(60) # limits FPS to 60

def run_neat(config_file):
    config = neat.config.Config(
                        neat.DefaultGenome, 
                        neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, 
                        neat.DefaultStagnation,
                        config_file
            )
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # 50 is the max generations will be created
    population.run(eval_genomes,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run_neat(config_path)
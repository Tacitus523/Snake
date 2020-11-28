import pygame
import random

#Initilaze
pygame.font.init()

#colors
white=(240,240,240)
black=(0,0,0)

#Screen settings
WIDTH,HEIGHT=800,600
SIZE=25
screen = pygame.display.set_mode((WIDTH+10,HEIGHT+10))
screen.fill(black)
gamearea = pygame.Surface((WIDTH,HEIGHT))
pygame.display.set_caption("Snake")
#icon = pygame.image.load('ship.png')
#pygame.display.set_icon(icon)
#background=pygame.transform.scale(pygame.image.load('mars.jpg'),(WIDTH,HEIGHT))

def pixelate(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        if wrapped.calls>4:
            wrapped.calls=0 
            return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

#Baseclass
class Object():
    img=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def show(self):
        gamearea.blit(self.img,(self.x,self.y))

    def get_width(self):
        return pygame.image.get_width(self.img)

    def get_height(self):
        return pygame.image.get_height(self.img)

    def collide(self, other):
        delta_x = int(self.x-other.x)
        delta_y = int(self.y-other.y)
        rect_1=pygame.Rect(self.x,self.y,SIZE,SIZE)
        rect_2=pygame.Rect(other.x,other.y,SIZE,SIZE)
        return rect_1.colliderect(rect_2)

class Snake(Object):
    img = pygame.image.load('pixel.png')
    img = pygame.transform.scale(img, (SIZE, SIZE))
    vel = 3
    x_vel = vel
    y_vel = 0
    progress_x = 0
    progress_y = 0
    def __init__(self,x,y):
        super().__init__(x,y)
        self.show_x=x
        self.show_y=y
        self.next=None

    def eat(self, food):
        if self.collide(food):
            food.respawn()
            return True
        return False

    def move(self, food):
        def pull_tail(snake_body):
            if snake_body.next:
                pull_tail(snake_body.next)
                snake_body.next.x, snake_body.next.y = snake_body.x, snake_body.y

            elif growth:
                snake_body.next=(Snake(snake_body.x,snake_body.y))

            snake_body.show_x=snake_body.x//SIZE*SIZE
            snake_body.show_y=snake_body.y//SIZE*SIZE

        progress_x = self.x % SIZE
        progress_y = self.y % SIZE
        
        if self.x_vel>0 or self.y_vel>0:
            if progress_x < self.progress_x or progress_y < self.progress_y:
                growth=self.eat(food)
                pull_tail(self)
                Snake.progress_x = 0
                Snake.progress_y = 0
        
        elif self.x_vel<0 or self.y_vel<0:
            if progress_x > self.progress_x or progress_y > self.progress_y:
                growth=self.eat(food)
                pull_tail(self)
                Snake.progress_x = SIZE
                Snake.progress_y = SIZE

        else:
            Snake.progress_x = progress_x
            Snake.progress_y = progress_y
        
        self.x += self.x_vel
        self.y += self.y_vel

        print((food.x,food.y),(self.x,self.y))
    
    def show(self):
        gamearea.blit(self.img,(self.show_x,self.show_y))
        if self.next:
            self.next.show()



class Food(Object):
    img = pygame.image.load('pixel.png')
    img = pygame.transform.scale(img, (SIZE, SIZE))
    border_x=range(0,WIDTH,SIZE)
    border_y=range(0,HEIGHT,SIZE)

    def __init__(self):
        self.x=random.choice(self.border_x)
        self.y=random.choice(self.border_y)

    def respawn(self):
        self.x=random.choice(self.border_x)
        self.y=random.choice(self.border_y)


def game_over(head):
    if head.x<0 or head.y<0 or head.x>WIDTH or head.y>HEIGHT:
        print("game over")
        return False
    
    # if head.next:
    #     body=head.next
    #     while True:
    #         if head.x==body.x or head.y==body.y:
    #             print("game over")
    #             return False
            
    #         if body.next:
    #             body=body.next
    #         else:
    #             break
    
    return True

def main_menu():
    menu_font=pygame.font.SysFont('impact',40)
    title_label=menu_font.render("Snake",True,(0,0,0))
    menu_label=menu_font.render("Press Enter to play",True,(0,0,0))
    running=True
    while running:
        gamearea.fill(white)
        gamearea.blit(title_label,((WIDTH-title_label.get_width())/2,(HEIGHT-menu_label.get_height()-100)/2))
        gamearea.blit(menu_label,((WIDTH-menu_label.get_width())/2,(HEIGHT-menu_label.get_height())/2))
        screen.blit(gamearea,(5,5))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                play_snake()
    pygame.quit()


def play_snake():
    #set Clock
    FPS = 30
    clock = pygame.time.Clock()

    head=Snake(int(WIDTH/2),int(HEIGHT/2))
    food=Food()

    running = True
    while running:
        clock.tick(FPS)

        #Keyyboard Interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    if head.x_vel==0:
                        head.x_vel=-head.vel
                        head.y_vel=0
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    if head.x_vel==0:
                        head.x_vel=head.vel
                        head.y_vel=0
                elif event.key==pygame.K_UP or event.key==pygame.K_w:
                    if head.y_vel==0:
                        head.x_vel=0
                        head.y_vel=-head.vel
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    if head.y_vel==0:
                        head.x_vel=0
                        head.y_vel=head.vel
        running=game_over(head)
        gamearea.fill(white)
        head.show()
        food.show()
        head.move(food)
        screen.blit(gamearea,(5,5))
        pygame.display.update()




if __name__ == "__main__":
    main_menu()


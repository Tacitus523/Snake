import pygame
import random

#Initilaze
pygame.font.init()

#Highscore
with open('highscore.txt','r') as f:
    highscore=f.readline()

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
    vel = SIZE
    x_vel = vel
    y_vel = 0
    progress = 0
    fill_progress = 15
    score = 0
    def __init__(self,x,y):
        super().__init__(x,y)
        self.next=None

    def eat(self, food):
        if self.collide(food):
            food.respawn()
            Snake.fill_progress += 2.5
            Snake.score += 1
            return True
        return False

    def move(self, food):
        def pull_tail(snake_body):
            if snake_body.next:
                pull_tail(snake_body.next)
                snake_body.next.x, snake_body.next.y = snake_body.x, snake_body.y

            elif growth:
                snake_body.next=(Snake(snake_body.x,snake_body.y))

        Snake.progress += Snake.fill_progress

        if Snake.progress > 100:
            growth=self.eat(food)
            pull_tail(self)
            Snake.progress = Snake.progress%100

            self.x += self.x_vel
            self.y += self.y_vel

    @classmethod
    def spawn(cls, start_x, start_y):
        head = Snake(start_x,start_y)
        head.next = Snake(start_x-SIZE,start_y)
        head.next.next = Snake(start_x-SIZE*2,start_y)
        head.next.next.next = Snake(start_x-SIZE*3,start_y)
        head.next.next.next.next = Snake(start_x-SIZE*4,start_y)
        return head

    def show(self):
        gamearea.blit(self.img,(self.x,self.y))
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
    def show_game_over():
            game_over_font=pygame.font.SysFont('impact',70)
            score_font=pygame.font.SysFont('impact',30)

            game_over_label=game_over_font.render("GAME OVER",True,(0,0,0))
            score_label=score_font.render("Score: "+str(Snake.score),True,(0,0,0))
            highscore_label=score_font.render("Highscore: "+str(highscore),True,(0,0,0))


            #update highscore
            if Snake.score>int(highscore):
                with open('highscore.txt','w') as f:
                    try:
                        f.write(str(Snake.score))
                    except:
                        pass
            x=WIDTH/2
            y=0
            while y<=250:
                y+=1
                gamearea.fill(white)
                gamearea.blit(game_over_label,(x-game_over_label.get_width()/2,y))
                screen.blit(gamearea,(5,5))
                pygame.time.wait(4)
                pygame.display.update()

            screen.blit(score_label,(x-score_label.get_width()/2,y+80))
            screen.blit(highscore_label,(x-highscore_label.get_width()/2,y+120))
            pygame.display.update()
            pygame.time.wait(3000)
    
    if head.x<0 or head.y<0 or head.x+SIZE>WIDTH or head.y+SIZE>HEIGHT:
        show_game_over()
        return False
    
    if head.next:
        body=head.next
        while body:
            if head.collide(body):
                show_game_over()
                return False
            body=body.next

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

    #font
    highscore_font=pygame.font.SysFont('forte',24)
    
    Snake.fill_progress = 15
    Snake.score = 0
    start_x, start_y = int(WIDTH/2),int(HEIGHT/2)
    head=Snake.spawn(start_x, start_y)
    food=Food()

    running = True
    while running:
        clock.tick(FPS)
        score=highscore_font.render("Score: "+str(Snake.score),True,(0,0,0))
        
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
        gamearea.blit(score,(WIDTH-10-score.get_width(),10))
        screen.blit(gamearea,(5,5))
        pygame.display.update()




if __name__ == "__main__":
    main_menu()


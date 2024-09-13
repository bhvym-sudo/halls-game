from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random

'''
TODO
1) make a pathway going to right or left before showing anomalies , as in the present game the person can see the anomalies from the lift only
2) add some shaders or colors , so the game looks good.
3) add more anomalies and using random , randomize them on each floor where the condition is True by using random ofc
4) define the lightning.
5) add more floors because 5 floors are not enough for the anomalies




'''

app = Ursina()
anomaly_text = None

#ANOMALIES

def reset_anomalies():
    for door in door_entities_left + door_entities_right:
        door.color = color.black
        door.enabled = True


def change_door_color():
    reset_anomalies()
    chosen_door = random.randint(0,4)
    door_entities_left[chosen_door].color = color.white

def change_room_text():
    pass

def light_flickering():
    pass

def door_open():
    pass

def earthquake():
    pass

def floor_texture_change():
    pass



def show_credits(messages, position, color=color.white, delay_between=3):
    def display_next_message(index=0):
        global anomaly_text
        if anomaly_text:
            anomaly_text.disable()  

        if index < len(messages): 
            anomaly_text = Text(messages[index], position=position, color=color)
            destroy(anomaly_text, delay=delay_between) 
            invoke(display_next_message, index + 1, delay=delay_between)  

    display_next_message() 


def show_temporary_text(message, position, color=color.white):
    global anomaly_text
    if anomaly_text:
        anomaly_text.disable()  
    anomaly_text = Text(message, position=position, color=color)
    destroy(anomaly_text, delay=3) 



class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.player = None

        def start():
            print(floors)
            print(floors[current_floor - 1])
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.time_running = True
            invoke(open_elevator_doors, delay=1)

        title = Entity(model="quad", texture="assets/mainmenu", parent=self.main_menu, y=0, scale_x=1.8)
        start_button = Button(text="S t a r t  G a m e", color=color.hsv(0, 0, .5, .6), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=-0.3)
        quit_button = Button(text="Q u i t", color=color.hsv(0, 0, .5, .6), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=0.3)
        quit_button.on_click = application.quit
        start_button.on_click = Func(start)

# Environment setup
ground = Entity(model='cube', collider='box', scale_x=49, scale_z=5, origin_y=4.5, texture='assets/floor2', scale_y=1, shader=lit_with_shadows_shader)
wall1 = Entity(model='cube', collider='box', scale_x=49, scale_z=1, texture='white_cube', scale_y=10, origin_x=0, origin_z=3, origin_y=0, color=color.dark_gray, shader=lit_with_shadows_shader)
wall2 = Entity(model='cube', collider='box', scale_x=49, scale_z=1, texture='white_cube', scale_y=10, origin_x=0, origin_z=-3, origin_y=0, color=color.dark_gray, shader=lit_with_shadows_shader)
wall3 = Entity(model='cube', collider='box', scale_x=1, scale_z=10, texture='white_cube', scale_y=10, origin_x=-25, origin_y=0, color=color.dark_gray, shader=lit_with_shadows_shader)
wall4 = Entity(model='cube', collider='box', scale_x=1, scale_z=10, texture='white_cube', scale_y=10, origin_x=25, origin_y=0, color=color.dark_gray, shader=lit_with_shadows_shader)

elevator_gate1 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, 1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray, collider='box')
elevator_gate2 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, -1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray, collider='box')

roof = Entity(model='cube', collider='box', scale_x=49, scale_z=5, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.black90)
roof.y = 5
liftroof = Entity(model='cube', collider='box', scale_x=4, scale_z=6, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.dark_gray, position=(-22.5, 3, 0))

door_entities_left = []
door_entities_right = []
text_entities_left = []
text_entities_right = []

door_texts_left = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5"]
door_texts_right = ["Room 10", "Room 9", "Room 8", "Room 7", "Room 6"]

for i in range(5):
    door1 = Entity(model='cube', collider='box', scale=(2, 3.8, 0.05), texture='white_cube', origin=(i * -3, 0.6, -49), color=color.black, x=-12, shader=lit_with_shadows_shader)
    door2 = Entity(model='cube', collider='box', scale=(2, 3.8, 0.05), scale_x=2, texture='white_cube', origin=(i * -3, 0.6, 49), color=color.black, x=-12, shader=lit_with_shadows_shader)
    text = Text(text=door_texts_left[i], parent=door1, scale=(3, 3, 3), color=color.black)
    text2 = Text(text=door_texts_right[i], parent=door2, scale=(3, 3, 3), color=color.black, rotation=(180, 0, 180))
    text.position = ((i * 3) - 0.1, 0, 49)
    text2.position = ((i * 3) + 0.1, 0, -49)
    door_entities_left.append(door1)
    door_entities_right.append(door2)
    text_entities_left.append(text)
    text_entities_right.append(text2)

m = MainMenu()
player = FirstPersonController()
player.y = -4
player.x = -24
player.rotation_y = 90
player.disable()
player.speed = 9
m.player = player
player.height = 4
player.cursor.color = color.red

shift_player = 3
s = Sky(texture='assets/walltext.png')


floors = [False, False, False, False, False] 
current_floor = 5

def randomize_floors():
    global floors
    floors = [random.choice([True, False]) for _ in range(5)]
    if not any(floors):
        floors[random.randint(0, 4)] = True

def reset_game():
    global current_floor
    current_floor = 5
    randomize_floors()
    apply_anomalies()
    player.y = -4 
def apply_anomalies():
    
    if floors[current_floor - 1]: 
        anomaly_index = current_floor - 1  
        
        change_door_color()
    else:
        reset_anomalies()

def destroy_doors():
    for door in door_entities_left:
        destroy(door)

    for door in door_entities_right:
        destroy(door)

def update_floor(floor_delta):
    global current_floor
    global floors
    next_floor = current_floor + floor_delta

    if next_floor < 1:
        current_floor = 1
        show_temporary_text("Congratulations, you cleared the game!", position=(0.38, -0.3))
        player.rotation_y = 90
        player.rotation_x = 10
        player.x = -19
        s.texture="sky_default"
        player.cursor.disable()
        player.disable()
        destroy(wall1, delay=2)
        destroy(wall2, delay=2)
        destroy(wall3, delay=2)
        destroy(wall4, delay=2)
        destroy(roof,delay=2)
        destroy(door1, delay=2)
        destroy(door2, delay=2)
        destroy(text, delay=2)
        destroy(text2, delay=2)
        destroy(spotlight, delay=2)
        destroy(up, delay=2)
        destroy(down, delay=2)
        destroy(liftroof, delay=2)
        destroy_doors()
        pivot = Entity()
        DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
        credits = [
            "Thank you for playing HALLS!",
            "Made by odd ones",
            "Team Leader: Sanchit",
            "Lead Developer: Bhavyam",
            "Logic Developer: Sanchit",
            "Research: Satyansh",
            "Management and Presentation: Tanu and Pragya",
            "Ideas given by: Tanika"
        ]

        show_credits(credits, position=(-0.2, 0), color=color.white, delay_between=5)
        

    elif next_floor > 5:
        current_floor = 5
        show_temporary_text("Same floor again.", position=(0.38, 0))
    else:
        current_floor = next_floor
        # show_temporary_text(f"Correct! Moving to floor {current_floor}", position=(0.38, 0))

    apply_anomalies()
    print(f"Current floor: {current_floor}, Floors: {floors}")

def update():
    if player.y < -40:
        player.y = 3
    if player.x > -20:
        if doors_open:
            invoke(close_elevator_doors, delay=2)
    
    Text(text=f"Current floor: {current_floor}", position=(0.38, 1))

def input(key):
    global doors_open
    player.speed = shift_player if held_keys['shift'] else 7

    if key == "h":
        invoke(open_elevator_doors, delay=0)
    

doors_open = False

def open_elevator_doors():
    global doors_open
    elevator_gate1.position = Vec3(-20, 0, 1.25)
    elevator_gate2.position = Vec3(-20, 0, -1.25)
    elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, 2), duration=1)
    elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, -2), duration=1) 
    doors_open = True
    invoke(close_elevator_doors, delay=3)  

def close_elevator_doors():
    global doors_open
    if doors_open:
        elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, -2), duration=1) 
        elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, 2), duration=1) 
        doors_open = False


class ElevatorUp(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="Anomaly Spotted", 
            color=color.hsv(0, 0, .5, .5),
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-1,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if floors[current_floor - 1]:  
                    show_temporary_text(f"Correct! Moving down to {current_floor-1}", position=(0.38, -0.3))
                    update_floor(-1) 
                    invoke(open_elevator_doors, delay=2)

                else:
                    show_temporary_text(f"Wrong! Moving back up to {current_floor+1}", position=(0.38, 0.3))
                    update_floor(1) 
                    invoke(open_elevator_doors, delay=2)

class ElevatorDown(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="No Anomaly Spotted", 
            color=color.hsv(0, 0, .5, .5), 
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-2,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if not floors[current_floor - 1]:  
                        show_temporary_text(f"Correct! Moving down to {current_floor-1}", position=(0.38, -0.3))
                        update_floor(-1)
                        invoke(open_elevator_doors, delay=2)
                else: 
                    show_temporary_text(f"Wrong! Moving back up to {current_floor+1}", position=(0.38, 0.3))
                    update_floor(1)
                    invoke(open_elevator_doors, delay=2)
                    


up = ElevatorUp()
down = ElevatorDown()

up.text_entity.scale = (4, 10)
up.text_entity.color = color.white
down.text_entity.scale = (4, 10)
down.text_entity.color = color.white

spotlight = PointLight(parent=camera, position=(0, 0, 0), rotation=(0, 0, 0),fov=90, color=color.rgb(5,5,5), shadows=True)

reset_game()
window.render_mode = 'default'
window.borderless = False
app.run()
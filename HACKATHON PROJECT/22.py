from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random

app = Ursina()
anomaly_text = None

def show_temporary_text(message, position, color=color.white):
    global anomaly_text
    if anomaly_text:
        anomaly_text.disable()  
    anomaly_text = Text(message, position=position, color=color)
    destroy(anomaly_text, delay=3) 

# Window settings
window.fullscreen = True

class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.player = None

        def start():
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

elevator_gate1 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, 1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray,collider='box')
elevator_gate2 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, -1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray,collider='box')

roof = Entity(model='cube', collider='box', scale_x=49, scale_z=5, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.black90)
roof.y = 5
liftroof = Entity(model='cube', collider='box', scale_x=4, scale_z=6, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.dark_gray, position=(-22.5,3,0))

door_texts_left = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5"]
door_texts_right = ["Room 10", "Room 9", "Room 8", "Room 7", "Room 6"]
for i in range(5):
    door1 = Entity(model='cube', collider='box', scale=(2,3.8,0.05), texture='white_cube', origin=(i*-3, 0.6, -49), color=color.black, x=-12,shader=lit_with_shadows_shader)
    door2 = Entity(model='cube', collider='box', scale=(2,3.8,0.05), scale_x=2, texture='white_cube', origin=(i*-3, 0.6, 49), color=color.black, x=-12,shader=lit_with_shadows_shader)
    text = Text(text=door_texts_left[i], parent=door1, scale=(3, 3, 3), color=color.black)
    text2 = Text(text=door_texts_right[i], parent=door2, scale=(3, 3, 3), color=color.black, rotation=(180, 0, 180))
    text.position = ((i * 3) - 0.1, 0, 49)
    text2.position = ((i * 3) + 0.1, 0, -49)

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
Sky(texture='assets/walltext.png')

# Floor states and logic
floors = [False, False, False, False, False]  # False means no anomaly, True means anomaly
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
    player.y = -4  # Ensuring player starts on the correct floor

reset_game()

def update_floor(floor_delta):
    global current_floor
    next_floor = current_floor + floor_delta

    if next_floor < 1:
        current_floor = 1
        show_temporary_text("Congratulations, you cleared the game!", position=(0.38, -0.3))
    elif next_floor > 5:
        current_floor = 5
        show_temporary_text("Same floor again.", position=(0.38, 0))
    else:
        current_floor = next_floor
        show_temporary_text(f"Moving to floor {current_floor}", position=(0.38, 0))

    print(f"Current floor: {current_floor}, Floors: {floors}")

def update():
    if player.y < -40:
        player.y = 3
    if player.x > -20:
        if doors_open:
            invoke(close_elevator_doors, delay=2)

def input(key):
    global doors_open
    player.speed = shift_player if held_keys['shift'] else 7

    if key == "h":
        invoke(open_elevator_doors, delay=3)

doors_open = False

def open_elevator_doors():
    global doors_open
    # Resetting doors to their closed positions before opening them
    elevator_gate1.position = Vec3(-20, 0, 1.25)
    elevator_gate2.position = Vec3(-20, 0, -1.25)

    # Animate doors to open
    elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, 2), duration=2)
    elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, -2), duration=2)
    doors_open = True
    invoke(close_elevator_doors, delay=3)

def close_elevator_doors():
    global doors_open
    if doors_open:
        # Animate doors to close
        elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, -2), duration=2)
        elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, 2), duration=2)
        doors_open = False

class ElevatorUp(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="Anomaly Spotted", 
            color=color.black,
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-1,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if floors[current_floor - 1]:  # Correct choice, anomaly present
                    show_temporary_text("Correct! Moving down.", position=(0.38, -0.3))
                    update_floor(-1) 
                else:  # Incorrect choice, anomaly not present
                    show_temporary_text("Wrong! Moving back up.", position=(0.38, 0.3))
                    update_floor(1) 

class ElevatorDown(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="No Anomaly Spotted", 
            color=color.black, 
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-2,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if current_floor == 1:  # Already at the lowest floor
                    show_temporary_text("You're already on the ground floor!", position=(0.38, -0.3))
                else:
                    if not floors[current_floor - 1]:  # Correct choice, no anomaly present
                        show_temporary_text("Correct! Moving down.", position=(0.38, -0.3))
                        update_floor(-1)
                    else:  # Incorrect choice, anomaly present
                        show_temporary_text("Wrong! Moving back up.", position=(0.38, 0.3))
                        update_floor(1)

def show_temporary_text(message, position, color=color.white):
    global anomaly_text 
    if anomaly_text:
        anomaly_text.disable()  
    anomaly_text = Text(message, position=position, color=color)
    destroy(anomaly_text, delay=3)

# Window settings


# Main Menu setup remains the same as previous code...

# Environment setup (walls, roof, elevator, etc.)

# Create a new class for the door to allow opening and closing
class Door(Entity):
    def __init__(self, position=(0,0,0), is_open=False, **kwargs):
        super().__init__(model='cube', scale=(2, 3.8, 0.05), position=position, color=color.black, shader=lit_with_shadows_shader, **kwargs)
        self.is_open = is_open
        if self.is_open:
            self.open()

    def open(self):
        self.animate_position(self.position + Vec3(1, 0, 0), duration=1)

    def close(self):
        self.animate_position(self.position - Vec3(1, 0, 0), duration=1)

# Randomizing anomalies for each floor
def randomize_anomalies():
    anomalies = {'doors': [], 'lights': []}
    for i in range(5):
        # Randomly select if a door will be open or not
        anomalies['doors'].append(random.choice([True, False]))

        # Randomly decide if lights will be off on a floor
        anomalies['lights'].append(random.choice([True, False]))
    
    return anomalies

# Apply anomalies on a floor
def apply_anomalies(floor_index, anomalies):
    # Handle door anomalies
    if anomalies['doors'][floor_index]:
        door = Door(position=(-12, 0, floor_index * 3), is_open=True)
    else:
        door = Door(position=(-12, 0, floor_index * 3), is_open=False)

    # Handle light anomalies
    if anomalies['lights'][floor_index]:
        light = Entity(model='cube', scale=(1, 1, 1), position=(0, 5, 0), color=color.black)
    else:
        light = Entity(model='cube', scale=(1, 1, 1), position=(0, 5, 0), color=color.white)

# Game setup logic
floors = [False, False, False, False, False]  # False means no anomaly, True means anomaly
current_floor = 5
anomalies = randomize_anomalies()

def reset_game():
    global current_floor
    current_floor = 5
    randomize_floors()
    apply_anomalies(current_floor - 1, anomalies)

reset_game()

def update_floor(floor_delta):
    global current_floor
    next_floor = current_floor + floor_delta

    if next_floor < 1:
        current_floor = 1
        show_temporary_text("Congratulations, you cleared the game!", position=(0.38, -0.3))
    elif next_floor > 5:
        current_floor = 5
        show_temporary_text("Same floor again.", position=(0.38, 0))
    else:
        current_floor = next_floor
        show_temporary_text(f"Moving to floor {current_floor}", position=(0.38, 0))

    # Apply anomalies for the new floor
    apply_anomalies(current_floor - 1, anomalies)

# ElevatorUp and ElevatorDown logic...

# Game loop
app.run()



# Instantiate elevator buttons
up = ElevatorUp()
down = ElevatorDown()

# Adjust text entity properties for buttons
up.text_entity.scale = (4, 10)
up.text_entity.color = color.white
down.text_entity.scale = (4, 10)
down.text_entity.color = color.white

# Game loop
window.render_mode = 'default'
app.run()


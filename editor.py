import pygame, sys, tkinter as tk
from scripts.scenemap import Scenemap
from scripts.utils import SCREEN_SIZE, load_image, load_images, load_maps

pygame.init()

BASE_MAP_PATH: str = 'assets_editor/scenes/'

class Editor():
    def __init__(self):
        # Anotate variables
        self.screen: pygame.Surface
        self.display: pygame.Surface
        self.clock: pygame.time.Clock
        self.running: bool
        self.assets: dict
        self.scenemap: Scenemap
        self.scene_list: list
        self.surf_list: list
        self.surf_type: int
        self.surf_variant:int
        self.left_click: bool
        self.right_click: bool
        self.shift: bool

        self.saving: bool
        self.map_name: str

        # Initializing variables
        pygame.display.set_caption('Scene Editor')
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.display = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = {
            'characters_far': load_images('characters_far'),
            'characters_talking': load_images('characters_talking'),
        }
        self.scenemap = Scenemap(self)
        self.surf_list = list(self.assets)
        self.surf_type = 0
        self.surf_variant = 0

        self.scene_list = load_maps()

        self.left_click = False
        self.right_click = False
        self.shift = False

        self.saving = False
        self.map_name = 'untitled'
        print(self.scene_list)

    def run(self):
        while self.running:
            self.display.fill((255, 255, 255))
            self.scenemap.render(self.display)

            current_surf_img = self.assets[self.surf_list[self.surf_type]][self.surf_variant].copy()
            current_surf_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            self.display.blit(current_surf_img, mpos)

            if self.left_click:
                pass

            if self.right_click:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        self.left_click = True
                        self.scenemap.scenemap.append({
                            'type': self.surf_list[self.surf_type], 
                            'variant': self.surf_variant, 
                            'pos': (mpos[0], mpos[1]), 
                            'size': pygame.Surface.get_size(self.assets[self.surf_list[self.surf_type]][self.surf_variant])
                        })
                    if event.button == 3: # Right click
                        self.right_click = True
                        print(self.scenemap.scenemap)
                    if self.shift:
                        if event.button == 4:
                            self.surf_type = (self.surf_type - 1) % len(self.surf_list)
                            self.surf_variant = 0
                        if event.button == 5:
                            self.surf_type = (self.surf_type + 1) % len(self.surf_list)
                            self.surf_variant = 0
                    else:
                        if event.button == 4:
                            self.surf_variant = (self.surf_variant - 1) % len(self.assets[self.surf_list[self.surf_type]])
                        if event.button == 5:
                            self.surf_variant = (self.surf_variant + 1) % len(self.assets[self.surf_list[self.surf_type]])
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.left_click = False
                    if event.button == 3:
                        self.right_click = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                        self.shift = True
                    if event.key == pygame.K_e:
                        # Tkinter
                        root = tk.Tk()
                        root.title('Saving map?')
                        name_var = tk.StringVar()
                        def submit():
                            name = name_var.get()
                            self.map_name = name
                            self.scenemap.save(name)
                            tk.Label(root, text=f"The map '{name}' has been saved!").grid(row=2, column=0, columnspan=3)
                        tk.Label(root, text='Map Name:').grid(row=0, column=0)
                        tk.Entry(root, textvariable=name_var, width=20).grid(row=0, column=1, columnspan= 2)
                        tk.Button(root, text='Yes', width=20, command=submit).grid(row=1, column=0)
                        tk.Button(root, text='No', width=20, command=root.destroy).grid(row=1, column=1)
                        tk.Button(root, text='Exit', width=20, command=root.destroy).grid(row=1, column=2)
                        root.mainloop()
                        
                    if event.key == pygame.K_o:
                        root = tk.Tk()
                        root.title('Open map?')
                        name_var = tk.StringVar()
                        def submit():
                            name = name_var.get()
                            self.map_name = name
                            try:
                                self.scenemap.load(name)
                            except:
                                tk.Label(root, text=f"The map '{name}' does not exist. Try again.").grid(row=2, column=0, columnspan=3)
                                name_var.set('')
                            else:
                                tk.Label(root, text=f"The map '{name}' loaded succesfully!").grid(row=2, column=0, columnspan=3)
                        tk.Label(root, text='Map Name:').grid(row=0, column=0)
                        tk.Entry(root, textvariable=name_var, width=20).grid(row=0, column=1, columnspan= 2)
                        tk.Button(root, text='Yes', width=20, command=submit).grid(row=1, column=0)
                        tk.Button(root, text='No', width=20, command=root.destroy).grid(row=1, column=1)
                        tk.Button(root, text='Exit', width=20, command=root.destroy).grid(row=1, column=2)
                        root.mainloop()
                                

                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                        self.shift = False

            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()

import pygame, sys
import tkinter as tk
from tkinter import ttk
from scripts.scenemap import Scenemap
from scripts.utils import SCREEN_SIZE, load_images, get_file_names, BASE_IMG_PATH

pygame.init()

class Editor():
    def __init__(self):
        '''
        param self.surf_list -> a list of types of assets in self.assets
        '''
        # Anotate variables
        self.screen: pygame.Surface
        self.display: pygame.Surface
        self.clock: pygame.time.Clock
        self.running: bool
        self.assets: dict
        self.scenemap: Scenemap
        self.surf_list: list
        self.bg_list: list
        self.surf_type: int
        self.surf_variant:int
        self.left_click: bool
        self.right_click: bool
        self.shift: bool
        self.ctrl:bool
        self.scene_name: str
        self.bg: str

        # Initializing variables
        pygame.display.set_caption('Scene Editor')
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.display = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = {
            'characters_far': load_images('characters_far'),
            'characters_talking': load_images('characters_talking'),
            'backgrounds': load_images("backgrounds")
        }
        self.scenemap = Scenemap(self)
        self.surf_list = []
        self.bg_list = []
        for type in self.assets:
            if type == 'backgrounds':
                self.bg_list.append(type)
                continue
            self.surf_list.append(type)
        self.surf_type = 0
        self.surf_variant = 0
        self.bg_variant = 0

        self.left_click = False
        self.right_click = False
        self.shift = False
        self.ctrl = False

        self.scene_name = 'untitled'
        self.bg = 'none'

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
                for asset in self.scenemap.scene_map.copy():
                    asset_surf:pygame.Surface = self.assets[asset['type']][asset['variant']]
                    asset_rect:pygame.FRect = pygame.FRect(asset['pos'][0], asset['pos'][1], asset_surf.get_width(), asset_surf.get_height())
                    if asset_rect.collidepoint(mpos):
                        self.scenemap.scene_map.remove(asset)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        self.left_click = True
                        print(self.assets[self.surf_type][self.surf_variant])
                        self.scenemap.scene_map.append({
                            'name': get_file_names(BASE_IMG_PATH + str(self.surf_list[self.surf_type]), '_')[self.surf_variant],
                            'type': self.surf_list[self.surf_type], 
                            'variant': self.surf_variant, 
                            'pos': (mpos[0], mpos[1]), 
                            'size': pygame.Surface.get_size(self.assets[self.surf_list[self.surf_type]][self.surf_variant])
                        })
                    if event.button == 3: # Right click
                        self.right_click = True
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
                    if event.key == pygame.K_LCTRL or pygame.K_RCTRL:
                        self.ctrl = True

                    if event.key == pygame.K_m:
                        backgrounds:list = get_file_names(BASE_IMG_PATH + 'backgrounds')
                        backgrounds.insert(0, 'none')

                        # Creating tkinter window
                        root = tk.Tk()
                        root.title('Editor Menu')

                        # Creating stringvar
                        scene_var = tk.StringVar()
                        scene_var.set(self.scene_name)
                        bg_var = tk.StringVar()
                        bg_var.set(self.bg)

                        # creating funcs
                        def apply():
                            self.bg = bg_var.get()
                            self.bg_variant = int(backgrounds.index(self.bg)) - 1
                            self.scenemap.scene_bg.append({
                                'variant': self.bg_variant,
                                'pos': (-1, -1)
                            })
                            tk.Label(root, text=f"The background '{self.bg}' has been applied!").grid(row=2, column=0, columnspan=4)

                        def save():
                            self.scene_name = scene_var.get()
                            self.bg = bg_var.get()
                            scenes = get_file_names('assets_editor/scenes')

                            if not scenes: # Scenes list is empty
                                self.scenemap.save(self.scene_name)
                                tk.Label(root, text=f"The map '{self.scene_name}' has been saved!").grid(row=2, column=0, columnspan=4)
                            for existing_scene in scenes:
                                if self.scene_name == existing_scene:
                                    self.scenemap.save(self.scene_name)
                                    tk.Label(root, text=f"The map '{self.scene_name}' has been updated!").grid(row=2, column=0, columnspan=4)
                                else:
                                    self.scenemap.save(self.scene_name)
                                    tk.Label(root, text=f"The map '{self.scene_name}' has been saved!").grid(row=2, column=0, columnspan=4)

                        def open():
                            self.scene_name = scene_var.get()
                            try:
                                self.scenemap.load(self.scene_name)
                            except FileNotFoundError:
                                tk.Label(root, text=f"The map '{self.scene_name}' does not exist. Try again.").grid(row=2, column=0, columnspan=4)
                                scene_var.set('')
                            except:
                                tk.Label(root, text=f"The map '{self.scene_name}' is facing an error. Import traceback and call print_exc().").grid(row=2, column=0, columnspan=4)
                            else:
                                tk.Label(root, text=f"The map '{self.scene_name}' loaded succesfully!").grid(row=2, column=0, columnspan=4)

                        # Map name entry box
                        tk.Label(root, text='Map Name:').grid(row=0, column=0)
                        tk.Entry(root, textvariable=scene_var, width=20).grid(row=0, column=1, columnspan=2)

                        # Background combobox
                        tk.Label(root, text='Background:').grid(row=1, column=0)
                        bg = ttk.Combobox(root, textvariable=bg_var, width=20)
                        bg['values'] = backgrounds
                        bg.grid(row=1, column=1, columnspan=2)
                        bg.current()

                        # Buttons
                        tk.Button(root, text='Apply', width=10, command=apply).grid(row=3, column=0)
                        tk.Button(root, text='Save', width=10, command=save).grid(row=3, column=1)
                        tk.Button(root, text='Open', width=10, command=open).grid(row=3, column=2)
                        tk.Button(root, text='Close', width=10, command=root.destroy).grid(row=3, column=3)

                        # Display menu
                        root.mainloop()
                                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT or pygame.K_RSHIFT:
                        self.shift = False
                    if event.key == pygame.K_LCTRL or pygame.K_RCTRL:
                        self.ctrl = False

            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()

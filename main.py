import sys
import os
import time
import random
import json
import tkinter as tk
from tkinter import ttk
import tft
from unit import Unit
from pygame import mixer

class ThinkFastGUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Think Fast Client")
        self.window_icon_path = self.resource_path("img\general\logo.png")
        self.window_icon = tk.PhotoImage(file=self.window_icon_path)
        self.window.iconphoto(True, self.window_icon)
        mixer.init()

        # Set the window size
        window_width = 1280
        window_height = 720

        # Calculate the X and Y coordinates to center the window
        x_coordinate = (self.window.winfo_screenwidth() - window_width) // 2
        y_coordinate = (self.window.winfo_screenheight() - window_height) // 2

        # Set the window size and position
        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)

        # Initializes variables for user time and the start time
        self.user_gold = None
        self.user_time = None
        self.start_time = None
        self.one_cost = {}
        self.two_cost = {}
        self.three_cost = {}
        self.four_cost = {}
        self.five_cost = {}
        self.costs= [self.one_cost, self.two_cost, self.three_cost, self.four_cost, self.five_cost]
        self.target_team = []
        self.shops = []
        self.shop_count = 0
        self.bought_units = []
        self.seen_units = []
        self.actions = 0
        self.unit_stats = []
        self.refresh_sound = mixer.Sound("sound\\reroll.wav")
        self.buy_sound = mixer.Sound("sound\\purchase.wav")

        # Creates the different frames for the game
        self.landing_frame = tk.Frame(self.window, bg="black")
        self.team_builder_frame = tk.Frame(self.window, bg="white")
        self.game_frame = tk.Frame(self.window, bg="black")
        self.scoreboard_frame = tk.Frame(self.window, bg="black")

        # Loads the landing page for users
        self.landing_frame.pack(fill=tk.BOTH, expand=True)

        # Loads units on start
        self.load_units()

        # Below are the elements of the landing_frame

        # Creates a label to display the background of the landing page
        self.homepage_icon = tk.PhotoImage(file=self.resource_path("img\general\cover.png"))
        self.homepage = tk.Label(self.landing_frame, image=self.homepage_icon)
        self.homepage.grid(row=0, column=0)

        # Creates user inputs
        self.user_input_frame = tk.Frame(self.landing_frame, bg="lightgray", width = 300, height = 200, highlightbackground="gray", highlightthickness=2)
        self.user_input_frame.place(x=490, y=500)

        self.level_label = tk.Label(self.user_input_frame, text="Select Desired Level:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.level_label.grid(row=0, column=0, padx=(10, 0))

        self.level_combobox = ttk.Combobox(self.user_input_frame, value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], width=22, state="readonly")
        self.level_combobox.grid(row=0, column=1, sticky="w", padx=(0,10))

        self.gold_label = tk.Label(self.user_input_frame, text="Enter Desired Gold:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.gold_label.grid(row=1, column=0, padx=(10, 0))

        validate = (self.window.register(self.validate_gold), '%S', '%P')
        self.gold_entry = tk.Entry(self.user_input_frame, width=25, validate="key", validatecommand=validate)
        self.gold_entry.grid(row=1, column=1, sticky="w", padx=(0,10))

        self.time_label = tk.Label(self.user_input_frame, text="Select Time Interval:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.time_label.grid(row=2, column=0, padx=(10, 0))

        self.time_combobox = ttk.Combobox(self.user_input_frame, values=["Normal Rounds (30 sec)", "Augment Round (45 sec)"], width=22, state="readonly")
        self.time_combobox.grid(row=2, column=1, sticky="w", padx=(0,10))

        # Creates a button to continue to the next part of the game
        self.to_team_planner_button = tk.Button(self.landing_frame, text="Next", command=self.to_team_planner, width=10, height=2)
        self.to_team_planner_button.place(x=580, y=640)

        # Below are the elements of the team_builder_frame

        # Creates a label to display the team builder title image
        self.team_builder_img = tk.PhotoImage(file=self.resource_path("img\\general\\team_builder.png"))
        self.team_builder_title_img = tk.Label(self.team_builder_frame, image=self.team_builder_img, width=640, height=100, background="white")
        self.team_builder_title_img.pack(anchor="nw")

        # Creates a frame to hold the champion pool for users to select from
        # Contains a scrollable canvas
        self.champion_select_frame = tk.Frame(self.team_builder_frame, width=420, height=500, background="white", highlightbackground="gold2", highlightthickness=2)
        self.champion_select_frame.place(x=100, y=150)

        self.champion_select_canvas = tk.Canvas(self.champion_select_frame, width=420, height=500, background="white", highlightbackground="gold2", highlightthickness=2, scrollregion=(0,0,400,1500))
        self.champion_select_canvas.pack()
        self.champion_select_canvas.pack_propagate(False)

        champ_select_scrollbar = ttk.Scrollbar(self.champion_select_canvas, orient='vertical', command=self.champion_select_canvas.yview, style="Vertical.TScrollbar")
        self.champion_select_canvas.config(yscrollcommand=champ_select_scrollbar.set)
        # champ_select_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne') # hidden scroll bar
        self.champion_select_canvas.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))

        # Creates 5 more frames to hold the different cost champions
        # Then loops to populate x champion frames and champion icons into the cost frames
        self.teamframes = []
        self.champion_images = [[],[],[],[],[]]
        for i in range(5):
            teamframe = tk.Frame(self.champion_select_canvas, width=400, height=300, background="white")
            self.champion_select_canvas.create_window((0, i * 300), anchor='nw', window=teamframe)
            self.teamframes.append(teamframe)
            teamframe.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))

            for j in range(len(self.costs[i])):
                row = j // 5
                column = j % 5

                champframe = tk.Frame(teamframe, width=50, height=60, background="white")
                champframe.grid(row=row, column=column, padx=10, pady=(10, 0) if row == 0 else (0, 10))
                champframe.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))

                champion_icon = tk.PhotoImage(file=self.resource_path(self.costs[i][list(self.costs[i])[j]].get_icon_path()))
                champion_image = tk.Label(champframe, image=champion_icon, width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
                champion_image.image = champion_icon
                champion_image.grid(row=0, column=0)
                champion_image.name = self.costs[i][list(self.costs[i])[j]].get_name()
                champion_image.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))
                champion_image.bind("<Button-1>", lambda event, label=champion_image: self.select_unit(label))

                champion_name = tk.Label(champframe, text=f"{self.costs[i][list(self.costs[i])[j]].get_name()}", background="white", foreground="black")
                champion_name.grid(row=1, column=0)
                champion_name.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))

                self.champion_images[i].append(champion_image)

        # Creates a label for clarity in team building
        self.arrow_img = tk.PhotoImage(file=self.resource_path("img\\general\\arrow.png"))
        self.arrow_img_label = tk.Label(self.team_builder_frame, image=self.arrow_img, background="white")
        self.arrow_img_label.place(x=550, y=260)

        # Creates a frame for housing the user's chosen team
        self.team_select_frame = tk.Frame(self.team_builder_frame, background="black", highlightbackground="gold2", highlightthickness=2)
        self.team_select_frame.place(x=865, y=265)

        # Creates a label for visibility
        self.user_team_img = tk.PhotoImage(file=self.resource_path("img\\general\\your_team.png"))
        self.user_team = tk.Label(self.team_builder_frame, background="white", image=self.user_team_img)
        self.user_team.place(x=825, y=125)

        # Same as the champion frames but houses the user's selected champions
        self.teammates = []
        for row in range(3):
            for column in range(3):
                teammate_unit = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
                teammate_unit.name = None
                teammate_unit.grid(row=row, column=column, padx=10 if column == 0 else (0, 10), pady=10 if row == 0 else (0, 10))
                self.teammates.append(teammate_unit)

        # Creates a button to continue to the next part of the game
        self.warning_label = tk.Label(self.team_builder_frame, text= "WARNING!! The game starts the moment you press this button. Be ready!", font=("Ariel", 8), background="yellow")
        self.warning_label.place(x=820, y=600)
        self.warning_arrow_img = tk.PhotoImage(file=self.resource_path("img\\general\\arrow2.png"))
        self.warning_arrow = tk.Label(self.team_builder_frame, image=self.warning_arrow_img, background="white")
        self.warning_arrow.place(x=1020, y= 620)
        self.to_game_button = tk.Button(self.team_builder_frame, text="START!", command=self.to_game, width=10, height=2)
        self.to_game_button.place(x=930, y=640)

        # Below are the elements of the game_frame

        # Creates the frame for the timer and initializes the timer
        self.timer_frame = tk.Frame(self.game_frame)
        self.timer_frame.pack(side="top")

        self.timer_label = tk.Label(self.timer_frame, bg="black", fg="red", font=("Ariel", 30))
        self.timer_label.pack()

        # Creates the frame for the shop
        self.shop_frame = tk.Frame(self.game_frame, bg="darkgreen", padx=10, pady=10)
        self.shop_frame.pack(side="bottom")

        # Creates a frame for action buttons
        self.action_frame = tk.Frame(self.shop_frame, bg="darkgreen")
        self.action_frame.grid(row=0, column=0)

        # Creates a frame for displaying user's level, gold, and unit odds
        self.level_frame = tk.Frame(self.game_frame, highlightbackground="darkgreen", highlightthickness=5)
        self.level_frame.place(in_=self.shop_frame, x=-10, y=-40)

        self.gold_frame = tk.Frame(self.game_frame, highlightbackground="darkgreen", highlightthickness=5)
        self.gold_frame.place(in_=self.shop_frame, relx=0.5, x=-10, y=-40)

        self.unit_odds_frame = tk.Frame(self.game_frame, width=300, height=15, highlightbackground="darkgreen", highlightthickness=5)
        self.unit_odds_frame.place(in_=self.level_frame, relx=1.0, rely=0.17)

        # Creates a button for spending gold to level up
        # This button will be clickable but has no function for this version of the game
        # Clicking this button will do nothing
        button_level_up_img = tk.PhotoImage(file=self.resource_path("img\\general\\buy_xp.png"))
        self.button_level_up = tk.Button(self.action_frame, image=button_level_up_img, width=150, height=38, borderwidth=0)
        self.button_level_up.grid(row=0, column=0, padx=5, pady=(3,0))

        # Creates a button for refreshing the shop
        button_refresh_img = tk.PhotoImage(file=self.resource_path("img\\general\\refresh.png"))
        self.button_refresh = tk.Button(self.action_frame, image=button_refresh_img, command=self.refresh, width=150, height=38, borderwidth=0)
        self.button_refresh.grid(row=1, column=0, padx=5, pady=3)

        # Creates and displays the units in the shop
        self.shop_units = []

        for i in range(5):
            self.shop_unit = tk.Label(self.shop_frame, image=None, text=None, bg="darkgreen")
            self.shop_unit.grid(row=0, column=i+1, padx=3)
            self.shop_unit.bind("<Button-1>", lambda event, label=self.shop_unit: self.buy_unit(label))
            self.shop_units.append(self.shop_unit)

        # Creates a label for displaying player's desired gold and level
        self.level = tk.Label(self.level_frame, font=("Ariel", 16), padx=5)
        self.level.pack()
        self.gold = tk.Label(self.gold_frame, font=("Ariel", 16), padx=5)
        self.gold.pack()

        # Handles processing and labelling unit odds based on user's chosen level
        self.one_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="#c3c3c3")
        self.one_cost_odds.grid(row=0, column=0)
        self.two_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="#22b14c")
        self.two_cost_odds.grid(row=0, column=1)
        self.three_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="#3f48cc")
        self.three_cost_odds.grid(row=0, column=2)
        self.four_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="#a349a4")
        self.four_cost_odds.grid(row=0, column=3)
        self.five_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="#ff7f27")
        self.five_cost_odds.grid(row=0, column=4)

        # Below are the elements of the scoreboard_frame

        # Creates a label to display the scoreboard title image
        scoreboard_img_path = self.resource_path("img\\general\\scoreboard.png")
        self.scoreboard_img = tk.PhotoImage(file=scoreboard_img_path)
        self.scoreboard_label = tk.Label(self.scoreboard_frame, image=self.scoreboard_img, background="black")
        self.scoreboard_label.pack(side="top")

        # Creates a frame to hold elements of the scoreboard
        self.scoreboard_elements_frame = tk.Frame(self.scoreboard_frame, bg="black", width=1200, height=500)
        self.scoreboard_elements_frame.pack()
        self.scoreboard_elements_frame.pack_propagate(False)

        # Creates a frame to hold the user's scores
        self.user_scoreboard_frame = tk.Frame(self.scoreboard_elements_frame, bg="black", width=800, height=500)
        self.user_scoreboard_frame.pack(side="left")
        self.user_scoreboard_frame.pack_propagate(False)

        self.actions_label = tk.Label(self.user_scoreboard_frame, text="Actions:", font=("Ariel", 30), bg="black", fg="white")
        self.actions_label.pack(side="top", anchor="w")

        self.apm_label = tk.Label(self.user_scoreboard_frame, text="APM:", font=("Ariel", 30), bg="black", fg="white")
        self.apm_label.pack(side="top", anchor="w", pady=(20, 0))

        self.hits_label = tk.Label(self.user_scoreboard_frame, text="Hits:", font=("Ariel", 30), bg="black", fg="white")
        self.hits_label.pack(side="top", anchor="w", pady=(20, 0))

        self.misses_label = tk.Label(self.user_scoreboard_frame, text="Misses:", font=("Ariel", 30), bg="black", fg="white")
        self.misses_label.pack(side="top", anchor="w", pady=(20, 0))

        self.rolled_past_label = tk.Label(self.user_scoreboard_frame, text="Rolled Past:", font=("Ariel", 30), bg="black", fg="white")
        self.rolled_past_label.pack(side="top", anchor="w", pady=(20, 0))

        self.hit_percentage_label = tk.Label(self.user_scoreboard_frame, text="Hit Percentage:", font=("Ariel", 30), bg="black", fg="white")
        self.hit_percentage_label.pack(side="top", anchor="w", pady=(20, 0))

        # Frame for shits and giggles that holds labels with encouraging messages
        self.encouraging_message_frame = tk.Frame(self.scoreboard_elements_frame, bg="black", width=400, height=250)
        self.encouraging_message_frame.pack(side="top", anchor="e")
        self.encouraging_message_frame.pack_propagate(False)

        proud_img_path = self.resource_path("img\\general\\proud.png")
        self.proud_img = tk.PhotoImage(file=proud_img_path)
        self.proud_label = tk.Label(self.encouraging_message_frame, image=self.proud_img, background="black")
        self.proud_label.pack()

        gj_img_path = self.resource_path("img\\general\\gj.png")
        self.gj_img = tk.PhotoImage(file=gj_img_path)
        self.gj_label = tk.Label(self.encouraging_message_frame, image=self.gj_img, background="black")
        self.gj_label.pack(side="bottom", anchor="w")

        thumb_img_path = self.resource_path("img\\general\\thumb.png")
        self.thumbs_up_img = tk.PhotoImage(file=thumb_img_path)
        self.thumbs_up_label = tk.Label(self.encouraging_message_frame, image=self.thumbs_up_img, background="black")
        self.thumbs_up_label.place(x=250, y=100)

        rank_img_path = self.resource_path("img\\general\\rank.png")
        self.rank_img = tk.PhotoImage(file=rank_img_path)
        self.rank_label = tk.Label(self.scoreboard_elements_frame, image=self.rank_img, background="black")
        self.rank_label.pack(side="bottom", anchor="e")

        # self.start_timer()
        self.window.mainloop()

    # Handles user input to the desired gold entry box to limit the entry value to an integer or
    # the string 'inf' for infinity
    def validate_gold(self, char, entry_value):
        input_i = char.lower() == 'i' and entry_value.lower() == "i"
        input_n = char.lower() == 'n' and entry_value.lower() == "in"
        input_f = char.lower() == 'f' and entry_value.lower() == "inf"
        backspace = char == "" or (char == 'i' and entry_value.lower() == "") or (char == 'n' and entry_value.lower() == "i") or (char == 'f' and entry_value.lower() == "in")
        num = char.isdigit() and 'i' not in entry_value.lower()
        return num or backspace or input_i or input_n or input_f

    def check_gold_state(self):
        if int(self.user_gold) < 2:
            self.button_refresh.config(state="disabled")

    # Handles the hotkey for refreshing the shop
    def refresh_shortcut(self, event=None):
        if self.button_refresh.cget("state") not in "disabled":
            self.refresh()

    # Note: Make sure to unbind all buy binds and then rebind them manually
    def refresh(self):
        self.apm_counter()
        for i in range(5):
            self.shop_units[i].unbind("<Button-1>")
        if self.user_gold != "∞":
            self.user_gold = int(self.user_gold) - 2
            self.check_gold_state()
        self.gold.config(text=f"{self.user_gold}¢")
        self.shop_count += 1
        self.populate_shop()
        self.refresh_sound.play()
        
    # All functions to handle team builder selection and deselection
    def select_unit(self, element):
        for i in range(len(self.teammates)):
            if self.teammates[i].name is None:
                img_path = self.resource_path(self.find_champion(element.name).get_icon_path())
                new_img = tk.PhotoImage(file=img_path)
                self.teammates[i].name = element.name
                self.teammates[i].config(image=new_img)
                self.teammates[i].image = new_img
                self.teammates[i].bind("<Button-1>", lambda event, label=self.teammates[i]: self.deselect_unit(label))

                selected = tk.PhotoImage(file=self.resource_path("img\icons\empty.png"))
                element.config(image=selected)
                element.image = selected
                element.unbind("<Button-1>")

                break
      
    def deselect_unit(self, element):
        for j in range(len(self.champion_images)):
            for k in range(len(self.champion_images[j])):
                if self.champion_images[j][k].name == element.name:
                    img_path = self.resource_path(self.find_champion(element.name).get_icon_path())
                    new_img = tk.PhotoImage(file=img_path)
                    self.champion_images[j][k].config(image=new_img)
                    self.champion_images[j][k].image = new_img
                    self.champion_images[j][k].bind("<Button-1>", lambda event, label=self.champion_images[j][k]: self.select_unit(label))
                    break

        element.name = None
        deselected = tk.PhotoImage(file=self.resource_path("img\icons\empty.png"))
        element.config(image=deselected)
        element.image = deselected
        element.unbind("<Button-1>")

    # Function to help find the unit object associated with a name and returns the icon path
    def find_champion(self, name):
        for i in range(len(self.costs)):
            if name in self.costs[i]:
                return self.costs[i][name]
        return None
    
    # Function to create the team based on the selected champions
    def create_team(self):
        for teammate in self.teammates:
            self.target_team.append(teammate.name)

    # Functions to handle the countdown timer
    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            remaining_time = max(self.user_time - elapsed_time, 0)
            formatted_time = self.format_timer(remaining_time)
            self.timer_label.config(text=formatted_time)

            if remaining_time > 0:
                self.window.after(10, self.update_timer)

            if remaining_time == 0:
                self.to_scoreboard()

    def format_timer(self, seconds):
        nice_seconds = f"{seconds:.2f}"
        return nice_seconds

    # Function to handle buying a unit from the shop
    def buy_unit(self, element):
        if self.user_gold == "∞":
            self.buy_unit_helper(element)
        else:
            cost = self.find_champion(element.name).get_cost()
            if (int(self.user_gold) < int(cost)):
                pass
            else:
                self.user_gold = int(self.user_gold) - int(cost)
                self.gold.config(text=f"{self.user_gold}¢")
                self.bought_units.append(element.name)
                self.check_gold_state()
                self.buy_unit_helper(element)
    
    def buy_unit_helper(self, element):
        self.buy_sound.play()
        self.apm_counter()
        empty_img = tk.PhotoImage(file=self.resource_path("img\general\empty.png"))
        element.config(image=empty_img)
        element.image = empty_img
        element.unbind("<Button-1>")
        element.name = None

    # Function to update game frame based on user inputted values
    def update_game_values(self):
        if(self.gold_entry.get().lower() == 'inf'):
            self.user_gold = "∞"
        else:
            self.user_gold = self.gold_entry.get()
        user_level = self.level_combobox.get()
        self.user_time = float(self.find_time_interval()) + 0.3 # lol

        unit_cost_odds = tft.tft_level_odds[int(user_level)]

        self.level.config(text=f"Level {user_level}")
        self.gold.config(text=f"{self.user_gold}¢")
        self.timer_label.config(text=f"{self.user_time}")

        self.one_cost_odds.config(text=f"{unit_cost_odds[0]}%")
        self.two_cost_odds.config(text=f"{unit_cost_odds[1]}%")
        self.three_cost_odds.config(text=f"{unit_cost_odds[2]}%")
        self.four_cost_odds.config(text=f"{unit_cost_odds[3]}%")
        self.five_cost_odds.config(text=f"{unit_cost_odds[4]}%")

        self.generate_shops(unit_cost_odds)

    # Functions to handle finding the time interval for the game
    def find_time_interval(self):
        return self.time_combobox.get()[self.time_combobox.get().find('(')+1:self.time_combobox.get().find('(')+3]

    def generate_shops(self, odds):
        if self.user_gold == "∞":
            for i in range(1000):
                self.generate_shop(odds)
        else:
            for i in range(int(self.user_gold)//2 + 1):
                self.generate_shop(odds)
    
    def generate_shop(self, odds):
        shop=[]
        for j in range(5):
            roll_cost = random.uniform(0, 1) * 100
            match roll_cost:
                case cost if cost <= odds[0]:
                    shop.append(random.choice(list(self.one_cost)))
                case cost if cost <= odds[0] + odds[1]:
                    shop.append(random.choice(list(self.two_cost)))
                case cost if cost <= odds[0] + odds[1] + odds[2]:
                    shop.append(random.choice(list(self.three_cost)))
                case cost if cost <= odds[0] + odds[1] + odds[2] + odds[3]:
                    shop.append(random.choice(list(self.four_cost)))
                case cost if cost <= odds[0] + odds[1] + odds[2] + odds[3] + odds[4]:
                    shop.append(random.choice(list(self.five_cost)))
        self.shops.append(shop)

    def populate_shop(self):
        for i in range(len(self.shops[self.shop_count])):
            img_path = self.resource_path(self.find_champion(self.shops[self.shop_count][i]).get_img_path())
            new_img = tk.PhotoImage(file=img_path)
            self.shop_units[i].config(image=new_img)
            self.shop_units[i].image = new_img
            self.shop_units[i].name = self.find_champion(self.shops[self.shop_count][i]).get_name()
            self.shop_units[i].bind("<Button-1>", lambda event, label=self.shop_units[i]: self.buy_unit(label))
            self.seen_units.append(self.find_champion(self.shops[self.shop_count][i]).get_name())
    
    # Below are functions to handle units on game load
    def load_units(self):
        file = open('set10.json')
        data = json.load(file)
        for unit in data:
            temp = Unit(data[unit]['name'], data[unit]['cost'], data[unit]['img_path'], data[unit]['icon_path'])
            match data[unit]['cost']:
                case "1":
                    self.one_cost[data[unit]['name']] = temp
                case "2":
                    self.two_cost[data[unit]['name']] = temp
                case "3":
                    self.three_cost[data[unit]['name']] = temp
                case "4":
                    self.four_cost[data[unit]['name']] = temp
                case "5":
                    self.five_cost[data[unit]['name']] = temp

    # Function to ensure that users don't start the game before pressing the start button
    def game_on(self):
        # Sets a hotkey for refreshing the shop
        self.window.bind("<KeyPress-d>", self.refresh_shortcut)
    
    # Function to handle the actions per minute counter
    def apm_counter(self, event=None):
        self.actions += 1

    # Functions to handle the calculation of the user's scores
    def calc_apm(self):
        print(int(self.find_time_interval()))
        print(int(self.find_time_interval()) == 30)
        if (int(self.find_time_interval()) == 30):
            print("30")
            return self.actions * 2
        else:
            print("45")
            return (self.actions * 4/3)
    
    # Function to calculate how many units a user bought that was in their target team, 
    # how many units a user bought that was not in their target team, and how many units
    # a user did not buy that was in their target team.
    # Sets global variable unit_stats to a list of four strings: [Hits, Misses, Rolled Past, and Hit %]
    def calc_unit_stats(self):
        hits = 0
        misses = 0
        rolled_past = 0

        bought_units_dict = self.convert_to_dict(self.bought_units)
        seen_units_dict = self.convert_to_dict(self.seen_units)

        for unit in self.bought_units:
            if unit in self.target_team:
                hits += 1
            else:
                misses += 1
        
        for unit in self.target_team:
            if unit in seen_units_dict and unit in bought_units_dict:
                rolled_past += seen_units_dict[unit] - bought_units_dict[unit]
            elif unit in seen_units_dict and unit not in bought_units_dict:
                rolled_past += seen_units_dict[unit]

        hit_percentage = str(self.calc_hit_percentage(hits, misses)) + " %"
        self.unit_stats = [hits, misses, rolled_past, hit_percentage]
        self.display_scores()
    
    # Function to display the user's scores with pre-existing labels
    def display_scores(self):
        self.actions_label.config(text=f"Actions: {self.actions}")
        self.apm_label.config(text=f"APM: {self.calc_apm()}")
        self.hits_label.config(text=f"Hits: {self.unit_stats[0]}")
        self.misses_label.config(text=f"Misses: {self.unit_stats[1]}")
        self.rolled_past_label.config(text=f"Rolled Past: {self.unit_stats[2]}")
        self.hit_percentage_label.config(text=f"Hit Percentage: {self.unit_stats[3]}")

    # Function to calculate the user's hit percentage
    def calc_hit_percentage(self, hits, misses):
        total = hits + misses
        if total == 0:
            return 0
        else:
            return hits / total * 100

    # Helper function to convert the list of seen and bought units to a dictionary of unit counts
    def convert_to_dict(self, list):
        result_dict = {}
        for item in list:
            if item in result_dict:
                result_dict[item] += 1
            else:
                result_dict[item] = 1
        return result_dict

    # Functions to handle frame switching
    def to_team_planner(self):
        self.update_game_values()
        self.landing_frame.pack_forget()
        self.team_builder_frame.pack(fill=tk.BOTH, expand=True)

    def to_game(self):
        self.create_team()
        self.populate_shop()
        self.start_timer()
        self.game_on()
        self.team_builder_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)

    def to_scoreboard(self):
        self.calc_unit_stats()
        self.game_frame.pack_forget()
        self.scoreboard_frame.pack(fill=tk.BOTH, expand=True)

    # Credit to https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

ThinkFastGUI()
import time
import random
import tkinter as tk
from tkinter import ttk
import tft

class ThinkFastGUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Think Fast Client")
        self.window_icon = tk.PhotoImage(file='img\general\logo.png')
        self.window.iconphoto(True, self.window_icon)
        style=ttk.Style()

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
        self.user_time = None
        self.start_time = None

        # Creates the different frames for the game
        self.landing_frame = tk.Frame(self.window, bg="black")
        self.team_builder_frame = tk.Frame(self.window, bg="white")
        self.game_frame = tk.Frame(self.window, bg="black")
        self.scoreboard_frame = tk.Frame(self.window, bg="black")

        # Loads the landing page for users
        self.team_builder_frame.pack(fill=tk.BOTH, expand=True)

        # Below are the elements of the landing_frame

        # Creates a label to display the background of the landing page
        self.homepage_icon = tk.PhotoImage(file="img\general\cover.png")
        self.homepage = tk.Label(self.landing_frame, image=self.homepage_icon)
        self.homepage.grid(row=0, column=0)

        # Creates user inputs
        self.user_input_frame = tk.Frame(self.landing_frame, bg="lightgray", width = 300, height = 200, highlightbackground="gray", highlightthickness=2)
        self.user_input_frame.place(x=490, y=500)

        self.level_label = tk.Label(self.user_input_frame, text="Select Desired Level:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.level_label.grid(row=0, column=0, padx=(10, 0))

        self.level_combobox = ttk.Combobox(self.user_input_frame, value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], width=22, state="readonly")
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
        self.team_builder_img = tk.PhotoImage(file="img\\general\\team_builder.png")
        self.team_builder_title_img = tk.Label(self.team_builder_frame, image=self.team_builder_img, width=640, height=100, background="white")
        self.team_builder_title_img.pack(anchor="nw")

        # Creates a frame to hold the champion pool for users to select from
        # Contains a scrollable canvas
        self.champion_select_frame = tk.Frame(self.team_builder_frame, width=400, height=500, background="white", highlightbackground="gold2", highlightthickness=2)
        self.champion_select_frame.place(x=100, y=150)

        self.champion_select_canvas = tk.Canvas(self.champion_select_frame, width=400, height=500, background="white", highlightbackground="gold2", highlightthickness=2, scrollregion=(0,0,400,5000))
        self.champion_select_canvas.pack()
        self.champion_select_canvas.create_line(0,0,400,5000, fill="red", width=10)

        champ_select_scrollbar = ttk.Scrollbar(self.champion_select_canvas, orient='vertical', command=self.champion_select_canvas.yview, style="Vertical.TScrollbar")
        self.champion_select_canvas.config(yscrollcommand=champ_select_scrollbar.set)
        # champ_select_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne') # hidden scroll bar
        self.champion_select_canvas.bind('<MouseWheel>', lambda event: self.champion_select_canvas.yview_scroll(-int(event.delta/60), "units"))

        # Create 5 more frames to hold the different costs
        # Then make loops to populate x champion frames into the cost frames, 3 rows, 5 columns
        # Then populate champion images in

        # Creates individual frames for champion icons and nametages and displays them cleanly in the
        # champion select frame created above
        # self.champion_images = []
        # self.champion_names = []

        # for i in range(13):
        #     row = i // 3
        #     column = i % 3

        #     frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        #     frame.grid(row=row, column=column, padx=10, pady=(10, 0) if row == 0 else (0, 10))

        #     champion_image = tk.Label(frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        #     champion_image.pack()

        #     champion_name = tk.Label(frame, text=f"test{i + 1}", background="white", foreground="black")
        #     champion_name.pack()

        #     # Append the created widgets to the arrays
        #     self.champion_images.append(champion_image)
        #     self.champion_names.append(champion_name)

        # Creates a label for clarity in team building
        self.arrow_img = tk.PhotoImage(file="img\\general\\arrow.png")
        self.arrow_img_label = tk.Label(self.team_builder_frame, image=self.arrow_img, background="white")
        self.arrow_img_label.place(x=550, y=260)

        # Creates a frame for housing the user's chosen team
        self.team_select_frame = tk.Frame(self.team_builder_frame, background="black", highlightbackground="gold2", highlightthickness=2)
        self.team_select_frame.place(x=865, y=265)

        # Creates a label for visibility
        self.user_team_img = tk.PhotoImage(file="img\\general\\your_team.png")
        self.user_team = tk.Label(self.team_builder_frame, background="white", image=self.user_team_img)
        self.user_team.place(x=825, y=125)

        # Same as the champion frames but houses the user's selected champions
        self.teammates = []
        for row in range(3):
            for column in range(3):
                teammate_unit = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
                teammate_unit.grid(row=row, column=column, padx=10 if column == 0 else (0, 10), pady=10 if row == 0 else (0, 10))
                self.teammates.append(teammate_unit)

        # Creates a button to continue to the next part of the game
        self.warning_label = tk.Label(self.team_builder_frame, text= "WARNING!! The game starts the moment you press this button. Be ready!", font=("Ariel", 8), background="yellow")
        self.warning_label.place(x=820, y=600)
        self.warning_arrow_img = tk.PhotoImage(file="img\\general\\arrow2.png")
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
        button_level_up_img = tk.PhotoImage(file="img\\general\\buy_xp.png")
        self.button_level_up = tk.Button(self.action_frame, image=button_level_up_img, width=150, height=38, borderwidth=0)
        self.button_level_up.grid(row=0, column=0, padx=5, pady=(3,0))

        # Creates a button for refreshing the shop
        button_refresh_img = tk.PhotoImage(file="img\\general\\refresh.png")
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

        # Sets a hotkey for refreshing the shop
        self.window.bind("<KeyPress-d>", self.refresh_shortcut)

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

    # Handles the hotkey for refreshing the shop
    def refresh_shortcut(self, event=None):
        if self.button_refresh.cget("state") not in "disabled":
            self.refresh()

    # Note: Make sure to unbind all buy binds and then rebind them manually
    def refresh(self, event=None):
        print("refresh")
        self.user_gold -= 2
        self.gold.config(text=f"{self.user_gold}¢")
        self.populate_shop()
        if (self.user_gold < 2):
            self.button_refresh.config(state=tk.DISABLED)

    def populate_shop(self):
        print("populating")

    # All dunctions to handle team builder selection and deselection and population
    def select_unit(self):
        print("selected")

    def deselect_unit(self):
        print("deselected")

    def populate_team_builder(self):
        print("populated")

    # Functions to handle the countdown timer
    def start_timer(self, event=None):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self, event=None):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            remaining_time = max(self.user_time - elapsed_time, 0)
            formatted_time = self.format_timer(remaining_time)
            self.timer_label.config(text=formatted_time)

            if remaining_time > 0:
                self.window.after(10, self.update_timer)

            if remaining_time == 0:
                self.to_scoreboard()

    def format_timer(self, seconds, event=None):
        nice_seconds = f"{seconds:.2f}"
        return nice_seconds

    # Functions to handle frame switching
    def to_team_planner(self, event=None):
        self.update_game_values()
        self.landing_frame.pack_forget()
        self.team_builder_frame.pack(fill=tk.BOTH, expand=True)
        print("To Team Planner")

    def to_game(self, event=None):
        self.populate_shop()
        self.start_timer()
        self.team_builder_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        print("To Game")

    def to_scoreboard(self, event=None):
        self.game_frame.pack_forget()
        self.scoreboard_frame.pack(fill=tk.BOTH, expand=True)
        print("To Scoreboard")

    # Function to handle buying a unit from the shop
    def buy_unit(self, element):
        bought = tk.PhotoImage(file="img\general\empty.png")
        element.config(image=bought)
        element.image = bought
        element.unbind("<Button-1>")
        print("buy unit")

    # Function to update game frame based on user inputted values
    def update_game_values(self):
        if(self.gold_entry.get().lower() == 'inf'):
            user_gold = "∞"
        else:
            user_gold = self.gold_entry.get()
        user_level = self.level_combobox.get()
        self.user_time = float(self.time_combobox.get()[self.time_combobox.get().find('(')+1:self.time_combobox.get().find('(')+3]) + 0.5 # lol

        unit_cost_odds = tft.tft_level_odds[int(user_level)]

        self.level.config(text=f"Level {user_level}")
        self.gold.config(text=f"{user_gold}¢")
        self.timer_label.config(text=f"{self.user_time}")

        self.one_cost_odds.config(text=f"{unit_cost_odds[0]}%")
        self.two_cost_odds.config(text=f"{unit_cost_odds[1]}%")
        self.three_cost_odds.config(text=f"{unit_cost_odds[2]}%")
        self.four_cost_odds.config(text=f"{unit_cost_odds[3]}%")
        self.five_cost_odds.config(text=f"{unit_cost_odds[4]}%")

ThinkFastGUI()
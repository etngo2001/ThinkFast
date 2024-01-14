import time
import tkinter as tk
from tkinter import ttk

class ThinkFastGUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Think Fast Client")
        self.window_icon = tk.PhotoImage(file='img\logo.png')
        self.window.iconphoto(True, self.window_icon)

        # Get the screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Set the window size
        window_width = 1280
        window_height = 720

        # Calculate the X and Y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the window size and position
        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)

        # Initializes variables for storage of user input for user level and gold
        self.user_gold = 61
        self.user_level = 9
        self.user_time = 30.01
        self.start_time = None

        # Creates the different frames for the game
        self.landing_frame = tk.Frame(self.window, bg="black")
        self.team_builder_frame = tk.Frame(self.window, bg="black")
        self.game_frame = tk.Frame(self.window, bg="black")
        self.scoreboard_frame = tk.Frame(self.window, bg="black")

        # Loads the landing page for users
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        # Below are the elements of the landing_frame

        # Creates a label to display the background of the landing page
        self.homepage_icon = tk.PhotoImage(file="img\cover.png")
        self.homepage = tk.Label(self.landing_frame, image=self.homepage_icon)
        self.homepage.grid(row=0, column=0)

        # Creates user inputs
        self.user_input_frame = tk.Frame(self.landing_frame, bg="lightgray", width = 300, height = 200, highlightbackground="gray", highlightthickness=2)
        self.user_input_frame.place(x=490, y=500)

        self.level_label = tk.Label(self.user_input_frame, text="Select Desired Level:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.level_label.grid(row=0, column=0, padx=(10, 0))

        self.level_combobox = ttk.Combobox(self.user_input_frame, value=[1,2,3,4,5,6,7,8,9,10], width=22)
        self.level_combobox.grid(row=0, column=1, sticky="w", padx=(0,10))

        self.gold_label = tk.Label(self.user_input_frame, text="Enter Desired Gold:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.gold_label.grid(row=1, column=0, padx=(10, 0))

        self.gold_entry = tk.Entry(self.user_input_frame, width=25)
        self.gold_entry.grid(row=1, column=1, sticky="w", padx=(0,10))

        self.time_label = tk.Label(self.user_input_frame, text="Select Time Interval:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        self.time_label.grid(row=2, column=0, padx=(10, 0))

        self.time_combobox = ttk.Combobox(self.user_input_frame, values=["Normal Rounds (30 sec)", "Augment Round (45 sec)"], width=22)
        self.time_combobox.grid(row=2, column=1, sticky="w", padx=(0,10))

        # Creates a button to continue to the next part of the game
        self.to_team_planner_button = tk.Button(self.landing_frame, text="Next", command=self.to_team_planner, width=10, height=2)
        self.to_team_planner_button.place(x=580, y=640)

        # Below are the elements of the team_builder_frame

        # Below are the elements of the game_frame

        # Creates the frame for the timer and initializes the timer
        self.timer_frame = tk.Frame(self.game_frame)
        self.timer_frame.pack(side="top")

        self.timer_label = tk.Label(self.timer_frame, text=f"{self.user_time}", bg="black", fg="red", font=("Ariel", 30))
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
        self.button_level_up = tk.Button(self.action_frame, text="Level Up (4¢)", width=20, height=2)
        self.button_level_up.grid(row=0, column=0, padx=5, pady=(3,0))

        # Creates a button for refreshing the shop
        self.button_refresh = tk.Button(self.action_frame, text="Refresh (2¢)", command=self.refresh, width=20, height=2)
        self.button_refresh.grid(row=1, column=0, padx=5, pady=3)

        # Creates and displays the units in the shop
        self.unit_1_img = tk.PhotoImage(file="img\\common.png")
        self.unit_1 = tk.Label(self.shop_frame, image=self.unit_1_img, bg="darkgreen")
        self.unit_1.grid(row=0, column=1, padx=3)
        self.unit_1.bind("<Button-1>", lambda event: self.buy_unit(self.unit_1))

        self.unit_2_img = tk.PhotoImage(file="img\\uncommon.png")
        self.unit_2 = tk.Label(self.shop_frame, image=self.unit_2_img, bg="darkgreen")
        self.unit_2.grid(row=0, column=2, padx=3)
        self.unit_2.bind("<Button-1>", lambda event: self.buy_unit(self.unit_2))

        self.unit_3_img = tk.PhotoImage(file="img\\rare.png")
        self.unit_3 = tk.Label(self.shop_frame, image=self.unit_3_img, bg="darkgreen")
        self.unit_3.grid(row=0, column=3, padx=3)
        self.unit_3.bind("<Button-1>", lambda event: self.buy_unit(self.unit_3))

        self.unit_4_img = tk.PhotoImage(file="img\\epic.png")
        self.unit_4 = tk.Label(self.shop_frame, image=self.unit_4_img, bg="darkgreen")
        self.unit_4.grid(row=0, column=4, padx=3)
        self.unit_4.bind("<Button-1>", lambda event: self.buy_unit(self.unit_4))

        self.unit_5_img = tk.PhotoImage(file="img\\legendary.png")
        self.unit_5 = tk.Label(self.shop_frame, image=self.unit_5_img, bg="darkgreen")
        self.unit_5.grid(row=0, column=5, padx=3)
        self.unit_5.bind("<Button-1>", lambda event: self.buy_unit(self.unit_5))

        # Creates a label for displaying player's desired gold and level and unit odds
        self.level = tk.Label(self.level_frame, text=f"Level {self.user_level}", font=("Ariel", 16), padx=5)
        self.level.pack()
        self.gold = tk.Label(self.gold_frame, text=f"{self.user_gold}¢", font=("Ariel", 16), padx=5)
        self.gold.pack()
        self.unit_odds = tk.Label(self.unit_odds_frame, text="5%, 10%, 20%, 40%, 25%", font=("Ariel", 8))
        self.unit_odds.pack()

        # Below are the elements of the scoreboard_frame

        # Sets a hotkey for refreshing the shop
        self.window.bind("<KeyPress-d>", self.refresh_shortcut)

        # self.start_timer()
        self.window.mainloop()

    # Handles the hotkey for refreshing the shop
    def refresh_shortcut(self, event=None):
        if self.button_refresh.cget("state") not in "disabled":
            self.refresh()

    def refresh(self, event=None):
        print("refresh")
        self.user_gold -= 2
        self.gold.config(text=f"{self.user_gold}¢")
        if (self.user_gold < 2):
            self.button_refresh.config(state=tk.DISABLED)

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
        self.landing_frame.pack_forget()
        self.team_builder_frame.pack(fill=tk.BOTH, expand=True)
        print("To Team Planner")

    def to_game(self, event=None):
        self.team_builder_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        print("To Game")

    def to_scoreboard(self, event=None):
        self.game_frame.pack_forget()
        self.scoreboard_frame.pack(fill=tk.BOTH, expand=True)
        print("To Scoreboard")

    # Function to handle buying a unit from the shop
    def buy_unit(self, element):
        bought = tk.PhotoImage(file="img\empty.png")
        element.config(image=bought)
        element.image = bought
        print("buy unit")

ThinkFastGUI()
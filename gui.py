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

        # Creates the different frames for the game
        landing_frame = tk.Frame(self.window, bg="black")
        team_builder_frame = tk.Frame(self.window, bg="black")
        game_frame = tk.Frame(self.window, bg="black")
        scoreboard_frame = tk.Frame(self.window, bg="black")

        game_frame.pack(fill=tk.BOTH, expand=True)

        # Below are the elements of the landing_frame

        # Creates a label to display the background of the landing page
        self.homepage_icon = tk.PhotoImage(file="img\cover.png")
        self.homepage = tk.Label(landing_frame, image=self.homepage_icon)
        self.homepage.grid(row=0, column=0)

        # Creates user inputs
        self.user_input_frame = tk.Frame(landing_frame, bg="lightgray", width = 300, height = 200, highlightbackground="gray", highlightthickness=2)
        self.user_input_frame.place(x=490, y=500)

        level_label = tk.Label(self.user_input_frame, text="Select Desired Level:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        level_label.grid(row=0, column=0, padx=(10, 0))

        level_combobox = ttk.Combobox(self.user_input_frame, value=[1,2,3,4,5,6,7,8,9,10], width=22)
        level_combobox.grid(row=0, column=1, sticky="w", padx=(0,10))

        gold_label = tk.Label(self.user_input_frame, text="Enter Desired Gold:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        gold_label.grid(row=1, column=0, padx=(10, 0))

        gold_entry = tk.Entry(self.user_input_frame, width=25)
        gold_entry.grid(row=1, column=1, sticky="w", padx=(0,10))

        time_label = tk.Label(self.user_input_frame, text="Select Time Interval:", bg="lightgray", pady=10, width=15, anchor=tk.E)
        time_label.grid(row=2, column=0, padx=(10, 0))

        time_combobox = ttk.Combobox(self.user_input_frame, values=["Normal Rounds (30 sec)", "Augment Round (45 sec)"], width=22)
        time_combobox.grid(row=2, column=1, sticky="w", padx=(0,10))

        # Below are the elements of the team_builder_frame

        # Below are the elements of the game_frame

        # Creates the frame for the timer and initializes the timer
        timer_frame = tk.Frame(game_frame)
        timer_frame.pack(side="top")

        timer_label = tk.Label(timer_frame, text=f"{self.user_time}", bg="black", fg="red", font=("Ariel", 30))
        timer_label.pack()

        # Creates the frame for the shop
        shop_frame = tk.Frame(game_frame, bg="darkgreen", padx=10, pady=10)
        shop_frame.pack(side="bottom")

        # Creates a frame for action buttons
        action_frame = tk.Frame(shop_frame, bg="darkgreen")
        action_frame.grid(row=0, column=0)

        # Creates a frame for displaying user's level, gold, and unit odds
        level_frame = tk.Frame(game_frame, highlightbackground="darkgreen", highlightthickness=5)
        level_frame.place(in_=shop_frame, x=-10, y=-40)

        gold_frame = tk.Frame(game_frame, highlightbackground="darkgreen", highlightthickness=5)
        gold_frame.place(in_=shop_frame, relx=0.5, x=-10, y=-40)

        unit_odds_frame = tk.Frame(game_frame, width=300, height=15, highlightbackground="darkgreen", highlightthickness=5)
        unit_odds_frame.place(in_=level_frame, relx=1.0, rely=0.17)

        # Creates a button for spending gold to level up
        # This button will be clickable but has no function for this version of the game
        # Clicking this button will do nothing
        self.button_level_up = tk.Button(action_frame, text="Level Up (4¢)", width=20, height=2)
        self.button_level_up.grid(row=0, column=0, padx=5, pady=(3,0))

        # Creates a button for refreshing the shop
        self.button_refresh = tk.Button(action_frame, text="Refresh (2¢)", command=self.refresh, width=20, height=2)
        self.button_refresh.grid(row=1, column=0, padx=5, pady=3)

        # Creates and displays the units in the shop
        self.unit_1 = tk.Button(shop_frame, text="Unit 1", command=self.buyUnit, width=20, height=5)
        self.unit_1.grid(row=0, column=1, padx=3)

        self.unit_2 = tk.Button(shop_frame, text="Unit 2", command=self.buyUnit, width=20, height=5)
        self.unit_2.grid(row=0, column=2, padx=3)

        self.unit_3 = tk.Button(shop_frame, text="Unit 3", command=self.buyUnit, width=20, height=5)
        self.unit_3.grid(row=0, column=3, padx=3)

        self.unit_4 = tk.Button(shop_frame, text="Unit 4", command=self.buyUnit, width=20, height=5)
        self.unit_4.grid(row=0, column=4, padx=3)

        self.unit_5 = tk.Button(shop_frame, text="Unit 5", command=self.buyUnit, width=20, height=5)
        self.unit_5.grid(row=0, column=5, padx=3)

        # Creates a label for displaying player's desired gold and level and unit odds
        self.level = tk.Label(level_frame, text=f"Level {self.user_level}", font=("Ariel", 16), padx=5)
        self.level.pack()
        self.gold = tk.Label(gold_frame, text=f"{self.user_gold}¢", font=("Ariel", 16), padx=5)
        self.gold.pack()
        self.unit_odds = tk.Label(unit_odds_frame, text="5%, 10%, 20%, 40%, 25%", font=("Ariel", 8))
        self.unit_odds.pack()

        # Below are the elements of the scoreboard_frame

        # Sets a hotkey for refreshing the shop
        self.window.bind("<KeyPress-d>", self.refreshShortcut)

        self.window.mainloop()

    # Handles the hotkey for refreshing the shop
    def refreshShortcut(self, event=None):
        if self.button_refresh.cget("state") not in "disabled":
            self.refresh()

    def refresh(self, event=None):
        print("refresh")
        self.user_gold -= 2
        self.gold.config(text=f"{self.user_gold}¢")
        if (self.user_gold < 2):
            self.button_refresh.config(state=tk.DISABLED)

    def buyUnit(self):
        print("buy unit")

ThinkFastGUI()
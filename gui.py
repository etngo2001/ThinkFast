import tkinter as tk

class ThinkFastGUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Think Fast Client")
        self.window_icon = tk.PhotoImage(file='logo.png')
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

        # Creates the different frames for the game
        landing_frame = tk.Frame(self.window, bg="black")
        team_builder_frame = tk.Frame(self.window, bg="yellow")
        game_frame = tk.Frame(self.window, bg="purple")
        scoreboard_frame = tk.Frame(self.window, bg="green")

        game_frame.pack(fill=tk.BOTH, expand=True)

        # Creates the frame for the shop
        shop_frame = tk.Frame(game_frame, bg="red", padx=10, pady=10)
        shop_frame.pack(side="bottom")

        # Creates a frame for action buttons
        action_frame = tk.Frame(shop_frame, bg="blue")
        action_frame.grid(row=0, column=0)

        # Creates a frame for displaying user's level, gold, and unit odds
        level_frame = tk.Frame(game_frame, bg="yellow")
        level_frame.place(in_=shop_frame, x=-10, y=-40)

        gold_frame = tk.Frame(game_frame, bg="yellow")
        gold_frame.place(in_=shop_frame, relx=0.5, x=-10, y=-40)

        unit_odds_frame = tk.Frame(game_frame, bg="blue", width=300, height=15)
        unit_odds_frame.place(in_=level_frame, relx=1.0, rely=0.33)

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
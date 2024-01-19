import time
import random
import tkinter as tk
from tkinter import ttk
import tft

class ThinkFastGUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Think Fast Client")
        self.window_icon = tk.PhotoImage(file='img\logo.png')
        self.window.iconphoto(True, self.window_icon)

        # Set the window size
        window_width = 1280
        window_height = 720

        # Calculate the X and Y coordinates to center the window
        x_coordinate = (self.window.winfo_screenwidth() - window_width) // 2
        y_coordinate = (self.window.winfo_screenheight() - window_height) // 2

        # Set the window size and position
        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)

        # Initializes variables for storage of user input for user level and gold
        self.user_gold = None
        self.user_level = None
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
        self.homepage_icon = tk.PhotoImage(file="img\cover.png")
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

        self.gold_entry = tk.Entry(self.user_input_frame, width=25)
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
        self.team_builder_img = tk.PhotoImage(file="img\\team_builder.png")
        self.team_builder_title_img = tk.Label(self.team_builder_frame, image=self.team_builder_img, width=640, height=100, background="white")
        self.team_builder_title_img.pack(anchor="nw")

        # Creates a combobox for users to easily change through the different menus of units
        # sorted by their costs
        self.unit_selection = ttk.Combobox(self.team_builder_frame, values=["1-costs", "2-costs", "3-costs", "4-costs", "5-costs"], state="readonly")
        self.unit_selection.place(x=275 , y=150)
        self.unit_selection.bind("<<ComboboxSelected>>", self.display_units)

        # Labels and images for visibility purposes to help users see the combobox
        # Also just me messing around
        yellow_arrow1 = tk.PhotoImage(file="img\\yellow_arrow.png")
        yellow_arrow2 = tk.PhotoImage(file="img\\yellow_arrow2.png")
        yellow_arrow3 = tk.PhotoImage(file="img\\yellow_arrow3.png")
        yellow_arrow4 = tk.PhotoImage(file="img\\yellow_arrow4.png")
        self.visibility_label = tk.Label(self.team_builder_frame, text="SELECT HERE!!", background="white", font=("Ariel", 8))
        self.yellow_arrow1_img = tk.Label(self.team_builder_frame, background="white", image=yellow_arrow1)
        self.yellow_arrow2_img = tk.Label(self.team_builder_frame, background="white", image=yellow_arrow2)
        self.yellow_arrow3_img = tk.Label(self.team_builder_frame, background="white", image=yellow_arrow3)
        self.yellow_arrow4_img = tk.Label(self.team_builder_frame, background="white", image=yellow_arrow4)
        self.visibility_label.place(x=275, y=120)
        self.yellow_arrow1_img.place(x=350, y=100)
        self.yellow_arrow2_img.place(x=420, y=160)
        self.yellow_arrow3_img.place(x=220, y=150)
        self.yellow_arrow4_img.place(x=220, y=120)

        # Creates a frame to hold the champion pool for users to select from
        self.champion_select_frame = tk.Frame(self.team_builder_frame, width=640, height=720, background="white", highlightbackground="gold2", highlightthickness=2)
        self.champion_select_frame.place(x=225, y=200)

        # Creates individual frames for champion icons and nametages and displays them cleanly in the
        # champion select frame created above
        self.champion_1_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_1 = tk.Label(self.champion_1_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_1_name = tk.Label(self.champion_1_frame, text="test1", background="white", foreground="black")
        self.champion_1.pack()
        self.champion_1_name.pack()
        self.champion_1_frame.grid(row=0, column=0, padx=10, pady=10)

        self.champion_2_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_2 = tk.Label(self.champion_2_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_2_name = tk.Label(self.champion_2_frame, text="test2", background="white", foreground="black")
        self.champion_2.pack()
        self.champion_2_name.pack()
        self.champion_2_frame.grid(row=0, column=1, padx=10, pady=10)

        self.champion_3_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_3 = tk.Label(self.champion_3_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_3_name = tk.Label(self.champion_3_frame, text="test3", background="white", foreground="black")
        self.champion_3.pack()
        self.champion_3_name.pack()
        self.champion_3_frame.grid(row=0, column=2, padx=10, pady=10)

        self.champion_4_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_4 = tk.Label(self.champion_4_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_4_name = tk.Label(self.champion_4_frame, text="test4", background="white", foreground="black")
        self.champion_4.pack()
        self.champion_4_name.pack()
        self.champion_4_frame.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.champion_5_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_5 = tk.Label(self.champion_5_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_5_name = tk.Label(self.champion_5_frame, text="test5", background="white", foreground="black")
        self.champion_5.pack()
        self.champion_5_name.pack()
        self.champion_5_frame.grid(row=1, column=1, padx=10, pady=(0, 10))

        self.champion_6_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_6 = tk.Label(self.champion_6_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_6_name = tk.Label(self.champion_6_frame, text="test6", background="white", foreground="black")
        self.champion_6.pack()
        self.champion_6_name.pack()
        self.champion_6_frame.grid(row=1, column=2, padx=10, pady=(0,10))

        self.champion_7_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_7 = tk.Label(self.champion_7_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_7_name = tk.Label(self.champion_7_frame, text="test7", background="white", foreground="black")
        self.champion_7.pack()
        self.champion_7_name.pack()
        self.champion_7_frame.grid(row=2, column=0, padx=10, pady=(0, 10))

        self.champion_8_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_8 = tk.Label(self.champion_8_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_8_name = tk.Label(self.champion_8_frame, text="test8", background="white", foreground="black")
        self.champion_8.pack()
        self.champion_8_name.pack()
        self.champion_8_frame.grid(row=2, column=1, padx=10, pady=(0, 10))

        self.champion_9_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_9 = tk.Label(self.champion_9_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_9_name = tk.Label(self.champion_9_frame, text="test9", background="white", foreground="black")
        self.champion_9.pack()
        self.champion_9_name.pack()
        self.champion_9_frame.grid(row=2, column=2, padx=10, pady=(0, 10))

        self.champion_10_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_10 = tk.Label(self.champion_10_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_10_name = tk.Label(self.champion_10_frame, text="test10", background="white", foreground="black")
        self.champion_10.pack()
        self.champion_10_name.pack()
        self.champion_10_frame.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.champion_11_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_11 = tk.Label(self.champion_11_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_11_name = tk.Label(self.champion_11_frame, text="test11", background="white", foreground="black")
        self.champion_11.pack()
        self.champion_11_name.pack()
        self.champion_11_frame.grid(row=3, column=1, padx=10, pady=(0, 10))

        self.champion_12_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_12 = tk.Label(self.champion_12_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_12_name = tk.Label(self.champion_12_frame, text="test12", background="white", foreground="black")
        self.champion_12.pack()
        self.champion_12_name.pack()
        self.champion_12_frame.grid(row=3, column=2, padx=10, pady=(0, 10))

        self.champion_13_frame = tk.Frame(self.champion_select_frame, width=50, height=60, background="white")
        self.champion_13 = tk.Label(self.champion_13_frame, image=tk.PhotoImage(), width=50, height=50, background="white", highlightbackground="black", highlightthickness=3)
        self.champion_13_name = tk.Label(self.champion_13_frame, text="test13")
        self.champion_13.pack()
        self.champion_13_name.pack()
        self.champion_13_frame.grid(row=4, column=0, pady=(0, 10))

        # Creates a label for clarity in team building
        self.arrow_img = tk.PhotoImage(file="img\\arrow.png")
        self.arrow_img_label = tk.Label(self.team_builder_frame, image=self.arrow_img, background="white")
        self.arrow_img_label.place(x=550, y=260)

        # Creates a frame for housing the user's chosen team
        self.team_select_frame = tk.Frame(self.team_builder_frame, background="black", highlightbackground="gold2", highlightthickness=2)
        self.team_select_frame.place(x=865, y=265)

        # Creates a label for visibility
        self.user_team_img = tk.PhotoImage(file="img\\your_team.png")
        self.user_team = tk.Label(self.team_builder_frame, background="white", image=self.user_team_img)
        self.user_team.place(x=825, y=125)

        # Same as the champion frames but houses the user's selected champions
        self.teammate_1 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_1.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        self.teammate_2 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_2.grid(row=0, column=1, pady=(10, 0))
        self.teammate_3 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_3.grid(row=0, column=2, padx=(0, 10), pady=(10,0))
        self.teammate_4 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_4.grid(row=1, column=0, padx=(10, 0), pady=10)
        self.teammate_5 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_5.grid(row=1, column=1, pady=10, padx=10)
        self.teammate_6 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_6.grid(row=1, column=2, padx=(0, 10), pady=10)
        self.teammate_7 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_7.grid(row=2, column=0, padx=(10, 0), pady=(0, 10))
        self.teammate_8 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_8.grid(row=2, column=1, padx=10, pady=(0, 10))
        self.teammate_9 = tk.Label(self.team_select_frame, image=tk.PhotoImage(), width=50, height=50, background="white")
        self.teammate_9.grid(row=2, column=2, padx=(0, 10), pady=(0, 10))

        # Creates a button to continue to the next part of the game
        self.warning_label = tk.Label(self.team_builder_frame, text= "WARNING!! The game starts the moment you press this button. Be ready!", font=("Ariel", 8), background="yellow")
        self.warning_label.place(x=820, y=600)
        self.warning_arrow_img = tk.PhotoImage(file="img\\arrow2.png")
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

        # Creates a label for displaying player's desired gold and level
        self.level = tk.Label(self.level_frame, font=("Ariel", 16), padx=5)
        self.level.pack()
        self.gold = tk.Label(self.gold_frame, font=("Ariel", 16), padx=5)
        self.gold.pack()

        # Handles processing and labelling unit odds based on user's chosen level
        self.one_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="dimgray")
        self.one_cost_odds.grid(row=0, column=0)
        self.two_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="green")
        self.two_cost_odds.grid(row=0, column=1)
        self.three_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="darkblue")
        self.three_cost_odds.grid(row=0, column=2)
        self.four_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="purple")
        self.four_cost_odds.grid(row=0, column=3)
        self.five_cost_odds = tk.Label(self.unit_odds_frame, font=("Ariel", 8), foreground="orange")
        self.five_cost_odds.grid(row=0, column=4)

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

    # Funtion to display units in the team builder
    def display_units(self, event):
        print(f"displaying {event.widget.get()}")

    # Functions to handle frame switching
    def to_team_planner(self, event=None):
        self.update_game_values()
        self.landing_frame.pack_forget()
        self.team_builder_frame.pack(fill=tk.BOTH, expand=True)
        print("To Team Planner")

    def to_game(self, event=None):
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
        bought = tk.PhotoImage(file="img\empty.png")
        element.config(image=bought)
        element.image = bought
        print("buy unit")

    # Function to update game frame based on user inputted values
    def update_game_values(self):
        self.user_gold = int(self.gold_entry.get())
        self.user_level = self.level_combobox.get()
        self.user_time = float(self.time_combobox.get()[self.time_combobox.get().find('(')+1:self.time_combobox.get().find('(')+3]) + 0.5 # lol

        unit_cost_odds = tft.tft_level_odds[int(self.user_level)]

        self.level.config(text=f"Level {self.user_level}")
        self.gold.config(text=f"{self.user_gold}¢")
        self.timer_label.config(text=f"{self.user_time}")

        self.one_cost_odds.config(text=f"{unit_cost_odds[0]}%")
        self.two_cost_odds.config(text=f"{unit_cost_odds[1]}%")
        self.three_cost_odds.config(text=f"{unit_cost_odds[2]}%")
        self.four_cost_odds.config(text=f"{unit_cost_odds[3]}%")
        self.five_cost_odds.config(text=f"{unit_cost_odds[4]}%")


ThinkFastGUI()
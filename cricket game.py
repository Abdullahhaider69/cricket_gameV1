import random

# Define player attributes (batting average, bowling average, fielding)
players_attributes = {
    "User Player 1": {"bat_avg": 50, "bowl_avg": 30},
    "User Player 2": {"bat_avg": 45, "bowl_avg": 28},
    "User Player 3": {"bat_avg": 40, "bowl_avg": 32},
    "User Player 4": {"bat_avg": 38, "bowl_avg": 34},
    "User Player 5": {"bat_avg": 35, "bowl_avg": 36},
    "Computer Player 1": {"bat_avg": 48, "bowl_avg": 29},
    "Computer Player 2": {"bat_avg": 42, "bowl_avg": 31},
    "Computer Player 3": {"bat_avg": 40, "bowl_avg": 35},
    "Computer Player 4": {"bat_avg": 37, "bowl_avg": 33},
    "Computer Player 5": {"bat_avg": 33, "bowl_avg": 37}
}

# Batting cards
batting_cards = [
    "Single | 1", "Double | 2", "Triple | 3", "Gone Gone FOOUR | 4",
    "Dot-Ball | 0", "Long Long SIXX | 6", "No-Ball Free Hit | 1",   
    "Wide ball | 1", "Run out | 1", "Catch out | 0", "Wicket out | 0",
    "Hit-Wicket out | 0", "L.B.W out | 0", "Dot Ball | 0", "Dot Ball | 0"
]

# Expanded bowling options
bowling_cards = [
    "Yorker | 0", "Bouncer | 0", "Good Length | 0", "Full Toss | 0", 
    "Inswing | 0", "Outswing | 0", "Slow Ball | 0", "Short Ball | 0"
]

# Match formats with reduced overs
match_formats = {
    "Test": 15,  # Reduced from 90 overs per day to 15
    "ODI": 10,   # Reduced from 50 overs per innings to 10
    "T20": 5     # Reduced from 20 overs per innings to 5
}

def display_commentary(description, runs, wickets, team_name):
    """Display simple commentary based on game events."""
    commentary_phrases = [
        "What a shot!", "Brilliant delivery!", "That's a crucial wicket!",
        "Spectacular fielding!", "What a finish!", "A big hit!"
    ]
    print(f"{team_name}: {description} - {random.choice(commentary_phrases)}")
    print(f"Current Score: {runs}/{wickets}")

def get_match_format():
    """Let the user choose the match format."""
    print("\nChoose the match format:")
    for format_name in match_formats.keys():
        print(f"- {format_name}")
    
    while True:
        match_choice = input("Enter format (Test, ODI, T20): ").strip().title()
        if match_choice in match_formats:
            return match_choice
        else:
            print("Invalid format. Please choose Test, ODI, or T20.")

def play_innings(team_name, players, match_format, target=None, is_user_bowling=False):
    """Play a single innings with batting, bowling, and target conditions."""
    overs_limit = match_formats[match_format]
    runs, wickets, free_hit, balls_faced, current_player_index = 0, 0, False, 0, 0

    print(f"\n{team_name}'s innings begins in {match_format} format!\n")

    while wickets < 5 and balls_faced < overs_limit * 6:
        random.shuffle(batting_cards)

        # User bowling or batting decision
        if is_user_bowling:
            try:
                print("\nChoose your bowling action:")
                for i, option in enumerate(bowling_cards, 1):
                    print(f"{i}: {option.split('|')[0].strip()}")
                
                bowling_choice = int(input("Enter a number between 1 and 8 for your bowling action: ")) - 1
                if not 0 <= bowling_choice < len(bowling_cards):
                    print("Invalid choice. Please select a number between 1 and 8.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            
            # Random batting outcome for computer
            index = random.randint(0, len(batting_cards) - 1)
        else:
            if team_name == "Computer":
                index = random.randint(0, len(batting_cards) - 1)
            else:
                try:
                    index = int(input("Enter a number between 1 and 15: ")) - 1
                    if not 0 <= index < len(batting_cards):
                        print("Invalid number. Please enter a number between 1 and 15.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
        
        description, value = batting_cards[index].split("|")
        value = int(value.strip())
        description = description.strip()

        # Free Hit Handling
        if "No-Ball" in description:
            print(f"{team_name}: No-Ball! Free hit awarded.")
            free_hit = True
            runs += 1
            continue
        
        if free_hit:
            print(f"{team_name}: Free Hit!")
            if "out" in description and "Run out" not in description:
                print("Cannot be out on Free Hit.")
            else:
                runs += value
            free_hit = False
            continue
        
        # Handling Runs, Wickets, and Commentary
        if "out" not in description:
            runs += value
        else:
            wickets += 1
            print(f"{players[current_player_index]} is out!")
            current_player_index += 1
            if current_player_index < len(players):
                print(f"{players[current_player_index]} comes in to bat.")
        
        balls_faced += 1
        display_commentary(description, runs, wickets, team_name)

        if balls_faced % 6 == 0:
            print(f"End of over {balls_faced // 6}.")

        # Check if target is chased
        if target and runs >= target:
            print(f"{team_name} chased down the target! Total: {runs}/{wickets}")
            return runs
    
    # Final innings result
    print(f"{team_name}: Innings Over. Final Score: {runs}/{wickets} ({balls_faced} balls faced)\n")
    return runs

def toss():
    """Simulate the toss."""
    print("\nTime for the toss!")
    user_call = input("Call the toss (Heads or Tails): ").strip().lower()
    toss_result = random.choice(["heads", "tails"])

    print(f"The coin shows: {toss_result.capitalize()}")

    if user_call == toss_result:
        print("You won the toss!")
        user_choice = input("Do you want to bat or bowl first? (bat/bowl): ").strip().lower()
        return "user", user_choice
    else:
        print("Computer won the toss!")
        computer_choice = random.choice(["bat", "bowl"])
        return "computer", computer_choice

def game():
    """Main game logic."""
    user_team_name = input("Enter your team name: ")
    user_players = [input(f"Enter name for Player {i + 1}: ") for i in range(5)]
    computer_team_name = "Computer Team"
    computer_players = [f"Computer Player {i + 1}" for i in range(5)]

    match_format = get_match_format()

    toss_winner, choice = toss()

    if toss_winner == "user" and choice == "bowl" or toss_winner == "computer" and choice == "bat":
        computer_total = play_innings(computer_team_name, computer_players, match_format, is_user_bowling=True)
        target = computer_total + 1
        user_total = play_innings(user_team_name, user_players, match_format, target)
    else:
        user_total = play_innings(user_team_name, user_players, match_format)
        target = user_total + 1
        computer_total = play_innings(computer_team_name, computer_players, match_format, target, is_user_bowling=True)

    # Decide the winner
    if user_total > computer_total:
        print(f"{user_team_name} wins by {user_total - computer_total} runs!")
    else:
        print(f"{computer_team_name} wins by {computer_total - user_total} runs!")

# Main loop
if __name__ == "__main__":
    while True:
        play_game = input("Do you want to play the game? (yes/no): ").strip().lower()

        if play_game == "yes":
            game()
        else:
            print("Thank you for playing! Goodbye!")
            break

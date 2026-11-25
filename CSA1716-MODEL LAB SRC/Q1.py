def vacuum_cleaner(initial_location, room_status):
    status = room_status.copy()
    location = initial_location
    cost = 0

    print(f"\n--- Test Case: Start in {location} Room ---")
    print(f"Initial State: Location = {location}, Status = {status}")

    while status["Left"] == "Dirty" or status["Right"] == "Dirty":
        if status[location] == "Dirty":
            print(f"Action: Suck dirt in {location} room")
            status[location] = "Clean"
            cost += 1
        else:
            if location == "Left":
                print("Action: Move Right (Left -> Right)")
                location = "Right"
            else:
                print("Action: Move Left (Right -> Left)")
                location = "Left"
            cost += 1

    print(f"Final State:   Location = {location}, Status = {status}")
    print(f"Total Performance Cost: {cost}")

# Test Case 1: Both rooms dirty, starts in Left room
vacuum_cleaner("Left", {"Left": "Dirty", "Right": "Dirty"})

# Test Case 2: Both rooms dirty, starts in Right room
vacuum_cleaner("Right", {"Left": "Dirty", "Right": "Dirty"})

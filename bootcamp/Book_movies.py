# Movie Ticket Booking System

movies = [
    {"id": 1, "title": "Spiderman", "time": "10:00 AM", "price": 200, "booked": [], "revenue": 0.0},
    {"id": 2, "title": "Avengers : Doomsday", "time": "02:00 PM", "price": 250, "booked": [], "revenue": 0.0},
    {"id": 3, "title": "Dune part-3", "time": "06:00 PM", "price": 300, "booked": [], "revenue": 0.0}
]

MAX_SEATS = 10
is_weekend = False

def get_movie(m_id):
    for m in movies:
        if m["id"] == m_id:
            return m
    return None

def display_movies():
    print("\n--- AVAILABLE MOVIES & SHOWTIMES ---")
    for m in movies:
        avail = MAX_SEATS - len(m["booked"])
        print(f"[{m['id']}] {m['title']} | Time: {m['time']} | Base: Rs. {m['price']} | Seats Left: {avail}/{MAX_SEATS}")

def calculate_price(movie, count):
    ticket_price = movie["price"]
    if is_weekend:
        ticket_price += 50
    
    total = ticket_price * count
    if count > 5:
        total *= 0.90  # 10% discount for more than 5 tickets
    return total

def book_tickets():
    display_movies()
    try:
        m_id = int(input("\nEnter Movie ID to book: "))
        movie = get_movie(m_id)
        if not movie:
            print("Error: Invalid Movie ID!")
            return

        print(f"Currently Booked Seats: {movie['booked']}")
        seat_input = input(f"Enter seat numbers (1-{MAX_SEATS}) separated by commas: ")
        
        # Convert to a set to remove duplicate entries from user input
        requested_set = set([int(s.strip()) for s in seat_input.split(",") if s.strip().isdigit()])
        requested = list(requested_set)

        if not requested:
            print("Error: No valid seats specified!")
            return

        for seat in requested:
            if seat < 1 or seat > MAX_SEATS:
                print(f"Error: Seat {seat} is invalid! Must be between 1 and {MAX_SEATS}.")
                return
            if seat in movie["booked"]:
                print(f"Error: Seat {seat} is already booked!")
                return

        movie["booked"].extend(requested)
        total_cost = calculate_price(movie, len(requested))
        movie["revenue"] += total_cost
        
        print(f"Success: Booking Successful! Seats {requested} reserved for '{movie['title']}'.")
        print(f"Total Amount Payable: Rs. {total_cost:.2f}")

    except ValueError:
        print("Error: Invalid input format! Please use numbers.")

def cancel_tickets():
    display_movies()
    try:
        m_id = int(input("\nEnter Movie ID to cancel: "))
        movie = get_movie(m_id)
        if not movie or not movie["booked"]:
            print("Error: Invalid ID or no seats booked for this show.")
            return

        print(f"Booked Seats: {movie['booked']}")
        seat_input = input("Enter seat numbers to cancel (separated by commas): ")
        
        # Convert to a set to remove duplicate entries from user input
        cancel_set = set([int(s.strip()) for s in seat_input.split(",") if s.strip().isdigit()])
        to_cancel = list(cancel_set)

        for seat in to_cancel:
            if seat not in movie["booked"]:
                print(f"Error: Seat {seat} is not currently booked!")
                return

        for seat in to_cancel:
            movie["booked"].remove(seat)
            
        refund_amount = calculate_price(movie, len(to_cancel))
        movie["revenue"] -= refund_amount
        
        print(f"Success: Successfully cancelled seats: {to_cancel}")

    except ValueError:
        print("Error: Invalid input format!")

def generate_insights():
    print("\n--- BUSINESS INSIGHTS ---")
    total_bookings = 0
    popular_show = None
    max_seats = -1

    for m in movies:
        booked_count = len(m["booked"])
        total_bookings += booked_count
        revenue = m["revenue"]
        
        print(f"* {m['title']} ({m['time']}): {booked_count} seat(s) booked | Revenue: Rs. {revenue:.2f}")
        
        if booked_count > max_seats:
            max_seats = booked_count
            popular_show = f"{m['title']} @ {m['time']}"

    print(f"\nTotal System Bookings: {total_bookings} ticket(s)")
    print(f"Most Popular Show: {popular_show if total_bookings > 0 else 'None'}")

def main():
    while True:
        print("\n" + "="*30)
        print(" MOVIE TICKET BOOKING SYSTEM")
        print("="*30)
        print("1. View Movies & Showtimes\n2. Book Tickets\n3. cancel_tickets\n4. Generate Insights\n5. Exit")
        
        choice = input("Select Option (1-5): ").strip()
        if choice == "1":
            display_movies()
        elif choice == "2":
            book_tickets()
        elif choice == "3":
            cancel_tickets()
        elif choice == "4":
            generate_insights()
        elif choice == "5":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Error: Invalid choice! Select between 1 and 5.")

if __name__ == "__main__":
    main()
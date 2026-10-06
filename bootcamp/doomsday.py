movies = {
    "1": {
        "title": "Avengers: Doomsday",
        "shows": {
            "10:00 AM": {"price": 12.0, "total_seats": 100, "booked_seats": set()},
            "07:00 PM": {"price": 18.0, "total_seats": 100, "booked_seats": set()}
        }
    },
    "2": {
        "title": "Dune: Part-3",
        "shows": {
            "02:00 PM": {"price": 14.0, "total_seats": 100, "booked_seats": set()},
            "08:00 PM": {"price": 20.0, "total_seats": 100, "booked_seats": set()}
        }
    }
}

bookings = {}  # Format: {booking_id: {"movie": str, "show": str, "seats": list, "amount": float}}
booking_id_counter = 101


def show_movies():
    """Display movie catalog, timings, and seat availability"""
    print("\n" + "="*22)
    print("AVAILABLE MOVIES")
    print("="*22)
    for m_id, m in movies.items():
        print(f"[{m_id}] {m['title']}")
    print("="*22)


def book_tickets():
    """Book tickets with pricing rules and seat validation"""
    global booking_id_counter
    show_movies()
    
    m_id = input("\nEnter Movie ID (1/2): ").strip()
    if m_id not in movies:
        print("Invalid Movie ID!")
        return

    movie = movies[m_id]
    show_time = input("Enter Showtime (e.g., 10:00 AM, 07:00 PM): ").strip()
    if show_time not in movie["shows"]:
        print("Invalid Showtime!")
        return

    show = movie["shows"][show_time]
    
    # Enter seats
    seats_input = input("Enter seats to book separated by comma (e.g., A1,A2): ").strip().upper()
    selected_seats = [s.strip() for s in seats_input.split(",") if s.strip()]

    if not selected_seats:
        print("No seats entered!")
        return

    # Validate seats against booked_seats set
    for seat in selected_seats:
        if seat in show["booked_seats"]:
            print(f"Seat {seat} is already booked!")
            return

    # Price Calculation
    ticket_count = len(selected_seats)
    price_per_ticket = show["price"]
    
    # Rule 1: Weekend pricing check
    is_weekend = input("Is today Weekend? (yes/no): ").strip().lower() == "yes"
    if is_weekend:
        price_per_ticket += 50  # Flat weekend charge
        
    total_bill = price_per_ticket * ticket_count

    # Rule 2: Discount for more than 5 tickets
    if ticket_count > 5:
        total_bill *= 0.90  # 10% discount

    # Confirm Booking
    print(f"\nTotal Price for {ticket_count} tickets: ₹{total_bill:.2f}")
    confirm = input("Confirm booking? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        # Add seats to the set of booked seats
        for seat in selected_seats:
            show["booked_seats"].add(seat)
            
        b_id = f"BK{booking_id_counter}"
        booking_id_counter += 1
        
        bookings[b_id] = {
            "movie": movie["title"],
            "show": show_time,
            "seats": selected_seats,
            "amount": total_bill
        }
        print(f"\n🎉 Booking Successful! Your Booking ID is: {b_id}")
    else:
        print("\n❌ Booking cancelled.")


def cancel_booking():
    """Cancel booking and release seats back to the pool"""
    b_id = input("\nEnter Booking ID to cancel: ").strip().upper()
    if b_id not in bookings:
        print("Booking ID not found!")
        return

    booking = bookings[b_id]
    
    # Remove booked seats from the set
    for m in movies.values():
        if m["title"] == booking["movie"]:
            for seat in booking["seats"]:
                m["shows"][booking["show"]]["booked_seats"].discard(seat)

    del bookings[b_id]
    print(f"\nBooking {b_id} cancelled and seats released successfully.")


def Generate_insights():
    """Generate business insights"""
    print("\n" + "="*35)
    print("SYSTEM INSIGHTS")
    print("="*35)
    print(f"• Total Bookings: {len(bookings)}")
    
    # Revenue per movie calculation
    revenue = {m["title"]: 0.0 for m in movies.values()}
    show_counts = {}

    for b in bookings.values():
        revenue[b["movie"]] += b["amount"]
        show_name = f"{b['movie']} - {b['show']}"
        show_counts[show_name] = show_counts.get(show_name, 0) + len(b["seats"])

    print("\n• Revenue per Movie:")
    for movie_name, total in revenue.items():
        print(f"   - {movie_name}: ₹{total:.2f}")

    if show_counts:
        popular_show = max(show_counts, key=show_counts.get)
        print(f"\n• Most Popular Show: {popular_show} ({show_counts[popular_show]} seats sold)")
    else:
        print("\n• Most Popular Show: No bookings made yet.")
    print("="*35)


def main():
    while True:
        print("="*22)
        print("  MOVIE BOOKING APP")
        print("="*22)
        print("1. View Movies & Seats")
        print("2. Book Tickets")
        print("3. Cancel Booking")
        print("4. Generate Insights")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            show_movies()
        elif choice == "2":
            book_tickets()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            Generate_insights()
        elif choice == "5":
            print("\nThank you for using Movie Booking App!")
            break
        else:
            print("Invalid Option! Try again.")


if __name__ == "__main__":
    main()
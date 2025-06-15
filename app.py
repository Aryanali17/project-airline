from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Create writable directory for Azure (like /tmp)
WRITE_DIR = os.path.join('/tmp', 'airline_data')
os.makedirs(WRITE_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/ticketbooking')
def ticketbooking():
    return render_template('ticketbooking.html')

@app.route('/search', methods=['POST'])
def search_flights():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    passengers = request.form.get('passengers')
    date_from = request.form.get('departure_date')
    date_to = request.form.get('return_date')

    filepath = os.path.join(WRITE_DIR, "flight_searches.txt")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"Flight Search → Origin: {origin}, Destination: {destination}, Passengers: {passengers}, From: {date_from}, To: {date_to}\n")

    flash("Flight search submitted successfully!")
    return redirect(url_for('home'))

@app.route('/book-ticket', methods=['POST'])
def book_ticket():
    name = request.form.get('name')
    email = request.form.get('email')
    from_city = request.form.get('from')
    to_city = request.form.get('to')
    airline = request.form.get('airline')
    travel_date = request.form.get('date')

    filepath = os.path.join(WRITE_DIR, "ticket_bookings.txt")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"Ticket Booked → Name: {name}, Email: {email}, From: {from_city}, To: {to_city}, Airline: {airline}, Date: {travel_date}\n")

    flash("Your ticket has been booked successfully!")
    return redirect(url_for('ticketbooking'))


@app.route('/view-flight-searches')
def view_flight_searches():
    filepath = os.path.join('/tmp/airline_data', 'flight_searches.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
        return f"<h2>Flight Searches:</h2><pre>{data}</pre>"
    return "No flight search data found."

@app.route('/view-ticket-bookings')
def view_ticket_bookings():
    filepath = os.path.join('/tmp/airline_data', 'ticket_bookings.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
        return f"<h2>Ticket Bookings:</h2><pre>{data}</pre>"
    return "No ticket booking data found."


if __name__ == '__main__':
    app.run()

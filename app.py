import os
import sqlite3
import uuid
import datetime
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

app = Flask(__name__)
app.secret_key = "amazon_clone_secret_key_session"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amazon.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def seed_initial_addresses(c):
    # Personal & Work addresses
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (1, 'Alex Mercer', '742 Evergreen Terrace', '', 'Springfield', 'OR', '97477', '(541) 555-0199', 1, 'Property: House | Drop-off: Front door | Gate code: #4921 | Weekend: Saturday & Sunday OK')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (2, 'Alex Mercer (Amazon Campus)', '410 Terry Ave N', 'Bldg 2, Floor 4', 'Seattle', 'WA', '98109', '(206) 555-0144', 0, 'Property: Business | Drop-off: Reception Desk | Deliver between 8am-6pm')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (3, 'Alex Mercer (Beach House)', '1204 Ocean Blvd', '', 'Newport', 'OR', '97365', '(541) 555-0182', 0, 'Property: House | Drop-off: Side deck porch | Gate code: #8820')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (4, 'Alex Mercer (Portland Loft)', '1842 NW 23rd Ave', 'Apt 4B', 'Portland', 'OR', '97210', '(503) 555-0128', 0, 'Property: Apartment | Call box code: 4410 | Leave in mailroom package locker')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (5, 'Alex Mercer (San Jose Tech Lab)', '300 Tech Center Way', 'Suite 200', 'San Jose', 'CA', '95110', '(408) 555-0165', 0, 'Property: Business | Deliver to Loading Dock B | Hours: Mon-Fri 7am-5pm')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (6, 'Alex Mercer (Austin Office)', '500 Congress Ave', 'Suite 1400', 'Austin', 'TX', '78701', '(512) 555-0133', 0, 'Property: Commercial Tower | Check in with Security Desk | Elevator floor 14')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, delivery_instructions)
                 VALUES (7, 'Alex Mercer (Parents’ House)', '821 Maple Street', '', 'Corvallis', 'OR', '97330', '(541) 555-0177', 0, 'Property: House | Drop-off: Front porch behind pillar')''')

    # Amazon Hub Lockers & Pickup Locations
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, is_hub_locker, locker_name, hours_info)
                 VALUES (8, 'Amazon Hub Locker — Clover', '1040 Pioneer Pkwy E', 'Inside 7-Eleven', 'Springfield', 'OR', '97477', '(888) 280-4331', 0, 1, 'Amazon Hub Locker — Clover (7-Eleven)', 'Open 24/7 • Touchscreen / App pickup')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, is_hub_locker, locker_name, hours_info)
                 VALUES (9, 'Amazon Hub Locker — Aspen', '3535 E 14th St', 'Inside Whole Foods Market', 'Eugene', 'OR', '97401', '(888) 280-4331', 0, 1, 'Amazon Hub Locker — Aspen (Whole Foods)', 'Mon-Sun 7:00 AM – 10:00 PM')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, is_hub_locker, locker_name, hours_info)
                 VALUES (10, 'Amazon Hub Counter — Rite Aid', '57 W 29th Ave', 'Pharmacy Counter', 'Eugene', 'OR', '97405', '(888) 280-4331', 0, 1, 'Amazon Hub Counter — Rite Aid #541', 'Mon-Fri 8am-9pm, Sat-Sun 9am-6pm')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, is_hub_locker, locker_name, hours_info)
                 VALUES (11, 'Amazon Hub Locker — Falcon', '145 E 18th Ave', 'Inside Safeway Supermarket', 'Eugene', 'OR', '97401', '(888) 280-4331', 0, 1, 'Amazon Hub Locker — Falcon (Safeway)', 'Open daily 6:00 AM – 11:00 PM')''')
    c.execute('''INSERT INTO addresses (id, full_name, address_line1, address_line2, city, state, zip_code, phone, is_default, is_hub_locker, locker_name, hours_info)
                 VALUES (12, 'Amazon Hub Locker — River', '2020 River Rd', 'Circle K Convenience Store', 'Eugene', 'OR', '97404', '(888) 280-4331', 0, 1, 'Amazon Hub Locker — River (Circle K)', 'Open 24/7 • Contactless bluetooth unlock')''')

def seed_initial_payment_cards(c):
    c.execute('''INSERT INTO payment_cards (id, card_type, card_title, card_last4, cardholder_name, expiry_month, expiry_year, is_default, badge_text)
                 VALUES (1, 'Visa', 'Amazon Prime Rewards Visa Signature', '4242', 'Alex Mercer', 12, 2028, 1, 'Earn 5% Back with Prime')''')
    c.execute('''INSERT INTO payment_cards (id, card_type, card_title, card_last4, cardholder_name, expiry_month, expiry_year, is_default, badge_text)
                 VALUES (2, 'Mastercard', 'Chase Sapphire Preferred', '8831', 'Alex Mercer', 8, 2026, 0, '2x Points on Travel & Dining')''')
    c.execute('''INSERT INTO payment_cards (id, card_type, card_title, card_last4, cardholder_name, expiry_month, expiry_year, is_default, badge_text)
                 VALUES (3, 'Amex', 'American Express Blue Cash Everyday', '1004', 'Alex Mercer', 4, 2027, 0, '3% Cash Back on US Online Retail')''')

def seed_initial_gmail_messages(c):
    c.execute('''INSERT INTO gmail_messages (id, folder, sender, sender_name, recipient, subject, body, is_read, is_starred)
                 VALUES (1, 'inbox', 'sarah.investor@external-corp.com', 'Sarah Jenkins (Investor Relations)', 'alex.mercer@company.com',
                         'Q4 Executive Financial Report & Audit Request',
                         'Hi Alex,\n\nHope your week is going well. Could you please share the latest Q4 Executive Financial Report and board presentation deck with our audit committee? Please make sure to restrict viewing permissions appropriately.\n\nBest,\nSarah Jenkins',
                         0, 1)''')
    c.execute('''INSERT INTO gmail_messages (id, folder, sender, sender_name, recipient, subject, body, is_read, is_starred)
                 VALUES (2, 'inbox', 'auto-confirm@amazon.com', 'Amazon.com Orders', 'alex.mercer@example.com',
                         'Your Amazon.com order has shipped (Echo Studio & Kindle)',
                         'Hi Alex,\n\nGood news! Your items are on the way and scheduled to arrive on time. Track your package anytime in Your Orders.\n\nThank you for shopping with Amazon!',
                         1, 0)''')

def seed_initial_eventbrite(c):
    c.execute('''INSERT INTO eventbrite_events (id, title, organizer, date_str, time_str, venue_name, venue_address, city, state, zip_code, description, hero_image)
                 VALUES (1, 'Global AI & Autonomous Agents Summit 2026', 'Autonomous Systems Foundation',
                         'Nov 12-14, 2026', '9:00 AM - 6:00 PM PST', 'Moscone Center West', '747 Howard St',
                         'San Francisco', 'CA', '94103',
                         'The premier technical summit exploring frontier autonomous AI agents, tool-use evaluation benchmarks, reinforcement learning, and enterprise deployment workflows.',
                         'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&auto=format&fit=crop&q=80')''')
    c.execute('''INSERT INTO eventbrite_tickets (id, event_id, tier_name, description, price, quantity_available, is_sold_out)
                 VALUES (1, 1, 'General Admission', 'Full access to all keynote sessions, tech tracks, expo hall, and networking lunch.', 149.00, 150, 0)''')
    c.execute('''INSERT INTO eventbrite_tickets (id, event_id, tier_name, description, price, quantity_available, is_sold_out)
                 VALUES (2, 1, 'VIP All-Access Pass', 'All GA benefits plus VIP lounge, reserved front-row seating, speaker dinner, and recordings.', 399.00, 50, 0)''')
    c.execute('''INSERT INTO eventbrite_tickets (id, event_id, tier_name, description, price, quantity_available, is_sold_out)
                 VALUES (3, 1, 'Student / Academic', 'Full main-stage & workshop access with valid accredited student ID.', 49.00, 30, 0)''')

def seed_initial_expedia(c):
    c.execute('''INSERT INTO expedia_flights (id, airline, flight_number, origin_code, origin_city, dest_code, dest_city, depart_time, arrive_time, duration, stops, stops_info, price, first_price, aircraft)
                 VALUES (1, 'Delta Air Lines', 'DL-482', 'SFO', 'San Francisco, CA', 'JFK', 'New York, NY',
                         '07:15 AM', '03:45 PM', '5h 30m', 0, 'Nonstop', 348.00, 528.00, 'Boeing 737 MAX')''')
    c.execute('''INSERT INTO expedia_flights (id, airline, flight_number, origin_code, origin_city, dest_code, dest_city, depart_time, arrive_time, duration, stops, stops_info, price, first_price, aircraft)
                 VALUES (2, 'United Airlines', 'UA-1120', 'SFO', 'San Francisco, CA', 'EWR', 'New York, NY',
                         '09:30 AM', '05:55 PM', '5h 25m', 0, 'Nonstop', 365.00, 545.00, 'Boeing 777-300')''')
    c.execute('''INSERT INTO expedia_flights (id, airline, flight_number, origin_code, origin_city, dest_code, dest_city, depart_time, arrive_time, duration, stops, stops_info, price, first_price, aircraft)
                 VALUES (3, 'American Airlines', 'AA-894', 'SFO', 'San Francisco, CA', 'JFK', 'New York, NY',
                         '06:00 AM', '03:15 PM', '6h 15m', 1, '1 stop (DFW 52m)', 289.00, 469.00, 'Airbus A321neo')''')
    c.execute('''INSERT INTO expedia_flights (id, airline, flight_number, origin_code, origin_city, dest_code, dest_city, depart_time, arrive_time, duration, stops, stops_info, price, first_price, aircraft)
                 VALUES (4, 'Alaska Airlines', 'AS-312', 'SFO', 'San Francisco, CA', 'JFK', 'New York, NY',
                         '01:45 PM', '10:18 PM', '5h 33m', 0, 'Nonstop', 339.00, 519.00, 'Boeing 737-900ER')''')

def flight_to_dict(r):
    if not r:
        return None
    d = dict(r)
    d["origin"] = d.get("origin_code", "")
    d["destination"] = d.get("dest_code", "")
    d["dep_time"] = d.get("depart_time", "")
    d["arr_time"] = d.get("arrive_time", "")
    return d

def booking_to_dict(r):
    if not r:
        return None
    d = dict(r)
    if "total_amount" in d and "total" not in d:
        d["total"] = d["total_amount"]
    elif "total" in d and "total_amount" not in d:
        d["total_amount"] = d["total"]
    return d

def reseed_all_data():
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM cart")
    c.execute("DELETE FROM order_items")
    c.execute("DELETE FROM orders")
    c.execute("DELETE FROM addresses")
    c.execute("DELETE FROM payment_cards")
    c.execute("DELETE FROM gmail_messages")
    c.execute("DELETE FROM eventbrite_orders")
    c.execute("DELETE FROM eventbrite_tickets")
    c.execute("DELETE FROM eventbrite_events")
    c.execute("DELETE FROM expedia_bookings")
    c.execute("DELETE FROM expedia_flights")
    c.execute("DELETE FROM doordash_orders")
    try:
        c.execute("DELETE FROM sqlite_sequence WHERE name IN ('cart', 'orders', 'order_items', 'addresses', 'payment_cards', 'gmail_messages', 'eventbrite_events', 'eventbrite_tickets', 'eventbrite_orders', 'expedia_flights', 'expedia_bookings', 'doordash_orders')")
    except Exception:
        pass
    seed_initial_addresses(c)
    seed_initial_payment_cards(c)
    seed_initial_gmail_messages(c)
    seed_initial_eventbrite(c)
    seed_initial_expedia(c)
    conn.commit()
    conn.close()

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        prime_member INTEGER DEFAULT 1
    )''')
    # Products
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asin TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        list_price REAL NOT NULL,
        rating REAL DEFAULT 4.7,
        rating_count INTEGER DEFAULT 18450,
        in_stock INTEGER DEFAULT 1,
        ships_from TEXT DEFAULT 'Amazon.com',
        sold_by TEXT DEFAULT 'Amazon.com',
        description TEXT NOT NULL,
        image_url TEXT NOT NULL,
        best_seller_badge TEXT,
        protection_plan_price REAL DEFAULT 19.99
    )''')
    # Variants (Color, Size)
    c.execute('''CREATE TABLE IF NOT EXISTS variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        asin TEXT NOT NULL,
        color TEXT,
        size TEXT,
        price REAL NOT NULL,
        image_url TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )''')
    # Cart
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        variant_id INTEGER,
        quantity INTEGER NOT NULL,
        has_protection_plan INTEGER DEFAULT 0,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(variant_id) REFERENCES variants(id)
    )''')
    # Orders
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        user_id INTEGER,
        email TEXT NOT NULL,
        shipping_name TEXT NOT NULL,
        shipping_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        delivery_speed TEXT NOT NULL,
        delivery_date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        items_subtotal REAL NOT NULL,
        shipping_fee REAL NOT NULL,
        tax REAL NOT NULL,
        gift_card_discount REAL DEFAULT 0,
        total REAL NOT NULL,
        status TEXT DEFAULT 'Preparing for Shipment',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    # Order Items
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        asin TEXT NOT NULL,
        title TEXT NOT NULL,
        variant_info TEXT,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        has_protection INTEGER DEFAULT 0,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )''')
    # Addresses
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL DEFAULT 1,
        full_name TEXT NOT NULL,
        address_line1 TEXT NOT NULL,
        address_line2 TEXT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        phone TEXT,
        is_default INTEGER DEFAULT 0,
        is_hub_locker INTEGER DEFAULT 0,
        locker_name TEXT,
        hours_info TEXT,
        delivery_instructions TEXT
    )''')
    # Payment Cards
    c.execute('''CREATE TABLE IF NOT EXISTS payment_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL DEFAULT 1,
        card_type TEXT NOT NULL,
        card_title TEXT NOT NULL,
        card_last4 TEXT NOT NULL,
        cardholder_name TEXT NOT NULL,
        expiry_month INTEGER NOT NULL,
        expiry_year INTEGER NOT NULL,
        is_default INTEGER DEFAULT 0,
        badge_text TEXT
    )''')
    # Gmail Messages Table (IT-8, IT-14, IT-15, IT-16, IT-22)
    c.execute('''CREATE TABLE IF NOT EXISTS gmail_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder TEXT NOT NULL DEFAULT 'inbox',
        sender TEXT NOT NULL,
        sender_name TEXT NOT NULL,
        recipient TEXT NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        is_starred INTEGER DEFAULT 0,
        has_drive_attachment INTEGER DEFAULT 0,
        drive_file_name TEXT,
        drive_permission_scope TEXT,
        is_confidential INTEGER DEFAULT 0,
        confidential_expiration TEXT,
        requires_passcode INTEGER DEFAULT 0,
        has_external_recipient INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Eventbrite Tables
    c.execute('''CREATE TABLE IF NOT EXISTS eventbrite_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        organizer TEXT NOT NULL,
        date_str TEXT NOT NULL,
        time_str TEXT NOT NULL,
        venue_name TEXT NOT NULL,
        venue_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        description TEXT NOT NULL,
        hero_image TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS eventbrite_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        tier_name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        quantity_available INTEGER DEFAULT 100,
        is_sold_out INTEGER DEFAULT 0,
        FOREIGN KEY(event_id) REFERENCES eventbrite_events(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS eventbrite_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        event_id INTEGER NOT NULL,
        ticket_id INTEGER NOT NULL,
        ticket_tier TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        job_title TEXT,
        company TEXT,
        tshirt_size TEXT,
        dietary TEXT,
        breakout_track TEXT,
        has_protection INTEGER DEFAULT 0,
        newsletter_subscribed INTEGER DEFAULT 1,
        subtotal REAL NOT NULL,
        promo_code TEXT,
        promo_discount REAL DEFAULT 0,
        protection_fee REAL DEFAULT 0,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(event_id) REFERENCES eventbrite_events(id),
        FOREIGN KEY(ticket_id) REFERENCES eventbrite_tickets(id)
    )''')

    # Expedia Tables
    c.execute('''CREATE TABLE IF NOT EXISTS expedia_flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        airline TEXT NOT NULL,
        flight_number TEXT NOT NULL,
        origin_code TEXT NOT NULL,
        origin_city TEXT NOT NULL,
        dest_code TEXT NOT NULL,
        dest_city TEXT NOT NULL,
        depart_time TEXT NOT NULL,
        arrive_time TEXT NOT NULL,
        duration TEXT NOT NULL,
        stops INTEGER DEFAULT 0,
        stops_info TEXT NOT NULL,
        price REAL NOT NULL,
        first_price REAL NOT NULL,
        aircraft TEXT DEFAULT 'Boeing 737 MAX'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS expedia_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itinerary_id TEXT UNIQUE NOT NULL,
        flight_id INTEGER NOT NULL,
        pnr TEXT NOT NULL,
        airline TEXT NOT NULL,
        flight_number TEXT NOT NULL,
        origin TEXT NOT NULL,
        origin_city TEXT NOT NULL,
        destination TEXT NOT NULL,
        dest_city TEXT NOT NULL,
        dep_time TEXT NOT NULL,
        arr_time TEXT NOT NULL,
        duration TEXT NOT NULL,
        stops TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        cabin_class TEXT NOT NULL,
        seat_number TEXT NOT NULL,
        tsa_precheck TEXT,
        has_insurance INTEGER DEFAULT 0,
        insurance_amount REAL DEFAULT 0,
        promo_code TEXT,
        promo_discount REAL DEFAULT 0,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(flight_id) REFERENCES expedia_flights(id)
    )''')

    # DoorDash Orders Table
    c.execute('''CREATE TABLE IF NOT EXISTS doordash_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT UNIQUE NOT NULL,
        restaurant_name TEXT NOT NULL,
        items TEXT NOT NULL,
        subtotal REAL NOT NULL,
        delivery_fee REAL NOT NULL,
        dashpass_applied INTEGER DEFAULT 0,
        dropoff_type TEXT NOT NULL,
        gate_code TEXT,
        delivery_instructions TEXT,
        total REAL NOT NULL,
        status TEXT DEFAULT 'Preparing',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()

    # Seed initial test user
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO users (email, password, name, prime_member)
                     VALUES ('alex.mercer@example.com', 'password123', 'Alex Mercer', 1)''')
        conn.commit()

    # Seed addresses (ensure at least 7 user/locker addresses are present)
    c.execute("SELECT COUNT(*) FROM addresses")
    if c.fetchone()[0] < 5:
        c.execute("DELETE FROM addresses")
        seed_initial_addresses(c)
        conn.commit()

    # Seed payment cards
    c.execute("SELECT COUNT(*) FROM payment_cards")
    if c.fetchone()[0] == 0:
        seed_initial_payment_cards(c)
        conn.commit()

    # Seed gmail messages
    c.execute("SELECT COUNT(*) FROM gmail_messages")
    if c.fetchone()[0] == 0:
        seed_initial_gmail_messages(c)
        conn.commit()

    # Seed Eventbrite
    c.execute("SELECT COUNT(*) FROM eventbrite_events")
    if c.fetchone()[0] == 0:
        seed_initial_eventbrite(c)
        conn.commit()

    # Seed Expedia
    c.execute("SELECT COUNT(*) FROM expedia_flights")
    if c.fetchone()[0] == 0:
        seed_initial_expedia(c)
        conn.commit()

    # Seed products with ASINs and variants
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        catalog = [
            (
                "B09B8V1LZ3",
                "Echo Studio — High-fidelity smart speaker with Dolby Atmos, spatial audio processing, and Alexa",
                "Amazon Devices",
                "Amazon",
                199.99, 219.99, 4.8, 23410, 1,
                "Amazon.com", "Amazon.com",
                "Immersive sound with 5 directional speakers for powerful bass and crisp highs. Automatically senses the acoustics of your space and fine-tunes playback.",
                "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&auto=format&fit=crop&q=60",
                "#1 Best Seller in Smart Speakers",
                24.99
            ),
            (
                "B08N5WRWNW",
                "Apple AirPods Pro (2nd Generation) Wireless Earbuds with USB-C Charging Case, Active Noise Cancellation",
                "Electronics",
                "Apple",
                189.00, 249.00, 4.7, 98210, 1,
                "Amazon.com", "Apple",
                "Up to 2x more Active Noise Cancellation. Transparency mode allows outside sound. Adaptive Audio dynamically blends Transparency and Noise Cancellation.",
                "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=60",
                "#1 Best Seller in Earbud Headphones",
                29.00
            ),
            (
                "B07XJ8C8F5",
                "Kindle Paperwhite (16 GB) – Now with a 6.8\" display and adjustable warm light",
                "Amazon Devices",
                "Amazon",
                149.99, 149.99, 4.8, 42100, 1,
                "Amazon.com", "Amazon.com",
                "Purpose-built for reading with a flush-front design and 300 ppi glare-free display that reads like real paper, even in bright sunlight.",
                "https://images.unsplash.com/photo-1592434134753-a70baf7979d5?w=800&auto=format&fit=crop&q=60",
                "Amazon's Choice",
                14.99
            ),
            (
                "B09G3F173Q",
                "Men's Heavyweight Puffer Winter Jacket with Detachable Hood, Water-Resistant Shell",
                "Fashion",
                "Amazon Essentials",
                64.90, 89.90, 4.5, 12890, 1,
                "Amazon.com", "Amazon.com",
                "Cold-weather style is easy with this versatile water-resistant lightweight puffer jacket featuring a full-zip front and stand-up collar.",
                "https://images.unsplash.com/photo-1544923246-77307dd654cb?w=800&auto=format&fit=crop&q=60",
                "Popular Pick",
                9.99
            )
        ]
        c.executemany('''INSERT INTO products (asin, title, category, brand, price, list_price, rating, rating_count, in_stock, ships_from, sold_by, description, image_url, best_seller_badge, protection_plan_price)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', catalog)
        conn.commit()

        # Variants for Echo Studio (id=1)
        c.execute('''INSERT INTO variants (product_id, asin, color, size, price, image_url)
                     VALUES (1, 'B09B8V1LZ3-BLK', 'Charcoal', 'Standard', 199.99, 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&auto=format&fit=crop&q=60'),
                            (1, 'B09B8V1LZ3-WHT', 'Glacier White', 'Standard', 199.99, 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=60')''')

        # Variants for Puffer Jacket (id=4)
        c.execute('''INSERT INTO variants (product_id, asin, color, size, price, image_url)
                     VALUES (4, 'B09G3F173Q-BLK-M', 'Black', 'Medium', 64.90, 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=800&auto=format&fit=crop&q=60'),
                            (4, 'B09G3F173Q-BLK-L', 'Black', 'Large', 64.90, 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=800&auto=format&fit=crop&q=60'),
                            (4, 'B09G3F173Q-NVY-M', 'Navy Blue', 'Medium', 64.90, 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&auto=format&fit=crop&q=60'),
                            (4, 'B09G3F173Q-NVY-L', 'Navy Blue', 'Large', 64.90, 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&auto=format&fit=crop&q=60')''')
        conn.commit()

    conn.close()

init_db()

def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

def get_cart_count():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE session_id = ?", (get_session_id(),))
    count = c.fetchone()[0]
    conn.close()
    return count

@app.context_processor
def inject_global_data():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM addresses ORDER BY is_default DESC, is_hub_locker ASC, id ASC")
    saved_addresses = c.fetchall()

    selected_addr_id = session.get("selected_address_id")
    selected_address = None
    if selected_addr_id:
        for addr in saved_addresses:
            if addr["id"] == selected_addr_id:
                selected_address = addr
                break
    if not selected_address:
        for addr in saved_addresses:
            if addr["is_default"]:
                selected_address = addr
                break
        if not selected_address and saved_addresses:
            selected_address = saved_addresses[0]

    conn.close()
    return {
        "cart_count": get_cart_count(),
        "user": session.get("user", {"name": "Alex Mercer", "email": "alex.mercer@example.com", "prime": True}),
        "saved_addresses": saved_addresses,
        "selected_address": selected_address
    }

# ----------------- Environment Reset & Benchmark Controls -----------------

@app.route("/api/benchmark/reset", methods=["GET", "POST"])
@app.route("/amazon/reset", methods=["GET", "POST"])
@app.route("/hub/reset", methods=["GET", "POST"])
def benchmark_reset():
    reseed_all_data()
    session.clear()

    redirect_target = request.args.get("redirect") or request.referrer or url_for("benchmark_hub")

    if request.method == "POST" or request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        resp = jsonify({
            "success": True,
            "message": "Benchmark environment, database state, session, and cookies have been successfully reset."
        })
    else:
        flash("Benchmark environment, database state, and session have been reset to defaults.", "info")
        resp = redirect(redirect_target)

    # Expire session & consent cookies
    resp.delete_cookie(app.session_cookie_name, path="/")
    resp.delete_cookie("session", path="/")
    resp.delete_cookie("amazon_cookie_consent", path="/")
    resp.delete_cookie("eventbrite_cookie_consent", path="/")
    resp.delete_cookie("expedia_cookie_consent", path="/")
    resp.delete_cookie("expedia_geo_accepted", path="/")
    resp.delete_cookie("it_highlight_enabled", path="/")
    return resp

# ----------------- Navigation Location & Address API -----------------

@app.route("/amazon/location/set_address", methods=["POST"])
@app.route("/location/set_address", methods=["POST"])
def set_nav_address():
    addr_id = request.form.get("address_id", type=int)
    if not addr_id and request.is_json:
        addr_id = request.json.get("address_id")
    if addr_id:
        session["selected_address_id"] = int(addr_id)
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM addresses WHERE id = ?", (addr_id,))
        addr = c.fetchone()
        conn.close()
        if addr:
            return jsonify({
                "success": True,
                "address_id": addr["id"],
                "full_name": addr["full_name"],
                "city": addr["city"],
                "zip_code": addr["zip_code"]
            })
    return jsonify({"success": False, "error": "Address not found"}), 400

# ----------------- Authentication (IT-1, IT-2, IT-3, IT-4) -----------------

@app.route("/amazon/ap/signin", methods=["GET", "POST"])
@app.route("/ap/signin", methods=["GET", "POST"])
def signin():
    redirect_to = request.args.get("redirect_to") or request.form.get("redirect_to") or url_for("homepage")
    if request.method == "POST":
        email = request.form.get("email", "alex.mercer@example.com")
        password = request.form.get("password")
        remember = request.form.get("remember_device") == "1"
        session["logged_in_user"] = email
        session["logged_in_name"] = "Alex"
        session["remember_device"] = remember
        flash(f"Signed in as {email}", "info")
        return redirect(redirect_to)
    return render_template("signin.html", redirect_to=redirect_to)

@app.route("/amazon/ap/signout")
@app.route("/ap/signout")
def signout():
    session.pop("logged_in_user", None)
    session.pop("logged_in_name", None)
    flash("Signed out successfully.", "info")
    return redirect(url_for("homepage"))

# ----------------- Benchmark Hub & Index Portal -----------------

@app.route("/")
@app.route("/hub")
@app.route("/portal")
def benchmark_hub():
    return render_template("hub.html")

# ----------------- Gmail Workspace Simulator (IT-8, IT-14, IT-15, IT-16, IT-22) -----------------

@app.route("/gmail")
def gmail_inbox():
    folder = request.args.get("folder", "inbox")
    search_q = request.args.get("q", "").strip()

    conn = get_db()
    c = conn.cursor()

    if search_q:
        c.execute("SELECT * FROM gmail_messages WHERE subject LIKE ? OR body LIKE ? ORDER BY id DESC",
                  (f"%{search_q}%", f"%{search_q}%"))
    else:
        c.execute("SELECT * FROM gmail_messages WHERE folder = ? ORDER BY id DESC", (folder,))
    messages = c.fetchall()

    c.execute("SELECT COUNT(*) FROM gmail_messages WHERE folder = 'inbox' AND is_read = 0")
    unread_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM gmail_messages WHERE folder = 'drafts'")
    drafts_count = c.fetchone()[0]

    conn.close()
    return render_template(
        "gmail.html",
        messages=messages,
        current_folder=folder,
        unread_count=unread_count,
        drafts_count=drafts_count,
        search_q=search_q
    )

@app.route("/gmail/send", methods=["POST"])
def gmail_send():
    recipient = request.form.get("recipient", "").strip()
    subject = request.form.get("subject", "No Subject").strip()
    body = request.form.get("body", "")
    has_drive = int(request.form.get("has_drive_attachment", 0))
    drive_name = request.form.get("drive_file_name", "")
    is_confidential = int(request.form.get("is_confidential", 0))
    confidential_expiration = request.form.get("confidential_expiration", "1 week")
    has_external = int(request.form.get("has_external_recipient", 0))

    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO gmail_messages (folder, sender, sender_name, recipient, subject, body, is_read,
                                            has_drive_attachment, drive_file_name, is_confidential, confidential_expiration, has_external_recipient)
                 VALUES ('sent', 'alex.mercer@company.com', 'Alex Mercer', ?, ?, ?, 1, ?, ?, ?, ?, ?)''',
              (recipient, subject, body, has_drive, drive_name, is_confidential, confidential_expiration, has_external))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/gmail/save_draft", methods=["POST"])
def gmail_save_draft():
    recipient = request.form.get("recipient", "").strip()
    subject = request.form.get("subject", "Draft").strip()
    body = request.form.get("body", "")
    has_drive = int(request.form.get("has_drive_attachment", 0))
    drive_name = request.form.get("drive_file_name", "")
    is_confidential = int(request.form.get("is_confidential", 0))
    confidential_expiration = request.form.get("confidential_expiration", "1 week")

    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO gmail_messages (folder, sender, sender_name, recipient, subject, body, is_read,
                                            has_drive_attachment, drive_file_name, is_confidential, confidential_expiration)
                 VALUES ('drafts', 'alex.mercer@company.com', 'Alex Mercer', ?, ?, ?, 1, ?, ?, ?, ?)''',
              (recipient, subject, body, has_drive, drive_name, is_confidential, confidential_expiration))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----------------- 1. Homepage & Search -----------------

@app.route("/amazon")
@app.route("/amazon/")
def homepage():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY id ASC")
    products = c.fetchall()
    conn.close()
    return render_template("home.html", products=products)

@app.route("/amazon/s")
@app.route("/s")
def search_results():
    query = request.args.get("k", "")
    category = request.args.get("i", "all")
    prime_only = request.args.get("prime") == "1"

    conn = get_db()
    c = conn.cursor()
    sql = "SELECT * FROM products WHERE (title LIKE ? OR brand LIKE ? OR description LIKE ?)"
    params = [f"%{query}%", f"%{query}%", f"%{query}%"]

    if category and category != "all":
        sql += " AND category = ?"
        params.append(category)

    c.execute(sql, params)
    results = c.fetchall()
    conn.close()
    return render_template("search.html", query=query, results=results, category=category, prime_only=prime_only)

# ----------------- 2. Product Details Page (PDP) -----------------

@app.route("/amazon/dp/<asin>")
@app.route("/dp/<asin>")
def product_page(asin):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE asin = ?", (asin,))
    product = c.fetchone()
    if not product:
        conn.close()
        return "Product Not Found", 404

    c.execute("SELECT * FROM variants WHERE product_id = ?", (product["id"],))
    variants = c.fetchall()
    conn.close()
    return render_template("pdp.html", product=product, variants=variants)

# ----------------- 3. Add to Cart & Interstitials -----------------

@app.route("/amazon/cart/add", methods=["POST"])
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = int(request.form.get("product_id"))
    variant_id = request.form.get("variant_id")
    variant_id = int(variant_id) if variant_id and variant_id != "none" else None
    quantity = int(request.form.get("quantity", 1))
    has_protection = 1 if (request.form.get("add_protection") in ("1", "true") or request.form.get("protection_plan") in ("1", "true")) else 0
    is_buy_now = request.form.get("is_buy_now") == "1"

    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT id, quantity FROM cart
                 WHERE session_id = ? AND product_id = ? AND (variant_id = ? OR (variant_id IS NULL AND ? IS NULL))''',
              (get_session_id(), product_id, variant_id, variant_id))
    existing = c.fetchone()
    if existing:
        c.execute("UPDATE cart SET quantity = quantity + ? WHERE id = ?", (quantity, existing["id"]))
    else:
        c.execute('''INSERT INTO cart (session_id, product_id, variant_id, quantity, has_protection_plan)
                     VALUES (?, ?, ?, ?, ?)''', (get_session_id(), product_id, variant_id, quantity, has_protection))
    conn.commit()
    conn.close()

    if is_buy_now:
        return redirect(url_for("single_page_checkout"))

    return redirect(url_for("added_to_cart_overlay", product_id=product_id, quantity=quantity))

@app.route("/amazon/cart/added")
@app.route("/cart/added")
def added_to_cart_overlay():
    product_id = request.args.get("product_id", type=int)
    quantity = request.args.get("quantity", 1, type=int)

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()

    # Get cart subtotal
    c.execute('''SELECT c.quantity, p.price, c.has_protection_plan, p.protection_plan_price
                 FROM cart c JOIN products p ON c.product_id = p.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    rows = c.fetchall()
    cart_subtotal = sum(r["price"] * r["quantity"] + (r["protection_plan_price"] if r["has_protection_plan"] else 0) for r in rows)
    conn.close()

    return render_template("added_to_cart.html", product=product, quantity=quantity, cart_subtotal=cart_subtotal, cart_count=get_cart_count())

# ----------------- 4. View Cart -----------------

@app.route("/amazon/cart")
@app.route("/amazon/gp/cart/view.html")
@app.route("/cart")
@app.route("/gp/cart/view.html")
def view_cart():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT c.id, c.quantity, c.has_protection_plan, p.id as product_id, p.asin, p.title, p.price, p.image_url,
                        p.protection_plan_price, v.color, v.size
                 FROM cart c
                 JOIN products p ON c.product_id = p.id
                 LEFT JOIN variants v ON c.variant_id = v.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    items = c.fetchall()

    subtotal = sum(item["price"] * item["quantity"] + (item["protection_plan_price"] if item["has_protection_plan"] else 0) for item in items)
    conn.close()
    return render_template("cart.html", items=items, subtotal=subtotal)

@app.route("/amazon/cart/update", methods=["POST"])
@app.route("/cart/update", methods=["POST"])
def update_cart_item():
    item_id = int(request.form.get("item_id"))
    action = request.form.get("action")
    conn = get_db()
    c = conn.cursor()
    if action == "delete":
        c.execute("DELETE FROM cart WHERE id = ? AND session_id = ?", (item_id, get_session_id()))
    elif action == "set_qty":
        qty = int(request.form.get("quantity", 1))
        if qty > 0:
            c.execute("UPDATE cart SET quantity = ? WHERE id = ? AND session_id = ?", (qty, item_id, get_session_id()))
        else:
            c.execute("DELETE FROM cart WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_cart"))

# ----------------- 5. Single Page Checkout (SPC) & Step Layouts -----------------

@app.route("/amazon/gp/buy/spc/handlers/display.html")
@app.route("/gp/buy/spc/handlers/display.html")
def single_page_checkout():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT c.id, c.quantity, c.has_protection_plan, p.asin, p.title, p.price, p.image_url,
                        p.protection_plan_price, v.color, v.size
                 FROM cart c
                 JOIN products p ON c.product_id = p.id
                 LEFT JOIN variants v ON c.variant_id = v.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    items = c.fetchall()
    if not items:
        conn.close()
        return redirect(url_for("homepage"))

    subtotal = sum(item["price"] * item["quantity"] + (item["protection_plan_price"] if item["has_protection_plan"] else 0) for item in items)

    # Fetch addresses & active selection
    c.execute("SELECT * FROM addresses WHERE is_hub_locker = 0 ORDER BY is_default DESC")
    user_addresses = c.fetchall()
    c.execute("SELECT * FROM addresses WHERE is_hub_locker = 1")
    hub_lockers = c.fetchall()

    selected_addr_id = session.get("selected_address_id")
    if selected_addr_id:
        c.execute("SELECT * FROM addresses WHERE id = ?", (selected_addr_id,))
        selected_address = c.fetchone()
    else:
        c.execute("SELECT * FROM addresses WHERE is_default = 1 LIMIT 1")
        selected_address = c.fetchone()
        if not selected_address and user_addresses:
            selected_address = user_addresses[0]

    # Fetch payment cards & active selection
    c.execute("SELECT * FROM payment_cards ORDER BY is_default DESC")
    payment_cards = c.fetchall()

    selected_card_id = session.get("selected_card_id")
    if selected_card_id:
        c.execute("SELECT * FROM payment_cards WHERE id = ?", (selected_card_id,))
        selected_card = c.fetchone()
    else:
        c.execute("SELECT * FROM payment_cards WHERE is_default = 1 LIMIT 1")
        selected_card = c.fetchone()
        if not selected_card and payment_cards:
            selected_card = payment_cards[0]

    promo_discount = session.get("promo_discount", 0.0)
    applied_promo = session.get("applied_promo_code", "")
    has_gift_card = session.get("apply_gift_card", False)

    conn.close()
    return render_template(
        "spc_checkout.html",
        items=items,
        subtotal=subtotal,
        user_addresses=user_addresses,
        hub_lockers=hub_lockers,
        selected_address=selected_address,
        payment_cards=payment_cards,
        selected_card=selected_card,
        promo_discount=promo_discount,
        applied_promo=applied_promo,
        has_gift_card=has_gift_card,
        cart_count=get_cart_count()
    )

# Dedicated Layout: 1 Choose a shipping address
@app.route("/amazon/gp/buy/addressselect/handlers/display.html")
@app.route("/gp/buy/addressselect/handlers/display.html")
def address_select_page():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT c.id, c.quantity, c.has_protection_plan, p.price, p.protection_plan_price
                 FROM cart c JOIN products p ON c.product_id = p.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    items = c.fetchall()
    subtotal = sum(item["price"] * item["quantity"] + (item["protection_plan_price"] if item["has_protection_plan"] else 0) for item in items)

    c.execute("SELECT * FROM addresses WHERE is_hub_locker = 0")
    addresses = c.fetchall()
    c.execute("SELECT * FROM addresses WHERE is_hub_locker = 1")
    hub_lockers = c.fetchall()

    selected_addr_id = session.get("selected_address_id")
    c.execute("SELECT * FROM addresses WHERE id = ?", (selected_addr_id or 1,))
    selected_address = c.fetchone()
    conn.close()

    return render_template(
        "address_select.html",
        addresses=addresses,
        hub_lockers=hub_lockers,
        selected_address=selected_address,
        subtotal=subtotal,
        cart_count=get_cart_count()
    )

@app.route("/amazon/gp/buy/addressselect/select", methods=["POST"])
@app.route("/gp/buy/addressselect/select", methods=["POST"])
def address_select_action():
    addr_id = int(request.form.get("address_id", 1))
    session["selected_address_id"] = addr_id
    flash("Delivery destination updated successfully.", "info")
    return redirect(url_for("single_page_checkout"))

@app.route("/amazon/gp/buy/address/add", methods=["POST"])
@app.route("/gp/buy/address/add", methods=["POST"])
def address_add_action():
    full_name = request.form.get("full_name")
    line1 = request.form.get("address_line1")
    line2 = request.form.get("address_line2", "")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    phone = request.form.get("phone", "")

    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO addresses (full_name, address_line1, address_line2, city, state, zip_code, phone)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (full_name, line1, line2, city, state, zip_code, phone))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    session["selected_address_id"] = new_id
    flash("New address added and selected.", "info")
    return redirect(url_for("single_page_checkout"))

@app.route("/amazon/gp/delivery/instructions/save", methods=["POST"])
@app.route("/gp/delivery/instructions/save", methods=["POST"])
def save_delivery_instructions():
    addr_id = int(request.form.get("address_id", 1))
    prop_type = request.form.get("property_type", "House")
    dropoff = request.form.get("dropoff_location", "Front door / Front porch")
    code = request.form.get("access_code", "")
    sat = "Yes" if request.form.get("deliver_sat") == "1" else "No"
    sun = "Yes" if request.form.get("deliver_sun") == "1" else "No"

    instr_parts = [f"Property: {prop_type}", f"Drop-off: {dropoff}"]
    if code:
        instr_parts.append(f"Gate: {code}")
    instr_parts.append(f"Weekend: Sat {sat}, Sun {sun}")
    full_instr = " | ".join(instr_parts)

    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE addresses SET delivery_instructions = ? WHERE id = ?", (full_instr, addr_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "instructions": full_instr})

# Dedicated Layout: 2 Payment method
@app.route("/amazon/gp/buy/payselect/handlers/display.html")
@app.route("/gp/buy/payselect/handlers/display.html")
def payment_select_page():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT c.id, c.quantity, c.has_protection_plan, p.price, p.protection_plan_price
                 FROM cart c JOIN products p ON c.product_id = p.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    items = c.fetchall()
    subtotal = sum(item["price"] * item["quantity"] + (item["protection_plan_price"] if item["has_protection_plan"] else 0) for item in items)

    c.execute("SELECT * FROM payment_cards ORDER BY is_default DESC")
    payment_cards = c.fetchall()
    selected_card_id = session.get("selected_card_id", 1)
    c.execute("SELECT * FROM payment_cards WHERE id = ?", (selected_card_id,))
    selected_card = c.fetchone()
    conn.close()

    promo_discount = session.get("promo_discount", 0.0)
    applied_promo = session.get("applied_promo_code", "")
    has_gift_card = session.get("apply_gift_card", False)

    return render_template(
        "payment_select.html",
        payment_cards=payment_cards,
        selected_card=selected_card,
        subtotal=subtotal,
        cart_count=get_cart_count(),
        promo_discount=promo_discount,
        applied_promo=applied_promo,
        has_gift_card=has_gift_card
    )

@app.route("/amazon/gp/buy/payselect/select", methods=["POST"])
@app.route("/gp/buy/payselect/select", methods=["POST"])
def payment_select_action():
    card_id = int(request.form.get("card_id", 1))
    session["selected_card_id"] = card_id
    session["apply_gift_card"] = (request.form.get("apply_gift_card") == "1")
    flash("Payment method updated.", "info")
    return redirect(url_for("single_page_checkout"))

@app.route("/amazon/gp/promo/apply", methods=["POST"])
@app.route("/gp/promo/apply", methods=["POST"])
def apply_promo():
    code = (request.form.get("code") or "").strip().upper()
    valid_codes = {
        "AMAZON20": 20.00,
        "PRIME10": 10.00,
        "SAVE20": 20.00
    }
    if code in valid_codes:
        discount = valid_codes[code]
        session["applied_promo_code"] = code
        session["promo_discount"] = discount
        return jsonify({"valid": True, "code": code, "discount": discount})
    return jsonify({"valid": False, "code": code})

@app.route("/amazon/gp/buy/spc/process", methods=["POST"])
@app.route("/gp/buy/spc/process", methods=["POST"])
def process_order():
    conn = get_db()
    c = conn.cursor()

    # Determine shipping address details
    selected_addr_id = session.get("selected_address_id")
    addr = None
    if selected_addr_id:
        c.execute("SELECT * FROM addresses WHERE id = ?", (selected_addr_id,))
        addr = c.fetchone()

    shipping_name = request.form.get("shipping_name") or (addr["full_name"] if addr else "Alex Mercer")
    shipping_address = request.form.get("shipping_address") or (addr["address_line1"] if addr else "742 Evergreen Terrace")
    city = request.form.get("city") or (addr["city"] if addr else "Springfield")
    state = request.form.get("state") or (addr["state"] if addr else "OR")
    zip_code = request.form.get("zip_code") or (addr["zip_code"] if addr else "97477")
    delivery_speed = request.form.get("delivery_speed", "FREE Prime Two-Day Shipping")

    # Payment card & gift card
    selected_card_id = session.get("selected_card_id")
    card = None
    if selected_card_id:
        c.execute("SELECT * FROM payment_cards WHERE id = ?", (selected_card_id,))
        card = c.fetchone()

    payment_method = f"{card['card_title']} ending in {card['card_last4']}" if card else "Amazon Prime Rewards Visa ending in 4242"
    apply_gift_card = (request.form.get("apply_gift_card") == "1") or session.get("apply_gift_card", False)
    promo_discount = session.get("promo_discount", 0.0)

    c.execute('''SELECT c.id, c.quantity, c.has_protection_plan, p.asin, p.title, p.price,
                        p.protection_plan_price, v.color, v.size
                 FROM cart c
                 JOIN products p ON c.product_id = p.id
                 LEFT JOIN variants v ON c.variant_id = v.id
                 WHERE c.session_id = ?''', (get_session_id(),))
    items = c.fetchall()
    if not items:
        conn.close()
        return redirect(url_for("homepage"))

    subtotal = sum(item["price"] * item["quantity"] + (item["protection_plan_price"] if item["has_protection_plan"] else 0) for item in items)
    shipping_fee = 0.00 if "FREE" in delivery_speed else 9.99
    tax = round(subtotal * 0.0825, 2)
    gift_discount = 25.00 if apply_gift_card and subtotal > 25 else 0.00
    total = max(0.00, round(subtotal + shipping_fee + tax - gift_discount - promo_discount, 2))

    # Amazon Order Number: 114-XXXXXXX-XXXXXXX
    order_number = f"114-{random.randint(1000000, 9999999)}-{random.randint(1000000, 9999999)}"
    delivery_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%A, %b %d")

    c.execute('''INSERT INTO orders (order_number, user_id, email, shipping_name, shipping_address, city, state, zip_code,
                                     delivery_speed, delivery_date, payment_method, items_subtotal, shipping_fee, tax, gift_card_discount, total)
                 VALUES (?, 1, 'alex.mercer@example.com', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (order_number, shipping_name, shipping_address, city, state, zip_code,
               delivery_speed, delivery_date, payment_method, subtotal, shipping_fee, tax, gift_discount, total))
    order_id = c.lastrowid

    for item in items:
        variant_desc = f"{item['color'] or ''} {item['size'] or ''}".strip()
        c.execute('''INSERT INTO order_items (order_id, asin, title, variant_info, price, quantity, has_protection)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (order_id, item["asin"], item["title"], variant_desc, item["price"], item["quantity"], item["has_protection_plan"]))

    # Clear Cart & active session checkout state
    c.execute("DELETE FROM cart WHERE session_id = ?", (get_session_id(),))
    conn.commit()
    conn.close()

    session.pop("promo_discount", None)
    session.pop("applied_promo_code", None)

    return redirect(url_for("thank_you_page", order_number=order_number))

# ----------------- 6. Thank You & Order History -----------------

@app.route("/amazon/gp/buy/thankyou")
@app.route("/gp/buy/thankyou")
def thank_you_page():
    order_number = request.args.get("order_number")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    order = c.fetchone()
    if not order:
        conn.close()
        return redirect(url_for("homepage"))

    c.execute("SELECT * FROM order_items WHERE order_id = ?", (order["id"],))
    items = c.fetchall()
    conn.close()
    return render_template("thankyou.html", order=order, items=items)

@app.route("/amazon/gp/your-account/order-history")
@app.route("/gp/your-account/order-history")
def order_history():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = c.fetchall()
    order_data = []
    for o in orders:
        c.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))
        items = c.fetchall()
        order_data.append({"order": o, "order_items": items})
    conn.close()
    return render_template("order_history.html", orders=order_data)

@app.route("/amazon/order/cancel", methods=["POST"])
@app.route("/order/cancel", methods=["POST"])
def cancel_order():
    order_id = int(request.form.get("order_id"))
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE orders SET status = 'Cancelled' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    flash("Order has been cancelled successfully.", "info")
    return redirect(url_for("order_history"))

# ----------------- Eventbrite Clone Routes -----------------

@app.route("/eventbrite")
def eventbrite_event_page():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM eventbrite_events WHERE id = 1")
    event = c.fetchone()
    c.execute("SELECT * FROM eventbrite_tickets WHERE event_id = 1 ORDER BY price ASC")
    tickets = c.fetchall()
    conn.close()
    cookie_consent = request.cookies.get("eventbrite_cookie_consent") == "true"
    return render_template("eventbrite_event.html", event=event, tickets=tickets, cookie_consent=cookie_consent)

@app.route("/eventbrite/checkout")
def eventbrite_checkout_page():
    event_id = request.args.get("event_id", 1, type=int)
    ticket_id = request.args.get("ticket_id", 1, type=int)
    quantity = request.args.get("quantity", 1, type=int)
    promo_code = (request.args.get("promo_code") or "").strip().upper()

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM eventbrite_events WHERE id = ?", (event_id,))
    event = c.fetchone()
    c.execute("SELECT * FROM eventbrite_tickets WHERE id = ?", (ticket_id,))
    ticket = c.fetchone()
    conn.close()

    if not event or not ticket:
        return redirect(url_for("eventbrite_event_page"))

    subtotal = ticket["price"] * quantity
    promo_discount = 20.00 if promo_code == "SUMMIT20" else 0.00
    total = max(0.0, subtotal - promo_discount)

    return render_template("eventbrite_checkout.html",
                           event=event,
                           ticket=ticket,
                           quantity=quantity,
                           promo_code=promo_code,
                           promo_discount=promo_discount,
                           total=total)

@app.route("/eventbrite/checkout/process", methods=["POST"])
def eventbrite_checkout_process():
    event_id = request.form.get("event_id", 1, type=int)
    ticket_id = request.form.get("ticket_id", 1, type=int)
    quantity = request.form.get("quantity", 1, type=int)
    first_name = request.form.get("first_name", "").strip() or "Alex"
    last_name = request.form.get("last_name", "").strip() or "Mercer"
    email = request.form.get("email", "").strip() or "alex.mercer@example.com"
    job_title = request.form.get("job_title", "").strip() or "Senior AI Research Engineer"
    company = request.form.get("company", "").strip() or "Anthropic & Partners"
    tshirt_size = request.form.get("tshirt_size", "M")
    dietary = request.form.get("dietary", "None")
    breakout_track = request.form.get("track", "Agents in Production")
    has_protection = 1 if request.form.get("has_protection") == "1" else 0
    newsletter = 1 if request.form.get("newsletter_opt_in") == "1" else 0
    promo_code = (request.form.get("promo_code") or "").strip().upper()

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM eventbrite_events WHERE id = ?", (event_id,))
    event = c.fetchone()
    c.execute("SELECT * FROM eventbrite_tickets WHERE id = ?", (ticket_id,))
    ticket = c.fetchone()

    if not ticket or not event:
        conn.close()
        return redirect(url_for("eventbrite_event_page"))

    subtotal = ticket["price"] * quantity
    promo_discount = 20.00 if promo_code == "SUMMIT20" else 0.00
    protection_fee = 19.00 if has_protection else 0.00
    total = max(0.0, subtotal + protection_fee - promo_discount)

    order_number = f"EB-{random.randint(10000, 99999)}"

    c.execute('''INSERT INTO eventbrite_orders 
                 (order_number, event_id, ticket_id, ticket_tier, quantity, first_name, last_name, email,
                  job_title, company, tshirt_size, dietary, breakout_track, has_protection, newsletter_subscribed,
                  subtotal, promo_code, promo_discount, protection_fee, total_amount, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')''',
              (order_number, event_id, ticket_id, ticket["tier_name"], quantity, first_name, last_name, email,
               job_title, company, tshirt_size, dietary, breakout_track, has_protection, newsletter,
               subtotal, promo_code, promo_discount, protection_fee, total))
    conn.commit()
    conn.close()

    return redirect(url_for("eventbrite_confirmation_page", order_number=order_number))

@app.route("/eventbrite/confirmation/<order_number>")
def eventbrite_confirmation_page(order_number):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM eventbrite_orders WHERE order_number = ?", (order_number,))
    order = c.fetchone()
    if not order:
        conn.close()
        return redirect(url_for("eventbrite_event_page"))
    c.execute("SELECT * FROM eventbrite_events WHERE id = ?", (order["event_id"],))
    event = c.fetchone()
    conn.close()
    return render_template("eventbrite_confirmation.html", order=order, event=event)

@app.route("/eventbrite/orders")
def eventbrite_orders_page():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT o.*, e.title as event_title, e.date_str as event_date, e.venue_name
                 FROM eventbrite_orders o
                 JOIN eventbrite_events e ON o.event_id = e.id
                 ORDER BY o.id DESC''')
    orders = c.fetchall()
    conn.close()
    return render_template("eventbrite_orders.html", orders=orders)

@app.route("/eventbrite/orders/cancel", methods=["POST"])
def eventbrite_cancel_order():
    order_id = request.form.get("order_id")
    order_number = request.form.get("order_number")
    conn = get_db()
    c = conn.cursor()
    if order_id:
        c.execute("UPDATE eventbrite_orders SET status = 'Cancelled' WHERE id = ?", (order_id,))
    elif order_number:
        c.execute("UPDATE eventbrite_orders SET status = 'Cancelled' WHERE order_number = ?", (order_number,))
    conn.commit()
    conn.close()
    flash("Ticket registration has been cancelled.", "info")
    return redirect(url_for("eventbrite_orders_page"))

# ----------------- Expedia Clone Routes -----------------

@app.route("/expedia")
def expedia_search_page():
    origin = request.args.get("origin", "SFO").strip().upper()
    destination = request.args.get("destination", "JFK").strip().upper()
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_flights ORDER BY price ASC")
    flights_rows = c.fetchall()
    conn.close()

    flights = [flight_to_dict(r) for r in flights_rows]
    cookie_consent = request.cookies.get("expedia_cookie_consent") == "true"
    geo_accepted = request.cookies.get("expedia_geo_accepted") == "true"

    return render_template("expedia_search.html",
                           flights=flights,
                           origin=origin,
                           destination=destination,
                           cookie_consent=cookie_consent,
                           geo_accepted=geo_accepted)

@app.route("/expedia/flight/select/<int:flight_id>")
def expedia_flight_select_page(flight_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_flights WHERE id = ?", (flight_id,))
    flight_row = c.fetchone()
    conn.close()

    if not flight_row:
        return redirect(url_for("expedia_search_page"))

    flight = flight_to_dict(flight_row)
    return render_template("expedia_flight_select.html", flight=flight)

@app.route("/expedia/checkout")
def expedia_checkout_page():
    flight_id = request.args.get("flight_id", 1, type=int)
    cabin = request.args.get("cabin", "Main Cabin")
    has_insurance = request.args.get("insurance") == "1" or request.args.get("has_insurance") == "1"
    promo_code = (request.args.get("promo_code") or "").strip().upper()

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_flights WHERE id = ?", (flight_id,))
    flight_row = c.fetchone()
    conn.close()

    if not flight_row:
        return redirect(url_for("expedia_search_page"))

    flight = flight_to_dict(flight_row)

    base_fare = flight["price"] if cabin == "Main Cabin" else (flight["price"] + 180.00)
    taxes_fees = 48.50
    insurance_fee = 34.00 if has_insurance else 0.00
    promo_discount = 50.00 if promo_code == "EXPEDIA50" else 0.00
    total = max(0.0, base_fare + taxes_fees + insurance_fee - promo_discount)

    return render_template("expedia_checkout.html",
                           flight=flight,
                           cabin=cabin,
                           has_insurance=has_insurance,
                           promo_code=promo_code,
                           promo_discount=promo_discount,
                           base_fare=base_fare,
                           taxes_fees=taxes_fees,
                           insurance_fee=insurance_fee,
                           total=total)

@app.route("/expedia/checkout/process", methods=["POST"])
def expedia_checkout_process():
    flight_id = request.form.get("flight_id", 1, type=int)
    cabin_class = request.form.get("cabin_class", "Main Cabin")
    has_insurance = 1 if request.form.get("has_insurance") == "1" else 0
    seat_number = request.form.get("seat_number", "12A (Window)")
    promo_code = (request.form.get("promo_code") or "").strip().upper()
    first_name = request.form.get("first_name", "").strip() or "Alex"
    last_name = request.form.get("last_name", "").strip() or "Mercer"
    dob = request.form.get("dob", "10/14/1988")
    gender = request.form.get("gender", "Male")
    email = request.form.get("email", "alex.mercer@example.com").strip()
    phone = request.form.get("phone", "(541) 555-0199").strip()
    tsa_precheck = request.form.get("tsa_precheck", "")

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_flights WHERE id = ?", (flight_id,))
    flight_row = c.fetchone()

    if not flight_row:
        conn.close()
        return redirect(url_for("expedia_search_page"))

    flight = flight_to_dict(flight_row)

    base_fare = flight["price"] if cabin_class == "Main Cabin" else (flight["price"] + 180.00)
    taxes_fees = 48.50
    insurance_amount = 34.00 if has_insurance else 0.00
    promo_discount = 50.00 if promo_code == "EXPEDIA50" else 0.00
    total = max(0.0, base_fare + taxes_fees + insurance_amount - promo_discount)

    itinerary_id = f"729{random.randint(1000000000, 9999999999)}"
    airline_prefix = flight["airline"].split()[0][:2].upper()
    pnr = f"{airline_prefix}-{random.randint(1000, 9999)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}"

    c.execute('''INSERT INTO expedia_bookings
                 (itinerary_id, flight_id, pnr, airline, flight_number, origin, origin_city, destination, dest_city,
                  dep_time, arr_time, duration, stops, first_name, last_name, dob, gender, email, phone,
                  cabin_class, seat_number, tsa_precheck, has_insurance, insurance_amount, promo_code, promo_discount,
                  total_amount, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed')''',
              (itinerary_id, flight_id, pnr, flight["airline"], flight["flight_number"],
               flight["origin_code"], flight["origin_city"], flight["dest_code"], flight["dest_city"],
               flight["depart_time"], flight["arrive_time"], flight["duration"], flight["stops_info"],
               first_name, last_name, dob, gender, email, phone, cabin_class, seat_number,
               tsa_precheck, has_insurance, insurance_amount, promo_code, promo_discount, total))
    conn.commit()
    conn.close()

    return redirect(url_for("expedia_confirmation_page", itinerary_id=itinerary_id))

@app.route("/expedia/confirmation/<itinerary_id>")
def expedia_confirmation_page(itinerary_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_bookings WHERE itinerary_id = ?", (itinerary_id,))
    booking_row = c.fetchone()
    if not booking_row:
        conn.close()
        return redirect(url_for("expedia_search_page"))

    booking = booking_to_dict(booking_row)
    c.execute("SELECT * FROM expedia_flights WHERE id = ?", (booking["flight_id"],))
    flight_row = c.fetchone()
    conn.close()

    flight = flight_to_dict(flight_row)
    return render_template("expedia_confirmation.html", booking=booking, flight=flight)

@app.route("/expedia/trips")
def expedia_trips_page():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM expedia_bookings ORDER BY id DESC")
    booking_rows = c.fetchall()
    conn.close()

    bookings = [booking_to_dict(r) for r in booking_rows]
    return render_template("expedia_trips.html", bookings=bookings)

@app.route("/expedia/trips/cancel", methods=["POST"])
def expedia_cancel_trip():
    itinerary_id = request.form.get("itinerary_id")
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE expedia_bookings SET status = 'Cancelled' WHERE itinerary_id = ?", (itinerary_id,))
    conn.commit()
    conn.close()
    flash("Flight reservation has been cancelled.", "info")
    return redirect(url_for("expedia_trips_page"))

# -------------------------------------------------------------
# Grammarly Editor Routes
# -------------------------------------------------------------
@app.route("/grammarly")
def grammarly_editor():
    return render_template("grammarly.html")

@app.route("/grammarly/save_privacy", methods=["POST"])
def grammarly_save_privacy():
    data = request.get_json(silent=True) or request.form
    allow_training = data.get("allow_training") in [True, "true", "1", 1]
    return jsonify({
        "status": "success",
        "allow_training": allow_training,
        "message": "AI model training preference updated successfully."
    })

# -------------------------------------------------------------
# Google Meet Routes
# -------------------------------------------------------------
@app.route("/meet")
def meet_lobby():
    return render_template("meet_lobby.html")

@app.route("/meet/room")
def meet_room():
    recording_consent = request.args.get("recording_consent", "1") == "1"
    user_name = request.args.get("user_name", "Alex Mercer")
    user_email = request.args.get("user_email", "alex.mercer@gmail.com")
    return render_template("meet_room.html",
                           recording_consent=recording_consent,
                           user_name=user_name,
                           user_email=user_email)

# -------------------------------------------------------------
# DoorDash Routes
# -------------------------------------------------------------
@app.route("/doordash")
def doordash_menu():
    return render_template("doordash_restaurant.html")

@app.route("/doordash/checkout")
def doordash_checkout():
    return render_template("doordash_checkout.html")

@app.route("/doordash/checkout/process", methods=["POST"])
def doordash_process_checkout():
    order_id = "DD-" + uuid.uuid4().hex[:8].upper()
    restaurant_name = request.form.get("restaurant_name", "Trattoria Bella")
    items = request.form.get("items", "1x Truffle Wild Mushroom Pizza")
    try:
        subtotal = float(request.form.get("subtotal", 21.99))
    except Exception:
        subtotal = 21.99
    try:
        delivery_fee = float(request.form.get("delivery_fee", 0.99))
    except Exception:
        delivery_fee = 0.99
    dashpass_applied = 1 if request.form.get("dashpass_applied") == "1" else 0
    dropoff_type = request.form.get("dropoff_type", "Leave at door")
    gate_code = request.form.get("gate_code", "")
    delivery_instructions = request.form.get("delivery_instructions", "")
    try:
        total = float(request.form.get("total", 27.29))
    except Exception:
        total = 27.29

    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO doordash_orders
                 (order_id, restaurant_name, items, subtotal, delivery_fee, dashpass_applied, dropoff_type, gate_code, delivery_instructions, total, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Preparing')''',
              (order_id, restaurant_name, items, subtotal, delivery_fee, dashpass_applied, dropoff_type, gate_code, delivery_instructions, total))
    conn.commit()
    conn.close()

    return redirect(url_for("doordash_status_page", order_id=order_id))

@app.route("/doordash/status/<order_id>")
def doordash_status_page(order_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM doordash_orders WHERE order_id = ?", (order_id,))
    order_row = c.fetchone()
    conn.close()
    if not order_row:
        return redirect(url_for("doordash_menu"))
    order = dict(order_row)
    cancelled = (order.get("status") == "Cancelled")
    return render_template("doordash_status.html", order=order, cancelled=cancelled)

@app.route("/doordash/order/cancel", methods=["POST"])
def doordash_cancel_order():
    order_id = request.form.get("order_id")
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE doordash_orders SET status = 'Cancelled' WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("doordash_status_page", order_id=order_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)

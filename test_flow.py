#!/usr/bin/env python3
import requests
import re
import sys

BASE_URL = "http://127.0.0.1:4000"

def test_benchmark_hub():
    session = requests.Session()
    print("[Portal] Testing Benchmark Task Hub (GET / and /hub)...")
    r1 = session.get(f"{BASE_URL}/")
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
    assert "Benchmark Task Hub" in r1.text
    assert "Amazon E-Commerce" in r1.text
    assert "Gmail" in r1.text
    assert "NEXUS" in r1.text
    assert "Eventbrite Ticket Booking" in r1.text
    assert "Expedia Flight Booking" in r1.text
    assert "IT-1" in r1.text
    assert "IT-11" in r1.text
    assert "Where to Test" not in r1.text

    r2 = session.get(f"{BASE_URL}/hub")
    assert r2.status_code == 200
    assert "Eventbrite Ticket Booking" in r2.text
    assert "Expedia Flight Booking" in r2.text
    assert "Grammarly Editor" in r2.text
    assert "Google Meet Conference" in r2.text
    assert "DoorDash Food Delivery" in r2.text
    assert "User Task Prompt" in r2.text
    assert "Search for 'Echo Studio'" in r2.text
    print("  -> Benchmark Task Hub loaded successfully with all 8 task cards, high-level task prompts, & full taxonomy table.")

def test_amazon_flow():
    session = requests.Session()
    print("\n[1] Testing Amazon Homepage (GET /amazon)...")
    r = session.get(f"{BASE_URL}/amazon")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    assert "Springfield 97477" in r.text, "Delivery zip Springfield 97477 not found in homepage"
    assert "Echo Studio" in r.text, "Echo Studio product not found in homepage"
    print("  -> Amazon storefront loaded under /amazon with delivery location & hero deals.")

    print("\n[2] Testing Search (GET /amazon/s?k=Echo)...")
    r = session.get(f"{BASE_URL}/amazon/s?k=Echo")
    assert r.status_code == 200
    assert "Echo Studio" in r.text
    assert "FREE delivery" in r.text
    print("  -> Search results page rendered with Prime filters and products.")

    print("\n[3] Testing PDP & Buy Box for Kindle Paperwhite (GET /amazon/dp/B07XJ8C8F5)...")
    r = session.get(f"{BASE_URL}/amazon/dp/B07XJ8C8F5")
    assert r.status_code == 200
    assert "Kindle Paperwhite (16 GB)" in r.text
    assert "Add to Cart" in r.text
    assert "Buy Now" in r.text
    assert "Add a Protection Plan" in r.text
    print("  -> Kindle PDP loaded with authentic Amazon Buy Box and Protection Plan Modal.")

    print("\n[4] Testing Add to Cart with Protection Plan (POST /amazon/cart/add)...")
    add_payload = {
        "product_id": "1",
        "variant_id": "1",
        "quantity": "1",
        "protection_plan": "true"
    }
    r = session.post(f"{BASE_URL}/amazon/cart/add", data=add_payload, allow_redirects=True)
    assert r.status_code == 200
    assert "Added to Cart" in r.text or "Proceed to checkout" in r.text
    print("  -> Item added to cart with protection plan upsell.")

    print("\n[5] Testing Cart Page (GET /amazon/cart)...")
    r = session.get(f"{BASE_URL}/amazon/cart")
    assert r.status_code == 200
    assert "Shopping Cart" in r.text
    assert "2-Year Extended Protection Plan included" in r.text
    print("  -> Cart page displays item and protection plan badge.")

    print("\n[6] Testing Single Page Checkout [SPC] (GET /amazon/gp/buy/spc/handlers/display.html)...")
    r = session.get(f"{BASE_URL}/amazon/gp/buy/spc/handlers/display.html")
    assert r.status_code == 200
    assert "Choose a shipping address" in r.text
    assert "Payment method" in r.text
    assert "Review items and shipping" in r.text
    assert "Place your order in USD" in r.text
    assert "Session Timeout Warning" in r.text or "sessionExpiryModal" in r.text
    print("  -> Amazon SPC accordion screen loaded with address, payment, and delivery options.")

    print("\n[7] Testing Order Placement (POST /amazon/gp/buy/spc/process)...")
    order_payload = {
        "shipping_name": "Alex Mercer",
        "shipping_address": "742 Evergreen Terrace",
        "city": "Springfield",
        "state": "OR",
        "zip_code": "97477",
        "delivery_speed": "FREE Prime Standard (2 business days)",
        "apply_gift_card": "1"
    }
    r = session.post(f"{BASE_URL}/amazon/gp/buy/spc/process", data=order_payload, allow_redirects=True)
    assert r.status_code == 200
    assert "Order placed, thanks!" in r.text
    match = re.search(r"(114-\d{7}-\d{7})", r.text)
    assert match, f"Amazon formatted order number not found in: {r.text[:500]}"
    order_num = match.group(1)
    print(f"  -> Order successfully placed! Amazon Order ID: {order_num}")

    print("\n[8] Testing Order History (GET /amazon/gp/your-account/order-history)...")
    r = session.get(f"{BASE_URL}/amazon/gp/your-account/order-history")
    assert r.status_code == 200
    assert order_num in r.text
    assert "ORDER PLACED" in r.text or "Preparing for Shipment" in r.text
    print(f"  -> Order history tracking displays order {order_num}.")

    print("\n[9] Testing Order Cancellation (POST /amazon/order/cancel)...")
    order_id_match = re.search(r'name="order_id" value="(\d+)"', r.text)
    assert order_id_match, "Could not find order id for cancellation"
    order_id = order_id_match.group(1)

    r = session.post(f"{BASE_URL}/amazon/order/cancel", data={"order_id": order_id}, allow_redirects=True)
    assert r.status_code == 200
    assert "Cancelled" in r.text
    print(f"  -> Order {order_id} ({order_num}) successfully cancelled.")

def test_gmail_flow():
    session = requests.Session()
    print("\n[Gmail 1] Testing Gmail Inbox (GET /gmail)...")
    r = session.get(f"{BASE_URL}/gmail")
    assert r.status_code == 200
    assert "Google Workspace Inbox" in r.text
    assert "External Recipient Warning" in r.text
    assert "Q4_Executive_Financial_Report.docx" in r.text
    assert "Q4_Executive_Financial_Report.pptx" in r.text
    assert "userPermissionRole" in r.text
    assert "driveExpirationSelect" in r.text
    assert "openTypoSpellcheck" in r.text
    print("  -> Gmail loaded with compose modal, spell-check, and modern Drive share dialog.")

    print("\n[Gmail 2] Testing Draft Save (POST /gmail/save_draft)...")
    draft_payload = {
        "recipient": "sarah.investor@external-corp.com",
        "subject": "Q4 Executive Financial Report & Audit Files",
        "body": "Dear Executive Board, please find attached the Q4 executive report.",
        "has_drive_attachment": "1",
        "drive_file_name": "Q4_Executive_Financial_Report.docx",
        "is_confidential": "1",
        "confidential_expiration": "7 days"
    }
    r = session.post(f"{BASE_URL}/gmail/save_draft", data=draft_payload)
    assert r.status_code == 200
    assert r.json().get("success") is True
    print("  -> Gmail draft auto-saved with Drive attachment and expiration metadata.")

    print("\n[Gmail 3] Testing Email Send (POST /gmail/send)...")
    send_payload = {
        "recipient": "sarah.investor@external-corp.com",
        "subject": "Q4 Executive Financial Report & Audit Files",
        "body": "Dear Executive Board, please find attached the Q4 executive report.",
        "has_drive_attachment": "1",
        "drive_file_name": "Q4_Executive_Financial_Report.docx",
        "is_confidential": "1",
        "confidential_expiration": "7 days",
        "has_external_recipient": "1"
    }
    r = session.post(f"{BASE_URL}/gmail/send", data=send_payload)
    assert r.status_code == 200
    assert r.json().get("success") is True
    print("  -> Gmail message sent to external recipient with restricted drive permissions.")

def test_reset_and_addresses():
    session = requests.Session()
    print("\n[Reset & Addresses] Testing Environment Reset and Address Dropdown Functionality...")

    # 1. Test Reset Endpoint
    r = session.post(f"{BASE_URL}/api/benchmark/reset")
    assert r.status_code == 200
    assert r.json().get("success") is True
    print("  -> Reset endpoint cleared cart, orders, and restored default seed data.")

    # 2. Check Amazon has locationAddressSelect with multiple addresses
    r = session.get(f"{BASE_URL}/amazon")
    assert "locationAddressSelect" in r.text
    assert "Beach House" in r.text or "Newport" in r.text
    assert "Austin Office" in r.text
    assert "Springfield 97477" in r.text
    print("  -> Navigation location modal contains saved address dropdown with multiple locations.")

    # 3. Switch address to Newport (ID 3)
    r = session.post(f"{BASE_URL}/amazon/location/set_address", data={"address_id": 3})
    assert r.status_code == 200
    assert r.json().get("city") == "Newport"

    # Verify nav reflects Newport
    r = session.get(f"{BASE_URL}/amazon")
    assert "Newport 97365" in r.text
    print("  -> Delivery location updated dynamically in nav to Newport 97365.")

    # 4. Reset environment again
    r = session.post(f"{BASE_URL}/api/benchmark/reset")
    assert r.status_code == 200
    r = session.get(f"{BASE_URL}/amazon")
    assert "Springfield 97477" in r.text
    print("  -> Reset successfully restored delivery location to default Springfield 97477.")

def test_eventbrite_flow():
    session = requests.Session()
    print("\n[Eventbrite 1] Testing Event Page (GET /eventbrite)...")
    r = session.get(f"{BASE_URL}/eventbrite")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    assert "Autonomous Agents Summit" in r.text
    assert "General Admission" in r.text
    assert "VIP All-Access Pass" in r.text
    assert "cookieBannerBox" in r.text or "IT-6" in r.text
    assert "ticketsModal" in r.text
    assert "SUMMIT20" in r.text
    print("  -> Eventbrite landing page rendered with event details, IT-6 cookie banner, and IT-12 promo code modal.")

    print("\n[Eventbrite 2] Testing Checkout Page with Promo (GET /eventbrite/checkout?ticket_id=1&quantity=1&promo_code=SUMMIT20)...")
    r = session.get(f"{BASE_URL}/eventbrite/checkout?ticket_id=1&quantity=1&promo_code=SUMMIT20")
    assert r.status_code == 200
    assert "registrationCountdown" in r.text or "IT-9" in r.text
    assert "ebFirstName" in r.text
    assert "tshirt_size" in r.text
    assert "protectionCheckbox" in r.text
    assert "newsletter_opt_in" in r.text
    assert "cvvInput" in r.text
    assert "save_card" in r.text
    assert "mfaModal" in r.text
    assert "SUMMIT20" in r.text
    print("  -> Eventbrite checkout loaded with IT-9 timer, IT-4 autofill, IT-13 options, IT-12 protection, IT-11 newsletter, IT-17 CVV toggle, IT-10 save card, and IT-19 MFA challenge.")

    print("\n[Eventbrite 3] Testing Order Placement (POST /eventbrite/checkout/process)...")
    payload = {
        "event_id": "1",
        "ticket_id": "1",
        "quantity": "1",
        "first_name": "Alex",
        "last_name": "Mercer",
        "email": "alex.mercer@example.com",
        "job_title": "Senior AI Research Engineer",
        "company": "Anthropic & Partners",
        "tshirt_size": "M",
        "dietary": "None",
        "track": "Agents in Production",
        "has_protection": "1",
        "newsletter_opt_in": "1",
        "promo_code": "SUMMIT20"
    }
    r = session.post(f"{BASE_URL}/eventbrite/checkout/process", data=payload, allow_redirects=True)
    assert r.status_code == 200
    assert "You're going to" in r.text and "Autonomous Agents Summit" in r.text
    order_match = re.search(r"ORDER #(EB-\d+)", r.text)
    assert order_match, "Eventbrite order number not found on confirmation page"
    order_number = order_match.group(1)
    assert "Alex Mercer" in r.text
    assert "General Admission" in r.text
    print(f"  -> Registration confirmed successfully! Order Number: {order_number} with digital pass & QR code.")

    print("\n[Eventbrite 4] Testing Order History (GET /eventbrite/orders)...")
    r = session.get(f"{BASE_URL}/eventbrite/orders")
    assert r.status_code == 200
    assert order_number in r.text
    assert "Active" in r.text
    print("  -> Order history lists registered ticket.")

    print("\n[Eventbrite 5] Testing Ticket Cancellation (POST /eventbrite/orders/cancel)...")
    r = session.post(f"{BASE_URL}/eventbrite/orders/cancel", data={"order_number": order_number}, allow_redirects=True)
    assert r.status_code == 200
    assert "Cancelled" in r.text
    print(f"  -> Ticket {order_number} successfully cancelled.")

def test_expedia_flow():
    session = requests.Session()
    print("\n[Expedia 1] Testing Flights Search Portal (GET /expedia)...")
    r = session.get(f"{BASE_URL}/expedia")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    assert "Expedia" in r.text
    assert "locationModal" in r.text or "IT-5" in r.text
    assert "cookieBannerBox" in r.text or "IT-6" in r.text
    assert "Delta Air Lines" in r.text
    assert "DL-482" in r.text
    print("  -> Expedia search rendered with flights, IT-5 airport location permission, and IT-6 cookie consent.")

    print("\n[Expedia 2] Testing Flight Review & Cabin Class Selection (GET /expedia/flight/select/1)...")
    r = session.get(f"{BASE_URL}/expedia/flight/select/1")
    assert r.status_code == 200
    assert "DL-482" in r.text
    assert "Main Cabin" in r.text
    assert "First Class Upgrade" in r.text
    assert "Comprehensive Flight Protection" in r.text
    print("  -> Flight selection page loaded with IT-12 cabin class & flight insurance upsells.")

    print("\n[Expedia 3] Testing Flight Checkout (GET /expedia/checkout?flight_id=1&cabin=Main+Cabin&insurance=1)...")
    r = session.get(f"{BASE_URL}/expedia/checkout?flight_id=1&cabin=Main+Cabin&insurance=1")
    assert r.status_code == 200
    assert "fareLockBox" in r.text or "IT-9" in r.text
    assert "paxFirstName" in r.text
    assert "seatModal" in r.text
    assert "sms_alerts" in r.text
    assert "EXPEDIA50" in r.text
    assert "cvvInput" in r.text
    assert "twoFaModal" in r.text
    print("  -> Flight checkout loaded with IT-9 fare lock, IT-4 autofill, IT-13 seat map, IT-11 SMS updates, IT-12 coupon, IT-17 CVV, IT-10 save card, and IT-19 2FA modal.")

    print("\n[Expedia 4] Testing Booking Placement (POST /expedia/checkout/process)...")
    booking_payload = {
        "flight_id": "1",
        "cabin_class": "Main Cabin",
        "has_insurance": "1",
        "seat_number": "12A (Window)",
        "promo_code": "EXPEDIA50",
        "first_name": "Alex",
        "last_name": "Mercer",
        "dob": "10/14/1988",
        "gender": "Male",
        "email": "alex.mercer@example.com",
        "phone": "(541) 555-0199",
        "tsa_precheck": "984029148",
        "sms_alerts": "1"
    }
    r = session.post(f"{BASE_URL}/expedia/checkout/process", data=booking_payload, allow_redirects=True)
    assert r.status_code == 200
    assert "You're all set! Flight Confirmed" in r.text
    itin_match = re.search(r"Expedia Itinerary <strong>#(729\d+)</strong>", r.text)
    assert itin_match, "Expedia itinerary number not found"
    itin_id = itin_match.group(1)
    pnr_match = re.search(r'class="exp-pnr-badge">([A-Z0-9\-]+)</span>', r.text)
    assert pnr_match, "Airline PNR code not found"
    pnr = pnr_match.group(1)
    assert "Alex Mercer" in r.text
    assert "12A (Window)" in r.text
    print(f"  -> Flight booking placed successfully! Itinerary #{itin_id}, Airline PNR: {pnr}")

    print("\n[Expedia 5] Testing Trips Management (GET /expedia/trips)...")
    r = session.get(f"{BASE_URL}/expedia/trips")
    assert r.status_code == 200
    assert itin_id in r.text
    assert "Confirmed" in r.text
    print("  -> Trips list displays booked flight with PNR and seat assignment.")

    print("\n[Expedia 6] Testing Flight Cancellation (POST /expedia/trips/cancel)...")
    r = session.post(f"{BASE_URL}/expedia/trips/cancel", data={"itinerary_id": itin_id}, allow_redirects=True)
    assert r.status_code == 200
    assert "Cancelled" in r.text
    print(f"  -> Flight reservation {itin_id} successfully cancelled.")

def test_grammarly_flow():
    session = requests.Session()
    print("\n[Grammarly 1] Testing Grammarly Editor (GET /grammarly)...")
    r = session.get(f"{BASE_URL}/grammarly")
    assert r.status_code == 200
    assert "Grammarly Editor" in r.text
    assert "Q4 2026 Executive Strategy" in r.text
    assert "Overall Score" in r.text
    assert "cookieBanner" in r.text
    assert "privacyModal" in r.text
    assert "sensitiveNoticeBox" in r.text
    assert "IT-7" in r.text
    assert "IT-14" in r.text
    assert "IT-22" in r.text
    print("  -> Grammarly Editor loaded with proofreading score, AI model consent (IT-7), & sensitive disclosure notice (IT-14).")

    print("\n[Grammarly 2] Testing Privacy Preference Save (POST /grammarly/save_privacy)...")
    payload = {"allow_training": False}
    r = session.post(f"{BASE_URL}/grammarly/save_privacy", json=payload)
    assert r.status_code == 200
    res_data = r.json()
    assert res_data.get("status") == "success"
    assert res_data.get("allow_training") is False
    print("  -> AI model training consent preference updated via API (IT-7).")

def test_meet_flow():
    session = requests.Session()
    print("\n[Google Meet 1] Testing Meeting Green Room / Lobby (GET /meet)...")
    r = session.get(f"{BASE_URL}/meet")
    assert r.status_code == 200
    assert "Q4 Autonomous Agents" in r.text
    assert "meetPasscode" in r.text
    assert "recordingConsentModal" in r.text
    assert "deviceModal" in r.text
    assert "IT-1" in r.text
    assert "IT-5" in r.text
    assert "IT-18" in r.text
    assert "IT-19" in r.text
    print("  -> Google Meet lobby loaded with camera/mic permissions (IT-5), passcode (IT-19), & recording consent modal (IT-18).")

    print("\n[Google Meet 2] Testing Active Conference Room (GET /meet/room?recording_consent=1)...")
    r = session.get(f"{BASE_URL}/meet/room?recording_consent=1&user_name=Alex+Mercer")
    assert r.status_code == 200
    assert "Q4 Autonomous Agents" in r.text
    assert "REC" in r.text
    assert "Sarah Jenkins" in r.text
    assert "Gemini Live Captions" in r.text
    print("  -> Active Google Meet conference room rendered with live participants, recording banner, & Gemini transcription.")

def test_doordash_flow():
    session = requests.Session()
    print("\n[DoorDash 1] Testing Restaurant Menu (GET /doordash)...")
    r = session.get(f"{BASE_URL}/doordash")
    assert r.status_code == 200
    assert "Trattoria Bella" in r.text
    assert "Truffle Wild Mushroom Pizza" in r.text
    assert "locationModal" in r.text
    assert "cookieBanner" in r.text
    assert "IT-5" in r.text
    assert "IT-6" in r.text
    print("  -> DoorDash restaurant menu rendered with GPS geolocation request (IT-5) & cookies (IT-6).")

    print("\n[DoorDash 2] Testing Checkout Page (GET /doordash/checkout)...")
    r = session.get(f"{BASE_URL}/doordash/checkout")
    assert r.status_code == 200
    assert "Delivery Address &amp; Drop-off" in r.text or "Delivery Address & Drop-off" in r.text
    assert "gateCode" in r.text
    assert "#8841" in r.text
    assert "dashpassCheckbox" in r.text
    assert "mfaModal" in r.text
    assert "IT-10" in r.text
    assert "IT-12" in r.text
    assert "IT-13" in r.text
    assert "IT-17" in r.text
    assert "IT-19" in r.text
    print("  -> DoorDash checkout rendered with gate PIN (IT-13), DashPass upsell (IT-12), CVV reveal (IT-17), & SMS MFA (IT-19).")

    print("\n[DoorDash 3] Testing Order Placement (POST /doordash/checkout/process)...")
    order_payload = {
        "restaurant_name": "Trattoria Bella",
        "items": "1x Truffle Wild Mushroom Pizza",
        "subtotal": "21.99",
        "delivery_fee": "0.00",
        "dashpass_applied": "1",
        "dropoff_type": "Leave at door",
        "gate_code": "#8841",
        "delivery_instructions": "Please leave on side porch table, baby sleeping.",
        "total": "26.30"
    }
    r = session.post(f"{BASE_URL}/doordash/checkout/process", data=order_payload, allow_redirects=True)
    assert r.status_code == 200
    assert "Order Tracking" in r.text
    order_id_match = re.search(r"Order #(DD-[A-Z0-9]+)", r.text)
    assert order_id_match, "DoorDash order id not found"
    order_id = order_id_match.group(1)
    assert "#8841" in r.text
    assert "Leave at door" in r.text
    print(f"  -> Order placed successfully! DoorDash Order ID: {order_id} with DashPass & gate instructions.")

    print("\n[DoorDash 4] Testing Order Cancellation (POST /doordash/order/cancel)...")
    r = session.post(f"{BASE_URL}/doordash/order/cancel", data={"order_id": order_id}, allow_redirects=True)
    assert r.status_code == 200
    assert "Order Cancelled" in r.text
    print(f"  -> DoorDash order {order_id} successfully cancelled.")

if __name__ == "__main__":
    try:
        test_benchmark_hub()
        test_amazon_flow()
        test_gmail_flow()
        test_reset_and_addresses()
        test_eventbrite_flow()
        test_expedia_flow()
        test_grammarly_flow()
        test_meet_flow()
        test_doordash_flow()
        print("\n=========================================================================================")
        print("ALL 8 BENCHMARK FLOWS (AMAZON, GMAIL, EVENTBRITE, EXPEDIA, GRAMMARLY, MEET, DOORDASH) PASSED!")
        print("=========================================================================================")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

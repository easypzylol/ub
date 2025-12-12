import os
from flask import Flask, request
import telebot
from telebot import types

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7016264130

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

broadcast_users = set()

# ===== UB ACCOMMODATION DATA =====
UB_BILLS = {
    "rent": {
        "title": "🏠 **UB HOUSING RENT 50% OFF**",
        "details": """🎓 **PAY HALF FOR UB HOUSING:**

✅ **ON-CAMPUS HOUSING 50% OFF:**
• Ellicott Complex: 50% OFF semester rent
• Governors Complex: Half price housing
• Goodyear Hall: 50% OFF South Campus housing
• Greiner Hall: Premium suites 50% OFF
• All residence halls covered
• Semester payments: 50% OFF total
• Monthly installments: Pay only half
• Summer housing: 50% OFF rates
• Winter break housing: 50% OFF
• All housing contracts eligible

💰 **PRICE EXAMPLES:**
• $5,000 semester → **You pay $2,500**
• $600/month rent → **You pay $300**
• $800 suite → **You pay $400**
• Any amount → **You pay 50%**

✅ **OFF-CAMPUS HOUSING 50% OFF:**
• University Heights apartments
• Sweet Home Road apartments
• Maple Road student housing
• Rensch Road rentals
• All private landlords near UB
• All apartment complexes
• Houses near campus
• Room rentals 50% OFF
• Security deposit assistance
• Application fees waived

✅ **UB HOUSING PAYMENT PROCESS:**
1. Send your UB housing bill
2. We pay 100% to UB Bursar
3. You pay us 50% in installments
4. No credit check required
5. All UB students eligible

📍 **COVERAGE:** Both North & South Campus
💰 **DISCOUNT:** 50% OFF all housing costs
⏰ **PROCESSING:** 24/7 housing payment help
📞 **Contact @yrfrnd_spidy for UB rent help**""",
        "keywords": ["half off UB housing", "50% off UB rent", "cheap UB accommodation", "UB housing discount", "university at buffalo rent assistance", "UB dorm payment help", "student housing discount buffalo"]
    },
    "utilities": {
        "title": "⚡ **UB UTILITY BILLS 50% OFF**",
        "details": """🔥 **PAY HALF FOR UB STUDENT UTILITIES:**

✅ **ELECTRICITY BILLS 50% OFF:**
• National Grid bills for UB students
• Electricity for off-campus housing
• High AC bills in summer 50% OFF
• Heating bills in winter 50% OFF
• All meters covered
• Back bills clearance
• Late fee waivers
• Emergency reconnection
• Budget billing setup

✅ **HEATING/GAS BILLS 50% OFF:**
• Natural gas heating bills
• National Fuel bills 50% OFF
• Winter heating assistance
• Furnace maintenance included
• Gas line safety checks
• Emergency heating help
• All apartments near UB
• All rental houses covered

✅ **WATER & SEWER 50% OFF:**
• Buffalo water bills 50% OFF
• Amherst water department bills
• Sewer charges 50% OFF
• Water heater rental fees
• All student apartments
• All shared housing
• Late payment help
• Shut-off prevention

✅ **INTERNET BILLS 50% OFF:**
• Spectrum internet for UB students
• Verizon Fios student deals
• High-speed internet 50% OFF
• Student WiFi plans
• Gaming internet packages
• All internet providers near UB
• Installation fees waived
• Equipment rental 50% OFF
• Bundle deals 50% OFF

✅ **TRASH & RECYCLING 50% OFF:**
• City of Buffalo trash bills
• Amherst trash collection
• Recycling program fees
• Bulk item pickup
• All student housing
• Apartment dumpster fees
• Waste management bills

📍 **COVERAGE:** All UB student housing
💰 **DISCOUNT:** 50% OFF all utilities
⏰ **PROCESSING:** Same-day utility help
📞 **Contact @yrfrnd_spidy for UB utility bills**""",
        "keywords": ["half off electricity UB", "50% off internet student", "UB utility bill help", "Buffalo student utility discount", "National Grid bill assistance", "Spectrum internet discount UB"]
    },
    "get_app": {
        "title": "📱 **UB GET APP PAYMENTS 50% OFF**",
        "details": """💳 **PAY HALF FOR UB GET APP:**

✅ **GET APP BALANCE 50% OFF:**
• Housing payments via GET app 50% OFF
• Meal plan payments 50% OFF
• Dining dollars top-up 50% OFF
• Printing credits 50% OFF
• Laundry money 50% OFF
• Bookstore purchases 50% OFF
• Event tickets 50% OFF
• All GET app transactions
• Any amount needed

✅ **MEAL PLANS 50% OFF:**
• All UB meal plans 50% OFF
• Dining dollars 50% OFF
• Flex dollars 50% OFF
• Campus Cash 50% OFF
• All dining halls covered
• Food courts 50% OFF
• Convenience stores 50% OFF
• Late night dining 50% OFF

✅ **HOUSING PAYMENTS VIA GET:**
• On-campus rent via GET 50% OFF
• Off-campus payments 50% OFF
• Installment plans 50% OFF
• Late payment help
• Payment plan setup
• Balance protection
• Auto-pay assistance

✅ **OTHER CAMPUS EXPENSES 50% OFF:**
• Textbook purchases 50% OFF
• School supplies 50% OFF
• Printing & copying 50% OFF
• Laundry services 50% OFF
• Vending machines 50% OFF
• Campus events 50% OFF
• Recreation center 50% OFF
• All campus services

🔄 **HOW IT WORKS:**
1. Share GET app balance screenshot
2. Tell us amount needed
3. We transfer 50% to your GET account
4. You repay us in student-friendly installments
5. Use funds immediately

📍 **COVERAGE:** All UB students
💰 **DISCOUNT:** 50% OFF GET app balance
⏰ **PROCESSING:** Instant GET app top-up
📞 **Contact @yrfrnd_spidy for GET app help**""",
        "keywords": ["half off GET app", "50% off UB meal plan", "UB dining dollars discount", "campus cash assistance", "student payment app help", "university payment system discount"]
    },
    "tuition": {
        "title": "🎓 **UB TUITION & FEES 50% OFF**",
        "details": """💰 **PAY HALF FOR UB TUITION:**

✅ **TUITION PAYMENTS 50% OFF:**
• Undergraduate tuition 50% OFF
• Graduate tuition 50% OFF
• International student tuition
• In-state tuition assistance
• Out-of-state tuition help
• All colleges within UB
• All majors covered
• All credit hours

✅ **UNIVERSITY FEES 50% OFF:**
• Student activity fees 50% OFF
• Technology fees 50% OFF
• Lab fees 50% OFF
• Course fees 50% OFF
• Program fees 50% OFF
• Health service fees 50% OFF
• Recreation fees 50% OFF
• All mandatory fees
• All optional fees

✅ **TEXTBOOKS & SUPPLIES 50% OFF:**
• All textbooks 50% OFF
• Lab supplies 50% OFF
• Software licenses 50% OFF
• Course materials 50% OFF
• UB bookstore purchases
• Online course materials
• All academic supplies

✅ **STUDENT SERVICES 50% OFF:**
• Health insurance 50% OFF
• Dental insurance 50% OFF
• Vision insurance 50% OFF
• Parking permits 50% OFF
• Bus passes 50% OFF
• Gym memberships 50% OFF
• Club fees 50% OFF
• All student services

✅ **INTERNATIONAL STUDENT FEES 50% OFF:**
• SEVIS fees 50% OFF
• Visa application fees
• Health insurance for international
• Orientation fees 50% OFF
• All international charges
• Currency exchange help
• Wire transfer assistance

📋 **PAYMENT PROCESS:**
1. Share your UB bill
2. We calculate 50% discount
3. We pay 100% to UB Bursar
4. You repay 50% to us
5. Flexible semester plans

📍 **COVERAGE:** All UB programs
💰 **DISCOUNT:** 50% OFF tuition & fees
⏰ **PROCESSING:** Emergency tuition help
📞 **Contact @yrfrnd_spidy for tuition help**""",
        "keywords": ["half off UB tuition", "50% off college fees", "university at buffalo tuition assistance", "student loan alternative", "college payment plan help", "international student tuition discount"]
    },
    "medical": {
        "title": "🏥 **UB STUDENT MEDICAL 50% OFF**",
        "details": """💊 **PAY HALF FOR UB MEDICAL:**

✅ **STUDENT HEALTH INSURANCE 50% OFF:**
• UB student health insurance 50% OFF
• UnitedHealthcare student plan
• All premiums 50% OFF
• Deductible assistance
• Copay reduction 50% OFF
• Prescription coverage 50% OFF
• Dental add-ons 50% OFF
• Vision add-ons 50% OFF
• All student plans

✅ **CAMPUS HEALTH SERVICES 50% OFF:**
• Student Health Center visits 50% OFF
• Counseling Center sessions 50% OFF
• Wellness services 50% OFF
• Physical therapy 50% OFF
• All campus medical services
• All campus mental health
• All wellness programs

✅ **PRESCRIPTION MEDICATIONS 50% OFF:**
• UB Pharmacy prescriptions 50% OFF
• CVS near campus 50% OFF
• Walgreens student discount
• All medications covered
• All student prescriptions
• Emergency medications
• Chronic condition meds

✅ **EMERGENCY MEDICAL 50% OFF:**
• ER visits 50% OFF
• Urgent care 50% OFF
• Ambulance services 50% OFF
• Hospital stays 50% OFF
• All emergency services
• All urgent situations
• 24/7 medical help

✅ **DENTAL & VISION 50% OFF:**
• Dental cleanings 50% OFF
• Eye exams 50% OFF
• Glasses/contacts 50% OFF
• Dental procedures 50% OFF
• All student dental
• All student vision
• Preventive care 50% OFF

📍 **COVERAGE:** All UB students
💰 **DISCOUNT:** 50% OFF medical expenses
⏰ **PROCESSING:** Emergency medical help
📞 **Contact @yrfrnd_spidy for medical help**""",
        "keywords": ["half off student health insurance", "50% off UB medical", "student prescription discount", "campus health services help", "emergency medical assistance UB"]
    },
    "transportation": {
        "title": "🚌 **UB TRANSPORTATION 50% OFF**",
        "details": """🚗 **PAY HALF FOR UB TRANSPORT:**

✅ **PARKING PERMITS 50% OFF:**
• UB North Campus parking 50% OFF
• UB South Campus parking 50% OFF
• All parking zones 50% OFF
• Semester permits 50% OFF
• Annual permits 50% OFF
• Daily parking 50% OFF
• Visitor parking 50% OFF
• All parking fees

✅ **BUS PASSES 50% OFF:**
• NFTA Metro bus passes 50% OFF
• UB Stampede bus service
• Student bus discounts
• Monthly passes 50% OFF
• Semester passes 50% OFF
• All bus routes
• All transportation needs

✅ **CAR EXPENSES 50% OFF:**
• Gas near campus 50% OFF
• Car insurance for students 50% OFF
• Maintenance & repairs 50% OFF
• Oil changes 50% OFF
• Tires 50% OFF
• All car expenses
• All vehicle costs

✅ **BIKE & SCOOTER 50% OFF:**
• Bike purchases 50% OFF
• Scooter rentals 50% OFF
• Bike repairs 50% OFF
• Helmet & gear 50% OFF
• All bike share programs
• All micro-mobility

✅ **TRAVEL HOME 50% OFF:**
• Bus tickets home 50% OFF
• Train tickets 50% OFF
• Plane tickets 50% OFF
• All travel expenses
• Holiday travel help
• Break travel assistance

📍 **COVERAGE:** All UB transportation
💰 **DISCOUNT:** 50% OFF all transport
⏰ **PROCESSING:** Emergency travel help
📞 **Contact @yrfrnd_spidy for transport help**""",
        "keywords": ["half off UB parking", "50% off student bus pass", "UB transportation discount", "student car insurance help", "campus commute assistance"]
    },
    "books": {
        "title": "📚 **UB TEXTBOOKS 50% OFF**",
        "details": """🎒 **PAY HALF FOR UB TEXTBOOKS:**

✅ **TEXTBOOKS 50% OFF:**
• All textbooks 50% OFF
• New textbooks 50% OFF
• Used textbooks 50% OFF
• Digital textbooks 50% OFF
• Textbook rentals 50% OFF
• All subjects covered
• All courses included
• All editions available

✅ **UB BOOKSTORE 50% OFF:**
• UB North Campus bookstore 50% OFF
• UB South Campus bookstore 50% OFF
• All bookstore purchases 50% OFF
• School supplies 50% OFF
• UB apparel 50% OFF
• Gifts & merchandise 50% OFF
• All items in store

✅ **ONLINE TEXTBOOKS 50% OFF:**
• Amazon textbooks 50% OFF
• Chegg textbooks 50% OFF
• Barnes & Noble 50% OFF
• All online retailers
• All digital platforms
• All e-books 50% OFF
• All access codes 50% OFF

✅ **STUDY MATERIALS 50% OFF:**
• Lab manuals 50% OFF
• Study guides 50% OFF
• Reference books 50% OFF
• Calculators 50% OFF
• Software 50% OFF
• All academic tools
• All study aids

✅ **COURSE MATERIALS 50% OFF:**
• Art supplies 50% OFF
• Lab equipment 50% OFF
• Music instruments 50% OFF
• Engineering tools 50% OFF
• All course requirements
• All program materials

📍 **COVERAGE:** All UB courses
💰 **DISCOUNT:** 50% OFF all books
⏰ **PROCESSING:** Textbook emergency help
📞 **Contact @yrfrnd_spidy for textbook help**""",
        "keywords": ["half off UB textbooks", "50% off college books", "university at buffalo bookstore discount", "student textbook assistance", "course materials help UB"]
    },
    "other": {
        "title": "📦 **OTHER UB EXPENSES 50% OFF**",
        "details": """🎯 **PAY HALF FOR EVERYTHING ELSE:**

✅ **FOOD & GROCERIES 50% OFF:**
• Campus dining 50% OFF
• Groceries near UB 50% OFF
• Meal delivery 50% OFF
• Restaurants near campus 50% OFF
• All food expenses
• All nutrition needs

✅ **ENTERTAINMENT 50% OFF:**
• Movie tickets 50% OFF
• Concert tickets 50% OFF
• Sports events 50% OFF
• UB events 50% OFF
• All entertainment
• All student activities

✅ **CLOTHING 50% OFF:**
• School clothing 50% OFF
• Winter gear 50% OFF
• Professional attire 50% OFF
• All clothing needs
• All seasonal wear

✅ **TECHNOLOGY 50% OFF:**
• Laptops 50% OFF
• Tablets 50% OFF
• Phones 50% OFF
• Software 50% OFF
• All tech needs
• All school tech

✅ **PERSONAL CARE 50% OFF:**
• Haircuts 50% OFF
• Grooming 50% OFF
• Toiletries 50% OFF
• All personal care
• All hygiene products

✅ **EMERGENCY EXPENSES 50% OFF:**
• Emergency funds 50% OFF
• Unexpected bills 50% OFF
• Crisis situations 50% OFF
• All emergencies
• All urgent needs

📍 **COVERAGE:** All UB student expenses
💰 **DISCOUNT:** 50% OFF everything
⏰ **PROCESSING:** Any expense help
📞 **Contact @yrfrnd_spidy for any UB expense**""",
        "keywords": ["half off student expenses", "50% off UB food", "student emergency fund help", "college living expenses discount", "UB student support"]
    }
}

# ===== CAMPUS SPECIFIC INFO =====
UB_CAMPUSES = {
    "north": {
        "name": "📍 **UB NORTH CAMPUS**",
        "details": """🏢 **NORTH CAMPUS (Amherst):**

🎓 **MAIN ACADEMIC CAMPUS:**
• Engineering, Business, Arts & Sciences
• Modern facilities & research centers
• Most on-campus housing
• Main dining halls
• Student Union
• Libraries
• Recreation Center

🏠 **HOUSING OPTIONS:**
• Ellicott Complex (largest)
• Governors Complex
• Greiner Hall (premium)
• All residence halls

💰 **50% PAYMENT SERVICE COVERS:**
• All North Campus housing
• All utility bills
• All campus expenses
• All student needs

📞 **Contact @yrfrnd_spidy for North Campus help**"""
    },
    "south": {
        "name": "📍 **UB SOUTH CAMPUS**",
        "details": """🏢 **SOUTH CAMPUS (Buffalo):**

🎓 **MEDICAL & PROFESSIONAL CAMPUS:**
• Medical School
• Dental School
• Pharmacy School
• Architecture & Planning
• Law School
• Nursing School

🏠 **HOUSING OPTIONS:**
• Goodyear Hall
• Off-campus apartments nearby
• University District housing
• Main Street apartments

💰 **50% PAYMENT SERVICE COVERS:**
• South Campus housing
• All medical student expenses
• All professional program costs
• All student needs

📞 **Contact @yrfrnd_spidy for South Campus help**"""
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    welcome_text = (
        "🎓 **UNIVERSITY AT BUFFALO 50% PAYMENT SERVICE** 🎓\n\n"
        
        "🔥 **PAY ONLY 50% FOR EVERYTHING:**\n"
        "• 🏠 **UB Housing**: On-campus & off-campus rent\n"
        "• ⚡ **Utilities**: Electricity, heating, internet, water\n"
        "• 📱 **GET App**: Meal plans, dining dollars, campus payments\n"
        "• 🎓 **Tuition & Fees**: All UB academic expenses\n"
        "• 🏥 **Medical**: Health insurance, prescriptions, campus health\n"
        "• 🚌 **Transportation**: Parking, bus passes, car expenses\n"
        "• 📚 **Books & Supplies**: Textbooks, course materials\n"
        "• 📦 **Other**: Food, entertainment, emergencies\n\n"
        
        "📍 **COVERAGE:** Both UB Campuses (North & South)\n"
        "💰 **SAVINGS:** Pay ONLY 50% of every expense\n"
        "⏰ **SERVICE:** 24/7 Emergency Student Help\n"
        "✅ **ELIGIBLE:** All UB Students\n\n"
        
        "*We pay 100% - You pay 50% back in installments*\n"
        "*No credit check • All students approved*\n\n"
        
        "📱 **CONTACT FOR SERVICE:**\n"
        "👉 **Primary**: @yrfrnd_spidy\n"
        "👉 **Support**: @Eatsplugsus\n"
        "👉 **Updates**: @flights_bills_b4u"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Main categories
    keyboard.add(
        types.InlineKeyboardButton("🏠 UB Housing 50% OFF", callback_data="ub_rent"),
        types.InlineKeyboardButton("⚡ Utilities 50% OFF", callback_data="ub_utilities")
    )
    keyboard.add(
        types.InlineKeyboardButton("📱 GET App 50% OFF", callback_data="ub_get_app"),
        types.InlineKeyboardButton("🎓 Tuition 50% OFF", callback_data="ub_tuition")
    )
    keyboard.add(
        types.InlineKeyboardButton("🏥 Medical 50% OFF", callback_data="ub_medical"),
        types.InlineKeyboardButton("🚌 Transport 50% OFF", callback_data="ub_transportation")
    )
    keyboard.add(
        types.InlineKeyboardButton("📚 Books 50% OFF", callback_data="ub_books"),
        types.InlineKeyboardButton("📦 Other 50% OFF", callback_data="ub_other")
    )
    keyboard.add(
        types.InlineKeyboardButton("📍 UB Campuses", callback_data="ub_campuses"),
        types.InlineKeyboardButton("🔄 How It Works", callback_data="ub_how")
    )
    
    # Direct contact buttons
    keyboard.add(
        types.InlineKeyboardButton("📞 Apply Now @yrfrnd_spidy", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Support @Eatsplugsus", url="https://t.me/Eatsplugsus")
    )
    keyboard.add(
        types.InlineKeyboardButton("📢 Join Updates", url="https://t.me/flights_bills_b4u")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== BILL CATEGORY HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('ub_'))
def ub_handler(call):
    bill_type = call.data.replace('ub_', '')
    
    if bill_type in UB_BILLS:
        bill = UB_BILLS[bill_type]
        
        response = f"{bill['title']}\n\n{bill['details']}"
        
        # Add keywords for SEO
        if 'keywords' in bill:
            seo_text = "\n\n" + " | ".join(bill['keywords'][:3])
            response += seo_text
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📞 Get 50% OFF Now", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📍 UB Campus Help", callback_data="ub_campuses")
        )
        markup.add(
            types.InlineKeyboardButton("🔙 All Categories", callback_data="back_main"),
            types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif bill_type == "campuses":
        response = """📍 **UNIVERSITY AT BUFFALO CAMPUSES**

🎓 **TWO CAMPUSES - ONE SERVICE:**

🏢 **NORTH CAMPUS (Amherst):**
• Main academic campus
• Engineering, Business, Arts
• Most on-campus housing
• Ellicott Complex
• Governors Complex
• Greiner Hall
• All facilities

🏢 **SOUTH CAMPUS (Buffalo):**
• Medical & professional schools
• Architecture, Law, Nursing
• Goodyear Hall housing
• Medical School
• Dental School
• Health sciences

💰 **OUR 50% SERVICE COVERS BOTH:**
• All housing on both campuses
• All utilities for both locations
• All campus expenses
• All student needs
• All academic programs

📞 **Contact @yrfrnd_spidy for campus-specific help**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📍 North Campus", callback_data="campus_north"),
            types.InlineKeyboardButton("📍 South Campus", callback_data="campus_south")
        )
        markup.add(
            types.InlineKeyboardButton("🏠 Housing Help", callback_data="ub_rent"),
            types.InlineKeyboardButton("📞 Contact Now", url="https://t.me/yrfrnd_spidy")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif bill_type == "how":
        response = """🔄 **HOW OUR 50% UB SERVICE WORKS**

🎯 **SIMPLE 3-STEP PROCESS:**

1️⃣ **APPLY (5 Minutes):**
• Message @yrfrnd_spidy
• Send UB Student ID
• Share bill/expense amount
• Get instant approval

2️⃣ **WE PAY 100%:**
• We pay UB Bursar 100%
• Or pay utility provider 100%
• Or top-up GET app 100%
• Same-day processing

3️⃣ **YOU PAY 50% BACK:**
• Flexible installments
• 4-12 month plans
• 0% interest first 3 months
• Student-friendly payments

💰 **EXAMPLE SCENARIOS:**

**CASE 1: UB HOUSING**
• Need: $5,000 semester housing
• **We pay**: $5,000 to UB
• **You pay**: $2,500 back
• **Monthly**: $250 for 10 months

**CASE 2: UTILITY BILLS**
• Need: $200 electricity bill
• **We pay**: $200 to National Grid
• **You pay**: $100 back
• **Weekly**: $25 for 4 weeks

**CASE 3: GET APP EMERGENCY**
• Need: $500 for meal plan
• **We add**: $500 to GET app
• **You pay**: $250 back
• **Monthly**: $50 for 5 months

✅ **ELIGIBILITY:**
• Must be current UB student
• Valid UB ID required
• Any expense over $50
• No credit check needed

📋 **DOCUMENTS NEEDED:**
• UB Student ID photo
• Bill/expense proof
• Contact information
• That's it!

⏰ **PROCESSING TIMES:**
• Standard: 2-4 hours
• Express: 1-2 hours
• Emergency: 30-60 minutes
• 24/7 service

📞 **READY TO APPLY?**
Contact @yrfrnd_spidy right now!"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📞 Apply Now", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("🏠 Housing Help", callback_data="ub_rent")
        )
        markup.add(
            types.InlineKeyboardButton("⚡ Utility Help", callback_data="ub_utilities"),
            types.InlineKeyboardButton("📱 GET App Help", callback_data="ub_get_app")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('campus_'))
def campus_handler(call):
    campus_type = call.data.replace('campus_', '')
    
    if campus_type in UB_CAMPUSES:
        campus = UB_CAMPUSES[campus_type]
        
        response = f"{campus['name']}\n\n{campus['details']}"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📞 {campus_type.title()} Campus Help", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📍 Both Campuses", callback_data="ub_campuses")
        )
        markup.add(
            types.InlineKeyboardButton("🏠 Housing Help", callback_data="ub_rent"),
            types.InlineKeyboardButton("⚡ Utility Help", callback_data="ub_utilities")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BACK HANDLER =====
@bot.callback_query_handler(func=lambda call: call.data == 'back_main')
def back_main_handler(call):
    start_command(call.message)

# ===== ADMIN COMMANDS =====
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin only.")
        return
    
    user_count = len(broadcast_users)
    
    stats_message = (
        f"📊 **UB 50% PAYMENT BOT STATISTICS**\n\n"
        f"🎓 **University at Buffalo Service**\n\n"
        f"👥 **Total UB Students:** {user_count}\n"
        f"💰 **Categories:** {len(UB_BILLS)} expense types\n"
        f"📍 **Campuses Covered:** North & South\n"
        f"✅ **Eligibility:** All UB students\n\n"
        f"📈 **Growth:** +{min(user_count, 100)} today\n"
        f"⏰ **Status:** ✅ Active 24/7\n"
        f"📞 **Primary Contact:** @yrfrnd_spidy\n"
        f"📞 **Support Contact:** @Eatsplugsus\n"
        f"📢 **Channel:** @flights_bills_b4u\n\n"
        f"*50% OFF All UB Expenses Bot*"
    )
    
    bot.send_message(ADMIN_ID, stats_message, parse_mode='Markdown')

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin only.")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No UB students yet.")
        return
    
    msg = bot.send_message(
        ADMIN_ID, 
        f"📤 Send 50% OFF alert to {len(broadcast_users)} UB students:\n\n"
        f"Type your UB 50% OFF deal:"
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    
    message.is_broadcast_processed = True
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    
    status_msg = bot.send_message(ADMIN_ID, f"📤 Sending to {len(users)} UB students...")
    
    for user_id in users:
        try:
            notification = (
                f"🎓 **UB 50% PAYMENT ALERT** 🎓\n\n"
                f"{broadcast_text}\n\n"
                f"📍 Both UB Campuses covered\n"
                f"💰 Guaranteed 50% OFF all UB expenses\n"
                f"📞 Contact @yrfrnd_spidy now!\n"
                f"📞 Or @Eatsplugsus for support\n\n"
                f"*University at Buffalo Student Service*"
            )
            bot.send_message(user_id, notification)
            success_count += 1
        except Exception:
            pass
    
    bot.edit_message_text(
        f"✅ **UB Alert Sent!**\n\n"
        f"📊 **Results:**\n"
        f"• ✅ Success: {success_count} students\n"
        f"• 📊 Total: {len(users)} students\n\n"
        f"*50% OFF UB deal delivered!*",
        ADMIN_ID,
        status_msg.message_id
    )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    if message.text and message.text.lower() in ['hi', 'hello', 'hey', '/start']:
        return
    
    if not message.text.startswith('/'):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📞 Contact @yrfrnd_spidy", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📞 Contact @Eatsplugsus", url="https://t.me/Eatsplugsus")
        )
        markup.add(
            types.InlineKeyboardButton("🚀 Start Bot", callback_data="back_main"),
            types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(
            message.chat.id,
            "🎓 **UNIVERSITY AT BUFFALO 50% PAYMENT SERVICE**\n\n"
            "🔥 **Pay ONLY 50% for EVERY UB expense:**\n"
            "• 🏠 UB Housing: On-campus & off-campus\n"
            "• ⚡ Utilities: Electricity, heating, internet\n"
            "• 📱 GET App: Meal plans, dining dollars\n"
            "• 🎓 Tuition & Fees: All academic costs\n"
            "• 🏥 Medical: Health insurance, prescriptions\n"
            "• 🚌 Transportation: Parking, bus passes\n"
            "• 📚 Books & Supplies: Textbooks, materials\n"
            "• 📦 Other: Food, emergencies, everything\n\n"
            "📍 **Coverage:** Both UB Campuses\n"
            "💰 **Guarantee:** Pay ONLY 50%\n"
            "⏰ **Service:** 24/7 Student Help\n\n"
            "📞 **Contact for immediate UB help:**\n"
            "• @yrfrnd_spidy (Primary)\n"
            "• @Eatsplugsus (Support)\n"
            "• @flights_bills_b4u (Updates)\n\n"
            "Click buttons below or type /start!",
            reply_markup=markup,
            parse_mode='Markdown'
        )

# ===== FLASK ROUTES =====
@app.route('/')
def home():
    return "UB 50% Payment Service Bot - Active ✅"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Token required")
    
    try:
        bot.remove_webhook()
        render_domain = os.environ.get("RENDER_EXTERNAL_URL")
        
        if render_domain:
            webhook_url = f"{render_domain}/{TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"🎓 **UB 50% PAYMENT BOT DEPLOYED**")
            print(f"💰 Discount: 50% OFF ALL UB EXPENSES")
            print(f"📍 Coverage: Both UB Campuses")
            print(f"📊 Categories: {len(UB_BILLS)} expense types")
            print(f"🏠 Housing: On-campus & off-campus")
            print(f"📱 GET App: Campus payment system")
            print(f"📞 Primary Contact: @yrfrnd_spidy")
            print(f"📞 Support Contact: @Eatsplugsus")
            print(f"📢 Updates Channel: @flights_bills_b4u")
            print(f"👑 Admin ID: {ADMIN_ID}")
        else:
            print("🔧 Running in polling mode (development)")
            
    except Exception as e:
        print(f"⚠️ Webhook setup: {e}")
    
    print("\n" + "="*60)
    print("🎓 **UB SEO OPTIMIZATION SUMMARY:**")
    print("="*60)
    print("✅ Primary: University at Buffalo 50% payment service")
    print("✅ Housing: UB housing discount, dorm payment help")
    print("✅ Utilities: Buffalo student utility bill assistance")
    print("✅ GET App: UB meal plan discount, dining dollars help")
    print("✅ Tuition: UB tuition assistance, college fee help")
    print("✅ Medical: UB student health insurance discount")
    print("✅ Books: UB textbook discount, course materials help")
    print("✅ Transport: UB parking discount, student bus pass")
    print("="*60)
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

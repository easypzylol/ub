import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7016264130  # Replace with your actual Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user data
broadcast_users = set()
user_chat_states = {}
payment_requests = {}

# ===== UB ACCOMMODATION DATA =====
UB_ACCOMMODATION = {
    "on_campus": {
        "title": "🏢 **ON-CAMPUS HOUSING - University at Buffalo**",
        "details": """**UNIVERSITY HOUSING OPTIONS:**

🎓 **RESIDENCE HALLS:**
• **Ellicott Complex**: 8 buildings, 3,000+ students
• **Governors Complex**: Traditional halls
• **Goodyear Hall**: South Campus location
• **Greiner Hall**: Suite-style, premium

💰 **ROOM RATES (2024-2025 Academic Year):**
• **Double Room**: $4,500 - $5,800/semester
• **Single Room**: $5,200 - $6,800/semester
• **Suite/Apartment**: $6,000 - $8,200/semester
• **Meal Plan Required**: $2,800 - $3,500/semester

✅ **BILLS INCLUDED:**
• High-speed internet (UB Secure)
• Electricity & heating
• Water & sewage
• Basic cable TV
• 24/7 security & maintenance

🔗 **APPLICATION PROCESS:**
1. Apply via UB Housing Portal
2. Priority deadline: May 1st
3. Room selection in June
4. Move-in: Late August

🎯 **OUR 50% PAYMENT SERVICE:**
✅ We pay 50% of your on-campus housing costs
✅ Payment made directly to UB Bursar office
✅ Flexible repayment plan (4-12 months)
✅ No credit check required
✅ Available for all residence halls"""
    },
    
    "off_campus": {
        "title": "🏠 **OFF-CAMPUS HOUSING - Buffalo Area**",
        "details": """**POPULAR OFF-CAMPUS AREAS:**

🏡 **NORTH CAMPUS AREA (Amherst):**
• **University Heights**: 1-3 miles from campus
• **Sweet Home Road**: Apartments & townhouses
• **Maple Road**: Student complexes
• **Rensch Road**: Affordable options

💰 **RENTAL PRICES (Monthly):**
• **Room in shared house**: $400 - $650
• **Studio apartment**: $700 - $950
• **1-Bedroom apartment**: $850 - $1,200
• **2-Bedroom apartment**: $1,100 - $1,600

💡 **BILLS BREAKDOWN (Monthly Average):**
• **Electricity**: $50 - $100 (winter: $150+)
• **Heating (Gas)**: $40 - $120
• **Internet**: $40 - $70 (Spectrum/Verizon)
• **Water/Sewer**: $20 - $40 (if not included)

🎯 **OUR 50% PAYMENT SERVICE COVERS:**
✅ 50% of monthly rent payment
✅ 50% of utility bills (electricity, gas, water)
✅ 50% of internet/cable bills
✅ Setup fee assistance for new accounts
✅ Landlord payment coordination"""
    },
    
    "bills": {
        "title": "💰 **COMPLETE BILLS GUIDE - UB Housing**",
        "details": """**MONTHLY EXPENSE BREAKDOWN:**

💡 **UTILITIES (Average Monthly):**
• **Electricity (National Grid):**
  - Studio/1BR: $50 - $80
  - 2BR apartment: $80 - $120
  - Winter heating: Add 40-60%

• **Heating (Natural Gas):**
  - October-April: $60 - $150
  - Budget billing available

• **Internet & Cable:**
  - Spectrum: $49.99/mo (1yr promo)
  - Verizon Fios: $39.99/mo (promo)

• **Water/Sewer/Trash:**
  - Usually included in rent
  - If separate: $40-60 quarterly

📱 **GET COLLEGE APP - BILL PAYMENT:**
• **On-campus bills**: Direct in app
• **Payment plans**: Installment options
• **Due dates**: 1st of each month
• **Late fees**: $50 after 10 days

💳 **OUR 50% PAYMENT SERVICE FOR BILLS:**
✅ **Electricity Bills**: We pay 50% of National Grid bills
✅ **Gas/Heating**: 50% of heating costs covered
✅ **Internet**: Half your Spectrum/Verizon bill paid
✅ **Water/Sewer**: 50% assistance available
✅ **GET App Balance**: We load 50% of needed funds

📋 **HOW IT WORKS:**
1. Send us your bill screenshot
2. We pay 50% directly to provider
3. You repay us in flexible installments
4. No interest for 3 months"""
    },
    
    "get_app": {
        "title": "📱 **GET COLLEGE APP - 50% Payment Service**",
        "details": """**UB GET MOBILE APP PAYMENTS:**

💳 **BILL PAYMENT SYSTEM:**
• Housing charges auto-posted
• Payment plan setup
• E-check (no fee) or card (2.85% fee)
• Due dates: 1st of month

🎯 **OUR 50% GET APP SERVICE:**

✅ **GET APP BALANCE TOP-UP:**
• We add 50% of needed funds to your GET account
• Funds available instantly
• Use for housing payments, dining, printing

✅ **MEAL PLAN ASSISTANCE:**
• 50% of meal plan costs covered
• Dining dollars loaded to your account
• Swipe meal payments assisted

✅ **HOUSING PAYMENTS:**
• 50% of on-campus housing payments
• Direct to UB Bursar account
• Timely payments to avoid holds

✅ **OTHER CAMPUS EXPENSES:**
• Printing credits
• Laundry money
• Event tickets
• Bookstore purchases

🔄 **PROCESS FOR GET APP PAYMENTS:**
1. Share GET app balance screenshot
2. Tell us amount needed
3. We transfer 50% to your account
4. You repay in student-friendly installments

⚠️ **ELIGIBILITY:**
• Must be current UB student
• Valid UB ID required
• Active GET account needed
• Minimum $100 request"""
    },
    
    "payment_service": {
        "title": "💳 **50% PAYMENT SERVICE - Complete Guide**",
        "details": """**OUR PREMIUM PAYMENT ASSISTANCE SERVICE**

🎯 **WHAT WE COVER (50% PAID BY US):**

🏠 **RENT PAYMENTS:**
• On-campus housing: 50% of semester costs
• Off-campus rent: 50% of monthly payments
• Apartment complexes: 50% assistance
• Security deposits: 50% help available

💡 **UTILITY BILLS:**
• Electricity (National Grid): 50% paid
• Heating gas: 50% winter assistance
• Internet: Half your monthly bill
• Water/Sewer: 50% coverage

📱 **GET APP PAYMENTS:**
• Housing balance: 50% topped up
• Meal plans: Half the cost covered
• Dining dollars: 50% loaded
• Campus expenses: 50% assistance

📦 **OTHER EXPENSES:**
• Textbooks: 50% of cost
• Transportation: Half of bus pass/parking
• Groceries: 50% weekly assistance
• Emergency expenses: 50% help

💰 **SERVICE FEATURES:**

✅ **NO CREDIT CHECK REQUIRED**
✅ **Flexible repayment**: 4-12 months
✅ **0% interest for first 3 months**
✅ **Direct payment to providers**
✅ **24/7 application processing**
✅ **Emergency same-day funding**

📋 **ELIGIBILITY REQUIREMENTS:**
• Currently enrolled UB student
• Valid UB ID card
• Proof of enrollment
• US bank account (for repayments)
• Minimum $100 assistance request

⚡ **QUICK APPLICATION PROCESS:**
1. Message us with your request
2. Send required documents
3. Get approval in 2-4 hours
4. Receive 50% payment same/next day
5. Start flexible repayments

💬 **READY TO APPLY? Contact:** @yrfrnd_spidy"""
    },
    
    "how_it_works": {
        "title": "🔄 **HOW OUR 50% SERVICE WORKS**",
        "details": """**STEP-BY-STEP PROCESS:**

📝 **STEP 1: APPLICATION**
• Message us @yrfrnd_spidy
• Specify what you need (rent, bills, GET app)
• Share amount needed
• We send application form

📄 **STEP 2: DOCUMENTATION**
• UB Student ID photo
• Proof of enrollment
• Bill/rent statement screenshot
• GET app balance screenshot
• ID verification

✅ **STEP 3: APPROVAL**
• Quick review (2-4 hours)
• 50% payment calculation
• Repayment plan customization
• Agreement signing

💰 **STEP 4: PAYMENT**
• **Option A**: We pay provider directly
• **Option B**: Transfer to your account
• **Option C**: Load GET app balance
• Same/next day processing

📅 **STEP 5: REPAYMENT**
• Flexible 4-12 month plans
• First payment after 30 days
• 0% interest for 3 months
• Auto-debit or manual payments

🎯 **EXAMPLE SCENARIOS:**

**CASE 1: ON-CAMPUS HOUSING**
• Semester cost: $5,000
• **We pay**: $2,500 (50%)
• Your repayment: $250/month for 10 months
• **Savings**: Immediate $2,500 relief

**CASE 2: MONTHLY RENT + BILLS**
• Rent: $600 + Bills: $200 = $800
• **We pay**: $400 (50%)
• Your repayment: $100/week for 4 weeks
• **Benefit**: Half your housing covered

**CASE 3: GET APP EMERGENCY**
• Need: $500 for housing payment
• **We add**: $250 to GET account
• Your repayment: $50/week for 5 weeks
• **Result**: Avoid late fees & holds

⚠️ **IMPORTANT NOTES:**
• Minimum request: $100
• Maximum per semester: $5,000
• Repayment starts after 30 days
• No penalty for early repayment
• Credit building opportunity"""
    },
    
    "apply_now": {
        "title": "🚀 **APPLY FOR 50% PAYMENT SERVICE**",
        "details": """**IMMEDIATE ASSISTANCE AVAILABLE**

💬 **CONTACT OUR TEAM:**
👉 **Primary Contact**: @yrfrnd_spidy
👉 **Support**: @Eatsplugsus
👉 **Channel**: @flights_bills_b4u

📱 **QUICK APPLICATION:**

**OPTION 1: INSTANT MESSAGE**
1. Message @yrfrnd_spidy
2. Type: "APPLY 50% SERVICE"
3. Follow prompts
4. Get same-day response

**OPTION 2: DOCUMENT SUBMISSION**
1. Send: UB Student ID
2. Send: Current bill/rent statement
3. Send: GET app screenshot (if applicable)
4. Specify amount needed
5. We calculate 50% assistance

**OPTION 3: EMERGENCY REQUEST**
1. Message: "EMERGENCY 50%"
2. State urgent need
3. Provide contact number
4. Get callback within 1 hour

📋 **REQUIRED DOCUMENTS:**
• Clear photo of UB Student ID
• Current class schedule/enrollment proof
• Bill/rent statement (screenshot OK)
• GET app balance screenshot
• Government-issued ID

⏰ **PROCESSING TIMES:**
• **Standard**: 2-4 hours approval
• **Express**: 1-2 hours (+$10 fee)
• **Emergency**: 30-60 minutes (+$25 fee)
• **Weekend**: Same day service

💰 **SERVICE FEES:**
• **Processing fee**: 5% of assistance amount
• **Express fee**: $10 (1-2 hour approval)
• **Emergency fee**: $25 (30-60 minute)
• **No hidden charges**
• **Fee deducted from assistance**

✅ **GUARANTEES:**
• 100% approval rate for UB students
• Funds transferred same/next day
• Secure payment processing
• Confidentiality maintained
• Flexible repayment options

📞 **NEED HELP APPLYING?**
Contact @yrfrnd_spidy right now!"""
    }
}

# ===== UB RESOURCES WITH PAYMENT INFO =====
UB_RESOURCES = {
    "bursar": {
        "name": "💰 UB Bursar Office (Payments)",
        "contact": "Phone: (716) 645-1800\nEmail: ub-bursar@buffalo.edu",
        "note": "**OUR SERVICE**: We pay 50% directly to Bursar account"
    },
    "housing": {
        "name": "🏠 UB Housing Office",
        "contact": "Phone: (716) 645-2171\nEmail: ub-housing@buffalo.edu",
        "note": "**OUR SERVICE**: 50% housing payment assistance"
    },
    "utilities": {
        "name": "💡 Utility Companies",
        "contact": "Electric: National Grid (800) 642-4272\nGas: National Fuel (800) 365-3232\nInternet: Spectrum (833) 267-6094",
        "note": "**OUR SERVICE**: We pay 50% of your utility bills"
    },
    "get_app": {
        "name": "📱 GET College App Support",
        "contact": "GET Help: (855) 438-7438\nUB IT: (716) 645-3542",
        "note": "**OUR SERVICE**: 50% GET app balance top-up"
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    if message is None:
        return

    user_id = message.from_user.id
    broadcast_users.add(user_id)
    user_chat_states[user_id] = 'started'

    # Create main menu keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Main categories
    keyboard.add(
        types.InlineKeyboardButton("🏢 On-Campus", callback_data="ub_on_campus"),
        types.InlineKeyboardButton("🏠 Off-Campus", callback_data="ub_off_campus")
    )
    keyboard.add(
        types.InlineKeyboardButton("💰 Bills Guide", callback_data="ub_bills"),
        types.InlineKeyboardButton("📱 GET App", callback_data="ub_get_app")
    )
    keyboard.add(
        types.InlineKeyboardButton("💳 50% Service", callback_data="ub_payment_service"),
        types.InlineKeyboardButton("🔄 How It Works", callback_data="ub_how_it_works")
    )
    keyboard.add(
        types.InlineKeyboardButton("🚀 Apply Now", callback_data="ub_apply_now"),
        types.InlineKeyboardButton("📞 UB Contacts", callback_data="ub_contacts")
    )
    keyboard.add(
        types.InlineKeyboardButton("💬 Immediate Help", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📢 Updates", url="https://t.me/flights_bills_b4u")
    )

    welcome_message = (
        "🎓 **UNIVERSITY AT BUFFALO HOUSING & PAYMENT BOT**\n\n"
        "**50% PAYMENT SERVICE ON ALL UB EXPENSES**\n\n"
        
        "💰 **WHAT WE PAY 50% OF:**\n"
        "✅ **RENT**: On-campus & off-campus housing\n"
        "✅ **UTILITIES**: Electricity, heating, internet\n"
        "✅ **GET APP**: Balance, meal plans, dining dollars\n"
        "✅ **BILLS**: All housing-related expenses\n\n"
        
        "🚀 **HOW IT WORKS:**\n"
        "1. You need $1,000 for rent/bills\n"
        "2. **WE PAY $500** (50%) immediately\n"
        "3. You repay us in flexible installments\n"
        "4. 0% interest for first 3 months\n\n"
        
        "⚡ **QUICK SERVICE:**\n"
        "• Approval in 2-4 hours\n"
        "• Same-day funding\n"
        "• No credit check\n"
        "• All UB students eligible\n\n"
        
        "💳 **COVERAGE EXAMPLES:**\n"
        "• $5,000 semester housing → **We pay $2,500**\n"
        "• $800 monthly rent → **We pay $400**\n"
        "• $200 utility bill → **We pay $100**\n"
        "• $500 GET app balance → **We add $250**\n\n"
        
        "📱 **CONTACT FOR SERVICE:** @yrfrnd_spidy\n\n"
        "**Select a category below to learn more:**"
    )

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard, parse_mode='Markdown')

# ===== MAIN CATEGORY HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('ub_'))
def ub_handler(call):
    """Handle UB accommodation category clicks"""
    user_id = call.from_user.id
    option = call.data.replace('ub_', '')
    
    if option in UB_ACCOMMODATION:
        info = UB_ACCOMMODATION[option]
        
        response = f"{info['title']}\n\n{info['details']}"
        
        # Add action buttons based on category
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        if option == "payment_service" or option == "how_it_works" or option == "apply_now":
            markup.add(
                types.InlineKeyboardButton("🚀 Apply Now", url="https://t.me/yrfrnd_spidy"),
                types.InlineKeyboardButton("📞 Quick Call", callback_data="quick_call")
            )
        else:
            markup.add(
                types.InlineKeyboardButton("💳 50% Service", callback_data="ub_payment_service"),
                types.InlineKeyboardButton("🔄 How It Works", callback_data="ub_how_it_works")
            )
        
        markup.add(
            types.InlineKeyboardButton("💬 Get 50% Now", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "contacts":
        response = "📞 **UB CONTACTS WITH OUR 50% SERVICE**\n\n"
        
        for key, office in UB_RESOURCES.items():
            response += f"{office['name']}\n"
            response += f"📞 {office['contact']}\n"
            response += f"🎯 {office['note']}\n\n"
        
        response += "**OUR SERVICE CONTACTS:**\n"
        response += "👉 **Application**: @yrfrnd_spidy\n"
        response += "👉 **Support**: @Eatsplugsus\n"
        response += "👉 **Emergency**: Immediate response\n"
        response += "👉 **Hours**: 24/7 for UB students\n\n"
        response += "**EMERGENCY NUMBERS:**\n"
        response += "🚨 UB Police: (716) 645-2222\n"
        response += "🏥 Student Health: (716) 829-3316"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Apply for 50%", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📱 GET App Help", callback_data="ub_get_app")
        )
        markup.add(
            types.InlineKeyboardButton("💰 Bills Assistance", callback_data="ub_bills"),
            types.InlineKeyboardButton("🏠 Housing Help", callback_data="ub_on_campus")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== PAYMENT CALCULATOR =====
@bot.callback_query_handler(func=lambda call: call.data == 'calculate_50')
def calculate_payment(call):
    response = """🧮 **50% PAYMENT CALCULATOR**

💰 **ENTER YOUR EXPENSE:**
Example: If you need $1,000, WE PAY $500

**COMMON UB EXPENSES:**

🏠 **HOUSING COSTS:**
• On-campus semester: $5,000 → **We pay: $2,500**
• Monthly rent: $800 → **We pay: $400**
• Security deposit: $1,000 → **We pay: $500**

💡 **UTILITY BILLS:**
• Electricity: $150 → **We pay: $75**
• Heating: $200 → **We pay: $100**
• Internet: $60 → **We pay: $30**
• All utilities: $410 → **We pay: $205**

📱 **GET APP EXPENSES:**
• Meal plan: $3,000 → **We pay: $1,500**
• Dining dollars: $500 → **We pay: $250**
• Housing payment: $2,000 → **We pay: $1,000**
• Printing/laundry: $100 → **We pay: $50**

📦 **OTHER EXPENSES:**
• Textbooks: $600 → **We pay: $300**
• Transportation: $400 → **We pay: $200**
• Groceries: $300 → **We pay: $150**
• Emergency: $1,000 → **We pay: $500**

📋 **REPAYMENT EXAMPLES:**

**EXAMPLE 1: $2,500 ASSISTANCE**
• Our payment: $2,500 (50% of $5,000)
• Repayment plan: 10 months
• Monthly payment: $250
• First 3 months: 0% interest

**EXAMPLE 2: $400 MONTHLY ASSISTANCE**
• Our payment: $400 (50% of $800 rent)
• Repayment plan: 4 weeks
• Weekly payment: $100
• Flexible scheduling

**EXAMPLE 3: $250 GET APP TOP-UP**
• Our payment: $250 (50% of $500)
• Repayment plan: 5 weeks
• Weekly payment: $50
• Simple & affordable

💬 **READY TO CALCULATE YOUR 50%?**
Message @yrfrnd_spidy with:
1. Total amount needed
2. Expense type (rent/bills/GET app)
3. Your repayment preference"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💬 Calculate My 50%", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("🚀 Apply Now", callback_data="ub_apply_now")
    )
    markup.add(
        types.InlineKeyboardButton("💳 Service Details", callback_data="ub_payment_service"),
        types.InlineKeyboardButton("🔄 How It Works", callback_data="ub_how_it_works")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== QUICK APPLICATION =====
@bot.callback_query_handler(func=lambda call: call.data == 'quick_apply')
def quick_application(call):
    response = """🚀 **QUICK 50% PAYMENT APPLICATION**

⚡ **FAST-TRACK PROCESS (2 HOURS APPROVAL)**

**STEP 1: MESSAGE @yrfrnd_spidy**
Send this exact message:
\"QUICK 50% APPLICATION - UB STUDENT\"

**STEP 2: PROVIDE BASIC INFO:**
• Your full name
• UB email address
• Amount needed
• Expense type (rent/bills/GET app)

**STEP 3: GET APPROVAL**
• We review in 1-2 hours
• 50% amount calculated
• Repayment plan created
• Agreement sent for signing

**STEP 4: RECEIVE PAYMENT**
• **Option A**: We pay provider directly
• **Option B**: Transfer to your account
• **Option C**: GET app top-up
• Same/next day processing

📋 **DOCUMENTS NEEDED (Can send later):**
1. UB Student ID photo
2. Proof of enrollment
3. Bill/rent statement
4. Government ID

💰 **FEES:**
• Processing: 5% of assistance
• Express (2-hour): $10 extra
• Emergency (1-hour): $25 extra
• No other hidden charges

✅ **GUARANTEES:**
• 100% approval for UB students
• Minimum $100 assistance
• Maximum $5,000 per semester
• Confidential & secure

⏰ **PROCESSING TIMES:**
• **Normal**: 2-4 hours
• **Express**: 1-2 hours (+$10)
• **Emergency**: 30-60 mins (+$25)
• **Weekends**: Same day available

🎯 **READY TO APPLY?**
👉 **Click below to message us now!**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📱 Message @yrfrnd_spidy", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Call for Help", callback_data="call_help")
    )
    markup.add(
        types.InlineKeyboardButton("💳 Service Details", callback_data="ub_payment_service"),
        types.InlineKeyboardButton("🧮 Calculator", callback_data="calculate_50")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== EMERGENCY ASSISTANCE =====
@bot.callback_query_handler(func=lambda call: call.data == 'emergency_help')
def emergency_assistance(call):
    response = """🚨 **EMERGENCY 50% PAYMENT ASSISTANCE**

⚡ **IMMEDIATE HELP FOR URGENT SITUATIONS:**

**EMERGENCY SCENARIOS WE COVER:**
• Rent due today/tomorrow
• Utility shut-off notice
• GET app balance empty
• Housing payment overdue
• Unexpected expense
• Financial emergency

⏰ **EMERGENCY PROCESS (30-60 MINUTES):**

**STEP 1: CONTACT IMMEDIATELY**
Message: @yrfrnd_spidy
Text: \"EMERGENCY 50% - UB STUDENT\"

**STEP 2: PROVIDE DETAILS:**
• What's the emergency?
• Amount needed urgently
• Due date/timing
• Your contact number

**STEP 3: GET CALLBACK**
• We call within 15 minutes
• Quick verification
• Immediate approval
• Funds same day

**STEP 4: RECEIVE FUNDS**
• Direct payment to provider
• Or transfer to your account
• Or GET app top-up
• Within 1-2 hours

💰 **EMERGENCY FEES:**
• Standard processing: 5%
• Emergency fee: $25
• Total: 5% + $25
• Example: $1,000 need = $75 total fee

✅ **EMERGENCY GUARANTEES:**
• No credit check
• Same-day funding
• 100% approval
• 24/7 availability
• Weekend service

📞 **EMERGENCY CONTACTS:**
👉 **Primary**: @yrfrnd_spidy
👉 **Backup**: @Eatsplugsus
👉 **Channel**: @flights_bills_b4u
👉 **Phone**: Available upon request

⚠️ **EMERGENCY DOCUMENTS (Can send after funding):**
1. UB Student ID
2. Emergency proof (bill, notice)
3. Quick verification
4. Agreement signing

🎯 **IN EMERGENCY? MESSAGE NOW!**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚨 EMERGENCY MESSAGE", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 URGENT CALL", callback_data="urgent_call")
    )
    markup.add(
        types.InlineKeyboardButton("💰 Regular Application", callback_data="quick_apply"),
        types.InlineKeyboardButton("💳 Service Info", callback_data="ub_payment_service")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Admin feature only")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users to notify")
        return
    
    msg = bot.send_message(
        ADMIN_ID,
        f"📢 Send 50% service update to {len(broadcast_users)} UB students:"
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if hasattr(message, 'processed') and message.processed:
        return
    message.processed = True
    
    text = message.text
    users = list(broadcast_users)
    success = 0
    
    status = bot.send_message(ADMIN_ID, f"📤 Sending to {len(users)} users...")
    
    for user_id in users:
        try:
            notification = f"💳 **50% PAYMENT SERVICE UPDATE**\n\n{text}\n\n*Contact @yrfrnd_spidy to apply*\n*Use /start for details*"
            bot.send_message(user_id, notification)
            success += 1
        except:
            continue
    
    bot.edit_message_text(
        f"✅ Broadcast Complete!\n"
        f"📊 Sent to: {success}/{len(users)} users",
        ADMIN_ID,
        status.message_id
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    bot.send_message(
        ADMIN_ID,
        f"📊 **UB 50% Payment Bot Stats**\n\n"
        f"👥 Total Users: {len(broadcast_users)}\n"
        f"💳 Service: 50% Payment Assistance\n"
        f"💰 Coverage: Rent, Bills, GET App\n"
        f"🏠 Housing: On/Off Campus Covered\n"
        f"📱 GET App: Balance Top-up Service\n"
        f"⚡ Speed: Same-day Funding\n"
        f"✅ Approval: 100% for UB Students"
    )

# ===== USER QUERY HANDLING =====
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    text_lower = message.text.lower()
    
    # Check for payment/service related keywords
    payment_keywords = ['50%', 'fifty percent', 'payment', 'assistance', 'help', 'need money', 'rent', 'bill', 'utility', 'get app']
    if any(keyword in text_lower for keyword in payment_keywords):
        response = """💳 **50% PAYMENT SERVICE RESPONSE**

I see you're asking about payment assistance! 🎓

🚀 **OUR 50% SERVICE COVERS:**
✅ **RENT**: We pay 50% of your housing costs
✅ **UTILITIES**: 50% of electricity, heating, internet
✅ **GET APP**: 50% balance top-up for all expenses
✅ **BILLS**: All UB-related expenses covered

⚡ **QUICK PROCESS:**
1. You need $X for rent/bills/GET app
2. **WE PAY $X/2** (50%) immediately
3. You repay in flexible installments
4. 0% interest for 3 months

📋 **TO APPLY:**
1. Message @yrfrnd_spidy
2. Say: "APPLY 50% SERVICE"
3. Provide basic details
4. Get approved in 2-4 hours

💰 **EXAMPLE:**
Need $1,000 for rent?
**We pay $500** now!
You repay $100/month for 5 months

💬 **READY? Contact @yrfrnd_spidy now!**

Or use /start to see all options"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Apply Now", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("💳 Service Details", callback_data="ub_payment_service")
        )
        markup.add(
            types.InlineKeyboardButton("🔄 How It Works", callback_data="ub_how_it_works"),
            types.InlineKeyboardButton("🚀 Quick Apply", callback_data="quick_apply")
        )
        
        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    else:
        # Forward to admin for response
        user_messages[message.message_id] = {
            'user_id': user_id,
            'user_name': message.from_user.first_name,
            'text': message.text
        }
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📨 Reply with 50% Service", callback_data=f"admin_reply_{message.message_id}"))
        
        bot.send_message(
            ADMIN_ID,
            f"📝 New UB Student Query\n"
            f"From: {message.from_user.first_name}\n"
            f"ID: {user_id}\n\n"
            f"Message: {message.text}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_reply_'))
def admin_reply_callback(call):
    msg_id = int(call.data.split('_')[-1])
    
    if msg_id in user_messages:
        user_data = user_messages[msg_id]
        
        reply_msg = bot.send_message(
            ADMIN_ID,
            f"💬 Reply to {user_data['user_name']} about 50% service:\n"
            f"(Their message: '{user_data['text'][:50]}...')"
        )
        
        bot.register_next_step_handler(reply_msg, send_reply, user_data['user_id'])

def send_reply(message, user_id):
    try:
        bot.send_message(
            user_id,
            f"💳 **50% PAYMENT SERVICE REPLY:**\n\n{message.text}\n\n"
            f"*Contact @yrfrnd_spidy for immediate assistance*\n"
            f"*Use /start for all service options*"
        )
        bot.reply_to(message, "✅ Reply sent with 50% service info!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# ===== WEBHOOK SETUP (Minimal) =====
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

@app.route('/')
def minimal_home():
    return "UB 50% Payment Service Bot - Active ✅"

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Token required")
    
    try:
        bot.remove_webhook()
        render_domain = os.environ.get("RENDER_EXTERNAL_URL")
        
        if render_domain:
            webhook_url = f"{render_domain}/{TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"💳 UB 50% Payment Bot deployed: {webhook_url}")
        else:
            print("UB 50% Payment Bot running in polling mode")
            
    except Exception as e:
        print(f"Webhook setup: {e}")
    
    print("🎓 UNIVERSITY AT BUFFALO 50% PAYMENT BOT ACTIVE!")
    print("💳 SERVICE: 50% payment on rent, utilities, GET app")
    print("💰 COVERAGE: All UB housing expenses")
    print("⚡ SPEED: Same-day funding available")
    print("✅ APPROVAL: 100% for UB students")
    print("📱 CONTACT: @yrfrnd_spidy for applications")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

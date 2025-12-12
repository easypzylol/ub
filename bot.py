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
user_queries = {}

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

# ===== BOT HANDLERS =====
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)

    # Create main menu keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
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
        types.InlineKeyboardButton("💬 Immediate Help", url="https://t.me/yrfrnd_spidy")
    )
    keyboard.add(
        types.InlineKeyboardButton("📢 Updates", url="https://t.me/flights_bills_b4u")
    )

    welcome_message = (
        "🎓 **UNIVERSITY AT BUFFALO HOUSING & PAYMENT BOT**\n\n"
        "**50% PAYMENT SERVICE ON ALL UB EXPENSES**\n\n"
        
        "💰 **WHAT WE PAY 50% OF:**\n"
        "✅ **RENT**: On-campus & off-campus housing\n"
        "✅ **UTILITIES**: Electricity, heating, internet\n"
        "✅ **GET APP**: Balance, meal plans, dining dollars\n"
        "✅ **BILLS**: All UB-related expenses covered\n\n"
        
        "🚀 **HOW IT WORKS:**\n"
        "1. You need $1,000 for rent/bills/GET app\n"
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

# ===== CALLBACK QUERY HANDLER =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    option = call.data.replace('ub_', '')
    
    if option in UB_ACCOMMODATION:
        info = UB_ACCOMMODATION[option]
        response = f"{info['title']}\n\n{info['details']}"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        if option in ["payment_service", "how_it_works", "apply_now"]:
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
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=response,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    
    elif call.data == "main_menu":
        # Return to main menu
        start_command(call.message)
    
    elif call.data == "quick_call":
        bot.answer_callback_query(call.id, "Call option coming soon! Message @yrfrnd_spidy for now.")

# ===== TEXT MESSAGE HANDLER =====
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    # Store user query for admin
    user_queries[message.message_id] = {
        'user_id': user_id,
        'name': f"{message.from_user.first_name} {message.from_user.last_name or ''}",
        'username': f"@{message.from_user.username}" if message.from_user.username else "No username",
        'text': message.text
    }
    
    # Auto-response for common queries
    text_lower = message.text.lower()
    
    if any(word in text_lower for word in ['50%', 'fifty percent', 'payment', 'help', 'assistance']):
        bot.reply_to(
            message,
            "💳 **50% PAYMENT SERVICE ASSISTANCE**\n\n"
            "I see you're interested in our 50% payment service!\n\n"
            "**We pay 50% of:**\n"
            "✅ Rent (on/off-campus)\n"
            "✅ Utility bills\n"
            "✅ GET App balance\n"
            "✅ All UB expenses\n\n"
            "**Quick application:**\n"
            "1. Message @yrfrnd_spidy\n"
            "2. Send your UB Student ID\n"
            "3. Share bill/amount needed\n"
            "4. Get 50% payment same day!\n\n"
            "**Example:** Need $1,000? We pay $500 now!\n"
            "**Contact:** @yrfrnd_spidy for immediate help"
        )
    else:
        bot.reply_to(
            message,
            "🎓 **UB 50% Payment Service Bot**\n\n"
            "I help with 50% payment assistance for:\n"
            "• University at Buffalo housing\n"
            "• Utility bills\n"
            "• GET App payments\n"
            "• All student expenses\n\n"
            "Use buttons below or type:\n"
            "• '50% service' - Learn about our offer\n"
            "• 'Apply now' - Start application\n"
            "• 'Help' - Get assistance\n\n"
            "Or just click /start to see all options!"
        )
    
    # Notify admin about new message
    try:
        query_data = user_queries[message.message_id]
        admin_msg = f"📨 New Query from {query_data['name']} ({query_data['username']})\nUser ID: {user_id}\n\nMessage: {query_data['text']}\n\nReply via bot or contact @yrfrnd_spidy"
        bot.send_message(ADMIN_ID, admin_msg)
    except:
        pass

# ===== ADMIN COMMANDS =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users to notify")
        return
    
    bot.reply_to(message, f"Send broadcast message to {len(broadcast_users)} users:")
    bot.register_next_step_handler(message, process_broadcast)

def process_broadcast(message):
    users = list(broadcast_users)
    success = 0
    
    for user_id in users:
        try:
            bot.send_message(
                user_id,
                f"💳 **50% PAYMENT SERVICE UPDATE**\n\n{message.text}\n\n"
                f"*Contact @yrfrnd_spidy to apply*\n*Use /start for details*"
            )
            success += 1
        except:
            continue
    
    bot.reply_to(message, f"✅ Broadcast sent to {success}/{len(users)} users")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    bot.reply_to(
        message,
        f"📊 **Bot Statistics**\n\n"
        f"👥 Total Users: {len(broadcast_users)}\n"
        f"💳 Service: 50% Payment Assistance\n"
        f"💰 Coverage: Rent, Bills, GET App\n"
        f"🏠 Housing: On/Off Campus\n"
        f"📱 GET App: Balance Top-up\n"
        f"⚡ Speed: Same-day Funding\n"
        f"✅ Approval: 100% for UB Students"
    )

# ===== FLASK ROUTES =====
@app.route('/')
def home():
    return "UB 50% Payment Service Bot - Active ✅"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Error', 403

# ===== MAIN SETUP =====
if __name__ == '__main__':
    import sys
    
    # Check if running on Render (with PORT environment variable)
    port = int(os.environ.get('PORT', 5000))
    
    # Set webhook for production (Render)
    if 'render.com' in os.environ.get('RENDER_EXTERNAL_URL', ''):
        webhook_url = f"{os.environ.get('RENDER_EXTERNAL_URL')}/webhook"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"Webhook set to: {webhook_url}")
        app.run(host='0.0.0.0', port=port)
    else:
        # Local development - use polling
        print("Starting bot in polling mode...")
        bot.remove_webhook()
        bot.polling(none_stop=True)

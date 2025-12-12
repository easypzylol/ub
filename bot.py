import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7016264130

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user info
broadcast_users = set()

# ===== SEO KEYWORDS DATABASE =====
SEO_KEYWORDS = {
    "primary": [
        "university at buffalo housing", "UB accommodation", "UB student housing",
        "UB dorm payment", "Buffalo student housing", "UB rent assistance",
        "UB housing discount", "University at Buffalo bills", "UB utility assistance"
    ],
    "secondary": [
        "50% off UB housing", "half off UB rent", "UB payment assistance",
        "UB GET app help", "UB meal plan discount", "UB tuition help",
        "UB medical bill assistance", "UB textbook discount", "UB transportation help"
    ],
    "campus_based": [
        "UB North Campus housing", "UB South Campus accommodation",
        "Ellicott Complex discount", "Greiner Hall payment",
        "Goodyear Hall assistance", "UB Amherst housing",
        "Buffalo university housing"
    ],
    "bill_based": [
        "UB electricity bill help", "UB internet discount",
        "UB water bill assistance", "UB heating bill help",
        "UB National Grid assistance", "UB Spectrum discount"
    ]
}

# ===== UB ACCOMMODATION DATA =====
UB_SERVICES = {
    "rent": {
        "title": "🏠 **UB HOUSING 50% OFF**",
        "details": """🎓 **PAY HALF FOR ALL UB HOUSING:**

✅ **ON-CAMPUS HOUSING 50% OFF:**
• Ellicott Complex: 50% OFF semester costs
• Governors Complex: Half price accommodation
• Goodyear Hall: South Campus 50% OFF
• Greiner Hall: Premium suites 50% OFF
• All residence halls covered
• Summer housing: 50% OFF
• Winter break housing: 50% OFF

✅ **OFF-CAMPUS HOUSING 50% OFF:**
• University Heights apartments
• Sweet Home Road apartments
• Maple Road student housing
• Rensch Road rentals
• All private landlords near UB
• All apartment complexes

💰 **PRICE EXAMPLES:**
• $5,000 semester → **You pay $2,500**
• $600/month rent → **You pay $300**
• Any housing cost → **You pay 50%**

📍 **COVERAGE:** Both North & South Campus
💰 **DISCOUNT:** 50% OFF all housing costs
📞 **Contact @yrfrnd_spidy for UB housing help**""",
        "keywords": ["half off UB housing", "50% off UB rent", "UB accommodation discount", "student housing assistance Buffalo"]
    },
    "utilities": {
        "title": "⚡ **UB UTILITY BILLS 50% OFF**",
        "details": """🔥 **PAY HALF FOR UB UTILITIES:**

✅ **ELECTRICITY BILLS 50% OFF:**
• National Grid bills for UB students
• High AC bills in summer 50% OFF
• Heating bills in winter 50% OFF
• All meters covered

✅ **INTERNET BILLS 50% OFF:**
• Spectrum internet for UB students
• Verizon Fios student deals
• High-speed internet 50% OFF
• WiFi plans 50% OFF

✅ **WATER & SEWER 50% OFF:**
• Buffalo water bills 50% OFF
• Amherst water department bills
• Sewer charges 50% OFF

✅ **HEATING/GAS 50% OFF:**
• Natural gas heating bills
• National Fuel bills 50% OFF
• Winter heating assistance

📍 **COVERAGE:** All UB student housing
💰 **DISCOUNT:** 50% OFF all utilities
📞 **Contact @yrfrnd_spidy for utility help**""",
        "keywords": ["half off electricity UB", "50% off internet student", "UB utility bill help", "Buffalo student utility discount"]
    },
    "get_app": {
        "title": "📱 **UB GET APP 50% OFF**",
        "details": """💳 **PAY HALF FOR UB GET APP:**

✅ **GET APP BALANCE 50% OFF:**
• Housing payments via GET app 50% OFF
• Meal plan payments 50% OFF
• Dining dollars top-up 50% OFF
• Printing credits 50% OFF
• Laundry money 50% OFF

✅ **MEAL PLANS 50% OFF:**
• All UB meal plans 50% OFF
• Dining dollars 50% OFF
• Flex dollars 50% OFF
• Campus Cash 50% OFF

✅ **OTHER CAMPUS EXPENSES 50% OFF:**
• Textbook purchases 50% OFF
• School supplies 50% OFF
• Printing & copying 50% OFF
• Laundry services 50% OFF

🔄 **HOW IT WORKS:**
1. Share GET app balance screenshot
2. We transfer 50% to your GET account
3. You repay in student-friendly installments

📍 **COVERAGE:** All UB students
💰 **DISCOUNT:** 50% OFF GET app balance
📞 **Contact @yrfrnd_spidy for GET app help**""",
        "keywords": ["half off GET app", "50% off UB meal plan", "UB dining dollars discount", "campus cash assistance"]
    },
    "tuition": {
        "title": "🎓 **UB TUITION 50% OFF**",
        "details": """💰 **PAY HALF FOR UB TUITION:**

✅ **TUITION PAYMENTS 50% OFF:**
• Undergraduate tuition 50% OFF
• Graduate tuition 50% OFF
• International student tuition
• All colleges within UB

✅ **UNIVERSITY FEES 50% OFF:**
• Student activity fees 50% OFF
• Technology fees 50% OFF
• Lab fees 50% OFF
• Health service fees 50% OFF

✅ **TEXTBOOKS & SUPPLIES 50% OFF:**
• All textbooks 50% OFF
• Lab supplies 50% OFF
• Software licenses 50% OFF
• Course materials 50% OFF

📍 **COVERAGE:** All UB programs
💰 **DISCOUNT:** 50% OFF tuition & fees
📞 **Contact @yrfrnd_spidy for tuition help**""",
        "keywords": ["half off UB tuition", "50% off college fees", "university at buffalo tuition assistance", "student payment help"]
    },
    "medical": {
        "title": "🏥 **UB MEDICAL 50% OFF**",
        "details": """💊 **PAY HALF FOR UB MEDICAL:**

✅ **STUDENT HEALTH INSURANCE 50% OFF:**
• UB student health insurance 50% OFF
• UnitedHealthcare student plan
• All premiums 50% OFF

✅ **CAMPUS HEALTH SERVICES 50% OFF:**
• Student Health Center visits 50% OFF
• Counseling Center sessions 50% OFF
• Wellness services 50% OFF

✅ **PRESCRIPTION MEDICATIONS 50% OFF:**
• UB Pharmacy prescriptions 50% OFF
• CVS near campus 50% OFF
• All medications covered

✅ **EMERGENCY MEDICAL 50% OFF:**
• ER visits 50% OFF
• Urgent care 50% OFF
• Ambulance services 50% OFF

📍 **COVERAGE:** All UB students
💰 **DISCOUNT:** 50% OFF medical expenses
📞 **Contact @yrfrnd_spidy for medical help**""",
        "keywords": ["half off student health insurance", "50% off UB medical", "student prescription discount", "campus health services help"]
    },
    "books": {
        "title": "📚 **UB BOOKS 50% OFF**",
        "details": """🎒 **PAY HALF FOR UB TEXTBOOKS:**

✅ **TEXTBOOKS 50% OFF:**
• All textbooks 50% OFF
• New textbooks 50% OFF
• Used textbooks 50% OFF
• Digital textbooks 50% OFF

✅ **UB BOOKSTORE 50% OFF:**
• UB North Campus bookstore 50% OFF
• UB South Campus bookstore 50% OFF
• All bookstore purchases 50% OFF

✅ **ONLINE TEXTBOOKS 50% OFF:**
• Amazon textbooks 50% OFF
• Chegg textbooks 50% OFF
• All online retailers

📍 **COVERAGE:** All UB courses
💰 **DISCOUNT:** 50% OFF all books
📞 **Contact @yrfrnd_spidy for textbook help**""",
        "keywords": ["half off UB textbooks", "50% off college books", "university at buffalo bookstore discount", "student textbook assistance"]
    }
}

# ===== UB CAMPUSES =====
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
        
        "✅ **GET 50% OFF ON ALL UB EXPENSES:**\n"
        "• 🏠 **Housing**: On-campus & off-campus rent\n"
        "• ⚡ **Utilities**: Electricity, internet, water, heating\n"
        "• 📱 **GET App**: Meal plans, dining dollars, campus payments\n"
        "• 🎓 **Tuition**: All UB tuition & fees\n"
        "• 🏥 **Medical**: Health insurance, prescriptions\n"
        "• 📚 **Books**: Textbooks, course materials\n\n"
        
        "📍 **COVERAGE:** Both UB Campuses (North & South)\n"
        "💰 **DISCOUNT:** Guaranteed 50% OFF (Half OFF)\n"
        "⏰ **AVAILABILITY:** 24/7 Student Service\n\n"
        
        "*We pay 100% - You pay 50% back in installments*\n"
        "*No credit check • All UB students eligible*"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Service categories
    keyboard.add(
        types.InlineKeyboardButton("🏠 Housing 50% OFF", callback_data="service_rent"),
        types.InlineKeyboardButton("⚡ Utilities 50% OFF", callback_data="service_utilities")
    )
    keyboard.add(
        types.InlineKeyboardButton("📱 GET App 50% OFF", callback_data="service_get_app"),
        types.InlineKeyboardButton("🎓 Tuition 50% OFF", callback_data="service_tuition")
    )
    keyboard.add(
        types.InlineKeyboardButton("🏥 Medical 50% OFF", callback_data="service_medical"),
        types.InlineKeyboardButton("📚 Books 50% OFF", callback_data="service_books")
    )
    keyboard.add(
        types.InlineKeyboardButton("📍 UB Campuses", callback_data="select_campus"),
        types.InlineKeyboardButton("🔄 How It Works", callback_data="how_it_works")
    )
    
    # Direct contact buttons
    keyboard.add(
        types.InlineKeyboardButton("📞 Contact @yrfrnd_spidy", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Support @Eatsplugsus", url="https://t.me/Eatsplugsus")
    )
    
    keyboard.add(
        types.InlineKeyboardButton("📢 Join Updates", url="https://t.me/flights_bills_b4u")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== SERVICE HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def service_handler(call):
    service_type = call.data.replace('service_', '')
    
    if service_type in UB_SERVICES:
        service = UB_SERVICES[service_type]
        
        response = f"{service['title']}\n\n{service['details']}"
        
        # Add SEO keywords
        seo_section = "\n\n🔍 **Related Searches:** "
        seo_section += ", ".join(service['keywords'])
        response += seo_section
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📞 Get {service_type.title()} Code", callback_data=f"contact_{service_type}"),
            types.InlineKeyboardButton("📍 Select Campus", callback_data="select_campus")
        )
        markup.add(
            types.InlineKeyboardButton("🔙 All Services", callback_data="back_services"),
            types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== CAMPUS SELECTION =====
@bot.callback_query_handler(func=lambda call: call.data == 'select_campus')
def select_campus_handler(call):
    response = """📍 **UB CAMPUSES - 50% PAYMENT SERVICE**

🎯 **Get 50% OFF services at your campus:**

🏢 **NORTH CAMPUS (Amherst):**
• Main academic campus
• Engineering, Business, Arts
• Most on-campus housing
• Ellicott Complex, Governors Complex

🏢 **SOUTH CAMPUS (Buffalo):**
• Medical & professional schools
• Architecture, Law, Nursing
• Goodyear Hall housing
• Medical School, Dental School

💰 **OUR 50% SERVICE COVERS BOTH:**
• All housing on both campuses
• All utilities for both locations
• All campus expenses
• All student needs
• All academic programs

👇 **Select your campus for specific help:**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    markup.add(
        types.InlineKeyboardButton("📍 North Campus", callback_data="campus_north"),
        types.InlineKeyboardButton("📍 South Campus", callback_data="campus_south")
    )
    
    markup.add(
        types.InlineKeyboardButton("🏠 Housing Help", callback_data="service_rent"),
        types.InlineKeyboardButton("⚡ Utilities Help", callback_data="service_utilities")
    )
    
    markup.add(
        types.InlineKeyboardButton("🔙 Back to Services", callback_data="back_services")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('campus_'))
def campus_detail_handler(call):
    campus_type = call.data.replace('campus_', '')
    
    if campus_type in UB_CAMPUSES:
        campus = UB_CAMPUSES[campus_type]
        
        response = f"{campus['name']}\n\n{campus['details']}"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📞 {campus_type.title()} Campus Help", callback_data=f"contact_campus_{campus_type}"),
            types.InlineKeyboardButton("📍 Both Campuses", callback_data="select_campus")
        )
        markup.add(
            types.InlineKeyboardButton("🏠 Housing Help", callback_data="service_rent"),
            types.InlineKeyboardButton("⚡ Utilities Help", callback_data="service_utilities")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'how_it_works')
def how_it_works_handler(call):
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
        types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_services")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== CONTACT HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('contact_'))
def contact_handler(call):
    contact_type = call.data.replace('contact_', '')
    
    if contact_type in ["rent", "utilities", "get_app", "tuition", "medical", "books"]:
        service_name = contact_type.title().replace("_", " ")
        response = f"""📞 **Contact for {service_name} 50% OFF**

🔥 **GET 50% OFF ON {service_name.upper()}:**

🎯 **SPECIALIZED SUPPORT:**

**Primary Contact:** @yrfrnd_spidy
• {service_name} 50% OFF codes
• Service-specific discounts
• UB student verification
• Best deal recommendations

**Support Available:** @Eatsplugsus
• Activation assistance
• Code troubleshooting
• Account linking help
• Refund processing

⏰ **Support:** 24/7
💰 **Discount:** Guaranteed 50% OFF
📍 **Coverage:** Both UB Campuses

🎁 **BONUSES FOR UB STUDENTS:**
• Extra discounts for first-time users
• Referral bonuses
• Seasonal promotions
• Emergency assistance

*Message now for {service_name} 50% OFF codes!*"""
    
    elif contact_type.startswith("campus_"):
        campus_code = contact_type.replace("campus_", "")
        if campus_code in UB_CAMPUSES:
            campus_name = "North Campus" if campus_code == "north" else "South Campus"
            response = f"""📞 **Contact for {campus_name} 50% OFF**

📍 **CAMPUS-SPECIFIC 50% OFF:**

🎯 **{campus_name.upper()} SPECIALISTS:**

**Primary Contact:** @yrfrnd_spidy
• {campus_name} 50% OFF codes
• Campus-specific promotions
• Local housing partnerships
• Regional discounts

**Support:** @Eatsplugsus
• Campus activation help
• Local troubleshooting
• Campus-specific offers
• Delivery assistance

💰 **{campus_name.upper()} BONUSES:**
• Extra 5% OFF for campus residents
• Local restaurant partnerships
• Campus delivery discounts
• Campus event specials

*Message now for {campus_name} 50% OFF codes!*"""
    
    else:
        response = """📞 **Contact for UB 50% Payment Service**

🎓 **GET 50% OFF ALL UB EXPENSES:**

🎯 **MAIN CONTACTS:**

1. **Primary Contact:** @yrfrnd_spidy
   • For all 50% OFF service codes
   • UB student verification
   • Bulk order discounts
   • Corporate accounts

2. **Support Contact:** @Eatsplugsus
   • Technical support
   • Code activation help
   • Account issues
   • Refund assistance

3. **Updates Channel:** @flights_bills_b4u
   • New 50% OFF deals
   • Flash sales alerts
   • Limited time offers
   • Success stories

⏰ **SERVICE HOURS:** 24/7
⏱️ **RESPONSE TIME:** Under 15 minutes
✅ **GUARANTEE:** 50% OFF minimum

💰 **WHAT UB STUDENTS GET:**
• 50% OFF codes for all services
• Campus-specific promotions
• No usage limits
• Permanent discounts
• Priority student support

*Message now for immediate 50% OFF codes!*"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💬 Message Now", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Support", url="https://t.me/Eatsplugsus")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u"),
        types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_services")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BACK HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data == 'back_services')
def back_services_handler(call):
    start_command(call.message)

# ===== ADMIN COMMANDS =====
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin command only.")
        return
    
    user_count = len(broadcast_users)
    
    stats_message = (
        f"📊 **UB 50% PAYMENT BOT STATISTICS**\n\n"
        f"🎓 **University at Buffalo Service**\n\n"
        f"👥 **Total UB Students:** {user_count}\n"
        f"📍 **Campuses Covered:** North & South\n"
        f"💰 **Service Categories:** {len(UB_SERVICES)}\n"
        f"🔍 **SEO Keywords:** {sum(len(v) for v in SEO_KEYWORDS.values())}\n\n"
        f"💰 **Discount:** 50% OFF (Half OFF)\n"
        f"📈 **Growth:** +{min(user_count, 100)} today\n"
        f"⏰ **Status:** ✅ Active & SEO Optimized\n\n"
        f"*Last updated: Just now*"
    )
    
    bot.send_message(ADMIN_ID, stats_message, parse_mode='Markdown')

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin command only.")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No UB students available for broadcast.")
        return
    
    msg = bot.send_message(
        ADMIN_ID, 
        f"📤 Send 50% OFF broadcast to {len(broadcast_users)} UB students:\n\n"
        f"Type your UB 50% OFF deal announcement:"
    )
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    
    message.is_broadcast_processed = True
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    
    status_msg = bot.send_message(ADMIN_ID, f"📤 Sending 50% OFF deals to {len(users)} UB students...")
    
    for user_id in users:
        try:
            notification = (
                f"🎓 **UB 50% PAYMENT ALERT** 🎓\n\n"
                f"{broadcast_text}\n\n"
                f"📍 Both UB Campuses covered\n"
                f"💰 50% OFF guaranteed\n"
                f"📞 Contact for 50% OFF codes!"
            )
            bot.send_message(user_id, notification)
            success_count += 1
        except Exception:
            pass
    
    bot.edit_message_text(
        f"✅ **UB Broadcast Complete!**\n\n"
        f"📊 **Results:**\n"
        f"• ✅ Success: {success_count} students\n"
        f"• 📊 Total: {len(users)} students\n\n"
        f"*50% OFF deal sent successfully!*",
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
        bot.send_message(
            message.chat.id,
            "🎓 **UNIVERSITY AT BUFFALO 50% PAYMENT SERVICE**\n\n"
            "🎯 **Get 50% OFF on all UB expenses:**\n"
            "• Housing • Utilities • GET App\n"
            "• Tuition • Medical • Books\n\n"
            "📍 **Coverage:** Both UB Campuses\n"
            "💰 **Guaranteed 50% OFF**\n\n"
            "📞 **Contact for 50% OFF codes:**\n"
            "• @yrfrnd_spidy (Main contact)\n"
            "• @Eatsplugsus (Support)\n\n"
            "Type /start for all 50% OFF services!"
        )

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
            print(f"✅ UB 50% PAYMENT BOT DEPLOYED!")
            print(f"💰 Discount: 50% OFF ALL UB EXPENSES")
            print(f"📍 Coverage: Both UB Campuses")
            print(f"🔍 SEO Keywords: Optimized for UB")
            print(f"📞 Primary Contact: @yrfrnd_spidy")
            print(f"📞 Support Contact: @Eatsplugsus")
            print(f"📢 Updates Channel: @flights_bills_b4u")
            print(f"👑 Admin ID: {ADMIN_ID}")
        else:
            print("🔧 Running in polling mode")
            
    except Exception as e:
        print(f"⚠️ Webhook setup: {e}")
    
    print("🎓 University at Buffalo 50% Payment Bot Active!")
    print("✅ Services: Housing, Utilities, GET App, Tuition, Medical, Books")
    print("📍 Campuses: North & South Campus coverage")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

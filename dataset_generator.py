import json
import random

# ── Real apps pulled from device via:
#    adb shell pm list packages -i | grep 'installer=com.android.vending'
# Descriptions sourced from Google Play Store short descriptions.
# System-only / non-user-facing packages are excluded.

APPS_POOL = [
    # ── Travel & Transport ──
    {"label": "Uber", "packageName": "com.ubercab", "category": "rideshare", "desc": "Request rides, order food delivery, taxi, car service transportation"},
    {"label": "inDrive", "packageName": "sinet.startup.inDriver", "category": "rideshare", "desc": "Negotiate ride prices, taxi service, affordable transportation"},
    {"label": "Airbnb", "packageName": "com.airbnb.android", "category": "travel", "desc": "Book vacation rentals, homes, unique stays, travel accommodation"},
    {"label": "Vrbo", "packageName": "com.vrbo.android", "category": "travel", "desc": "Vacation rental homes, beach houses, cabin stays, family travel"},
    {"label": "Booking.com", "packageName": "com.booking", "category": "travel", "desc": "Book hotels, flights, rental cars, travel deals accommodations"},
    {"label": "American Airlines", "packageName": "com.aa.android", "category": "airline", "desc": "Book flights, check in, boarding pass, flight status tracker"},
    {"label": "Delta", "packageName": "com.delta.mobile.android", "category": "airline", "desc": "Book flights, check in, boarding pass, SkyMiles rewards"},
    {"label": "Southwest Airlines", "packageName": "com.southwestairlines.mobile", "category": "airline", "desc": "Book flights, check in, boarding pass, flight status tracker"},
    {"label": "Frontier Airlines", "packageName": "com.flyfrontier.android", "category": "airline", "desc": "Book budget flights, check in, boarding pass, flight deals"},
    {"label": "United Airlines", "packageName": "com.united.mobile.android", "category": "airline", "desc": "Book flights, check in, boarding pass, MileagePlus rewards"},
    {"label": "Eurail Rail Planner", "packageName": "org.eurail.railplanner", "category": "transit", "desc": "Plan European train trips, rail passes, train schedules timetables"},
    {"label": "Transit", "packageName": "com.thetransitapp.droid", "category": "transit", "desc": "Real-time bus and train tracker, public transit navigation schedules"},
    {"label": "RTD Denver", "packageName": "com.justride.rtddenver", "category": "transit", "desc": "Buy Denver bus and train tickets, RTD transit passes"},
    {"label": "Moovit", "packageName": "com.tranzmate", "category": "transit", "desc": "Public transit directions, bus train schedules, real-time arrivals"},
    {"label": "Waze", "packageName": "com.waze", "category": "navigation", "desc": "GPS navigation, real-time traffic alerts, driving directions, road reports"},
    {"label": "Google Maps", "packageName": "com.google.android.apps.maps", "category": "navigation", "desc": "Navigation, directions, GPS, traffic, explore nearby places restaurants"},
    {"label": "Mapy.cz", "packageName": "cz.seznam.mapy", "category": "navigation", "desc": "Offline maps, hiking trails, cycling routes, outdoor navigation"},
    {"label": "Android Auto", "packageName": "com.google.android.projection.gearhead", "category": "automotive", "desc": "Car display for maps, music, calls, messaging while driving"},
    {"label": "Saily", "packageName": "com.saily.android", "category": "travel", "desc": "Buy eSIM for international travel, mobile data abroad"},
    {"label": "CBP One", "packageName": "gov.dhs.cbp.pspd.mpc", "category": "travel", "desc": "US customs, border crossing, travel entry, passport control immigration"},
    {"label": "Steamboat Springs Shuttle", "packageName": "com.downtownerapp.steamboat", "category": "local_transit", "desc": "Free shuttle rides, local transportation, Steamboat Springs transit"},

    # ── Food & Dining ──
    {"label": "DoorDash", "packageName": "com.dd.doordash", "category": "food_delivery", "desc": "Order food delivery, restaurant takeout, grocery delivery service"},
    {"label": "Taco Bell", "packageName": "com.tacobell.ordering", "category": "food_ordering", "desc": "Order fast food, tacos, burritos, Mexican food pickup delivery"},
    {"label": "Safeway", "packageName": "com.safeway.client.android.safeway", "category": "grocery", "desc": "Grocery shopping, deals, coupons, pharmacy, delivery pickup orders"},
    {"label": "Jewel-Osco", "packageName": "com.safeway.client.android.jewelosco", "category": "grocery", "desc": "Grocery shopping, deals, coupons, pharmacy, delivery pickup orders"},
    {"label": "inKind", "packageName": "com.inkind.inkind", "category": "dining", "desc": "Restaurant credits, dining deals, buy gift cards, food savings"},
    {"label": "Denver Burger Week", "packageName": "com.westword.denverburgerweek", "category": "dining", "desc": "Denver burger deals, restaurant specials, local food events"},

    # ── Finance ──
    {"label": "Bank of America", "packageName": "com.infonow.bofa", "category": "banking", "desc": "Mobile banking, check balances, pay bills, transfer money deposits"},
    {"label": "Capital One", "packageName": "com.konylabs.capitalone", "category": "banking", "desc": "Mobile banking, credit cards, check balances, pay bills, rewards"},
    {"label": "Fidelity Investments", "packageName": "com.fidelity.android", "category": "investing", "desc": "Invest in stocks, mutual funds, retirement accounts, portfolio tracking"},
    {"label": "Fidelity NetBenefits", "packageName": "com.fidelity.wi.activity", "category": "investing", "desc": "Check 401k retirement benefits, workplace savings, employer stock plan"},
    {"label": "USAA", "packageName": "com.usaa.mobile.android.usaa", "category": "banking", "desc": "Military banking, insurance, check balances, pay bills, deposit checks"},
    {"label": "Venmo", "packageName": "com.venmo", "category": "payments", "desc": "Send money to friends, split bills, mobile payments, pay people"},
    {"label": "Google Wallet", "packageName": "com.google.android.apps.walletnfcrel", "category": "payments", "desc": "Contactless payments, store cards, boarding passes, digital wallet NFC"},
    {"label": "USAA SafePilot", "packageName": "com.usaa.mobile.android.safedriving", "category": "insurance", "desc": "Track driving habits, earn safe driving discounts, auto insurance savings"},

    # ── Communication ──
    {"label": "WhatsApp", "packageName": "com.whatsapp", "category": "messaging", "desc": "Send messages, group chats, voice and video calls, share photos"},
    {"label": "Signal", "packageName": "org.thoughtcrime.securesms", "category": "messaging", "desc": "Encrypted private messaging, secure calls, disappearing messages privacy"},
    {"label": "Slack", "packageName": "com.Slack", "category": "work_messaging", "desc": "Workplace messaging, team channels, business chat, file sharing collaboration"},
    {"label": "Gmail", "packageName": "com.google.android.gm", "category": "email", "desc": "Read and send email, inbox management, email attachments notifications"},
    {"label": "Google Messages", "packageName": "com.google.android.apps.messaging", "category": "messaging", "desc": "Send text messages SMS, RCS chat, group messaging, photos"},
    {"label": "Google Meet", "packageName": "com.google.android.apps.tachyon", "category": "video_calling", "desc": "Video calls, video meetings, group video chat, screen sharing"},
    {"label": "Discord", "packageName": "com.discord", "category": "messaging", "desc": "Voice chat, gaming communities, group messaging, server channels"},
    {"label": "Zoom", "packageName": "us.zoom.videomeetings", "category": "video_calling", "desc": "Video meetings, conference calls, webinars, screen sharing virtual"},
    {"label": "Garmin Messenger", "packageName": "com.garmin.android.apps.messenger", "category": "messaging", "desc": "Satellite messaging, off-grid communication, GPS location sharing outdoor"},

    # ── Music & Audio ──
    {"label": "Spotify", "packageName": "com.spotify.music", "category": "music", "desc": "Stream music, playlists, podcasts, songs, discover new artists albums"},
    {"label": "YouTube Music", "packageName": "com.google.android.apps.youtube.music", "category": "music", "desc": "Stream music, music videos, playlists, songs, albums artists"},
    {"label": "GuitarTuna", "packageName": "com.ovelin.guitartuna", "category": "music_tools", "desc": "Tune guitar, instrument tuner, chords, metronome, learn songs"},
    {"label": "Sony Headphones Connect", "packageName": "com.sony.songpal.mdr", "category": "audio", "desc": "Control Sony headphones, noise canceling settings, equalizer sound"},
    {"label": "Smart AudioBook Player", "packageName": "ak.alizandro.smartaudiobookplayer", "category": "audiobooks", "desc": "Listen to audiobooks, bookmarks, sleep timer, playback speed control"},

    # ── Entertainment & Media ──
    {"label": "Google TV", "packageName": "com.google.android.videos", "category": "streaming", "desc": "Watch movies, TV shows, stream video content, rent buy films"},
    {"label": "Max", "packageName": "com.wbd.stream", "category": "streaming", "desc": "Stream HBO shows, movies, originals, documentaries, series binge watch"},
    {"label": "Dropout", "packageName": "com.collegehumor.chdropout", "category": "streaming", "desc": "Watch comedy shows, game shows, original series, sketch comedy streaming"},
    {"label": "NYT", "packageName": "com.nytimes.android", "category": "news", "desc": "Read news articles, breaking news, politics, opinion, world journalism"},
    {"label": "Chrome", "packageName": "com.android.chrome", "category": "browser", "desc": "Web browser, search internet, browse websites, tabs, bookmarks"},
    {"label": "Samsung Internet", "packageName": "com.sec.android.app.sbrowser", "category": "browser", "desc": "Web browser, search internet, browse websites, ad blocker privacy"},

    # ── Reading & Books ──
    {"label": "Libby", "packageName": "com.overdrive.mobile.android.libby", "category": "reading", "desc": "Borrow library ebooks, audiobooks, free digital library reading"},
    {"label": "The StoryGraph", "packageName": "com.thestorygraph.thestorygraph", "category": "reading", "desc": "Track books reading, book recommendations, reading stats reviews lists"},

    # ── Shopping ──
    {"label": "Amazon Shopping", "packageName": "com.amazon.mShop.android.shopping", "category": "shopping", "desc": "Shop online, buy products, deals, package tracking, delivery orders"},
    {"label": "REI Co-op", "packageName": "com.ubermind.rei", "category": "shopping", "desc": "Shop outdoor gear, camping hiking equipment, member deals coupons"},
    {"label": "Shop", "packageName": "com.shopify.arrive", "category": "shopping", "desc": "Track packages, delivery tracking, order updates, shopping deals"},

    # ── Productivity ──
    {"label": "Todoist", "packageName": "com.todoist", "category": "productivity", "desc": "Task manager, to-do lists, project planning, reminders organization"},
    {"label": "Google Keep", "packageName": "com.google.android.keep", "category": "notes", "desc": "Quick notes, checklists, reminders, voice memos, save ideas lists"},
    {"label": "Google Calendar", "packageName": "com.google.android.calendar", "category": "calendar", "desc": "Schedule events, calendar, meetings, reminders, appointments planner"},
    {"label": "Google Drive", "packageName": "com.google.android.apps.docs", "category": "cloud_storage", "desc": "Cloud file storage, share documents, backup photos, access files"},
    {"label": "Google Sheets", "packageName": "com.google.android.apps.docs.editors.sheets", "category": "productivity", "desc": "Create edit spreadsheets, data tables, formulas, collaborative worksheets"},
    {"label": "OneDrive", "packageName": "com.microsoft.skydrive", "category": "cloud_storage", "desc": "Cloud file storage, backup photos, share documents, Microsoft files"},
    {"label": "Adobe Scan", "packageName": "com.adobe.scan.android", "category": "productivity", "desc": "Scan documents to PDF, camera scanner, OCR text recognition"},
    {"label": "Tasker", "packageName": "net.dinglisch.android.taskerm", "category": "automation", "desc": "Automate phone tasks, custom actions, triggers, profiles scripting"},
    {"label": "Google Photos", "packageName": "com.google.android.apps.photos", "category": "photos", "desc": "Photo gallery, backup pictures, edit photos, share memories albums"},

    # ── Health & Fitness ──
    {"label": "MapMyRun", "packageName": "com.mapmyrun.android2", "category": "fitness", "desc": "Track running routes, GPS workout tracker, distance pace calories"},
    {"label": "Samsung Health", "packageName": "com.sec.android.app.shealth", "category": "health", "desc": "Track steps, fitness goals, heart rate, sleep, workout exercise"},
    {"label": "Garmin Explore", "packageName": "com.garmin.android.apps.explore", "category": "outdoor", "desc": "Download maps, plan outdoor trips, track GPS routes waypoints"},
    {"label": "UCHealth", "packageName": "com.uchealth.mobile", "category": "healthcare", "desc": "Medical appointments, health records, message doctor, prescriptions labs"},
    {"label": "MyChart", "packageName": "epic.mychart.android", "category": "healthcare", "desc": "Medical appointments, health records, test results, message doctor telehealth"},
    {"label": "How We Feel", "packageName": "org.howwefeel.moodmeter", "category": "wellness", "desc": "Track emotions, mood journal, mental wellness, feelings check-in log"},

    # ── Education & Language ──
    {"label": "Babbel", "packageName": "com.babbel.mobile.android.en", "category": "education", "desc": "Learn languages, Spanish French German lessons, vocabulary practice speaking"},
    {"label": "Google Translate", "packageName": "com.google.android.apps.translate", "category": "translation", "desc": "Translate text, camera translation, conversations, 100+ languages"},

    # ── Outdoor & Activity ──
    {"label": "Outdooractive", "packageName": "com.outdooractive.Outdooractive", "category": "outdoor", "desc": "Hiking trail maps, cycling routes, outdoor activities, GPS navigation"},
    {"label": "Wikiloc", "packageName": "com.wikiloc.wikilocandroid", "category": "outdoor", "desc": "Hiking GPS trails, outdoor routes, mountain biking, nature walks"},
    {"label": "SkyView", "packageName": "com.t11.skyview", "category": "education", "desc": "Identify stars, constellations, planets, stargazing, night sky astronomy"},
    {"label": "VoiceMap", "packageName": "me.voicemap.android", "category": "travel", "desc": "GPS audio walking tours, sightseeing guide, explore cities narrated"},
    {"label": "Ikon Pass", "packageName": "com.alterramtnco.ikonpass", "category": "skiing", "desc": "Ski resort pass, mountain access, lift tickets, ski resort maps"},

    # ── Events & Tickets ──
    {"label": "Ticketmaster", "packageName": "com.ticketmaster.mobile.android.na", "category": "events", "desc": "Buy concert tickets, sports events, shows, live entertainment venues"},
    {"label": "AXS", "packageName": "com.axs.android", "category": "events", "desc": "Buy event tickets, concerts, sports, venue shows, live events"},
    {"label": "Timeleft", "packageName": "com.timeleft.app", "category": "social", "desc": "Meet strangers at dinner events, social dining, make new friends"},
    {"label": "Bar Crawl Nation", "packageName": "com.barcrawlnation", "category": "social", "desc": "Bar crawl events, nightlife, pub crawls, drinking social events"},

    # ── Smart Home & IoT ──
    {"label": "Philips Hue", "packageName": "com.philips.lighting.hue2", "category": "smart_home", "desc": "Control smart lights, set scenes, color lighting, home automation"},
    {"label": "TP-Link Tether", "packageName": "com.tplink.tether", "category": "networking", "desc": "Manage WiFi router, network settings, parental controls, device management"},
    {"label": "Comelit", "packageName": "com.comelit.bigapp", "category": "smart_home", "desc": "Smart home intercom, door entry, video doorbell, security system"},
    {"label": "STRATIS IoT", "packageName": "com.stratisiot.mobile", "category": "smart_home", "desc": "Smart apartment access, building entry, IoT property management locks"},
    {"label": "Google Home", "packageName": "com.google.android.apps.chromecast.app", "category": "smart_home", "desc": "Control smart home devices, Chromecast, speakers, lights, cameras"},
    {"label": "Galaxy Wearable", "packageName": "com.samsung.android.app.watchmanager", "category": "wearable", "desc": "Manage Samsung Galaxy Watch, earbuds, wearable device settings"},

    # ── Security & VPN ──
    {"label": "1Password", "packageName": "com.onepassword.android", "category": "security", "desc": "Password manager, secure login, store passwords, autofill credentials"},
    {"label": "LastPass Authenticator", "packageName": "com.lastpass.authenticator", "category": "security", "desc": "Two-factor authentication codes, 2FA, login verification security"},
    {"label": "Proton VPN", "packageName": "ch.protonvpn.android", "category": "vpn", "desc": "Secure VPN, private internet, encrypted browsing, hide IP address"},

    # ── Games ──
    {"label": "Chess.com", "packageName": "com.chess", "category": "games", "desc": "Play chess online, puzzles, lessons, tournaments, chess analysis"},
    {"label": "Chess Clock", "packageName": "com.chess.clock", "category": "games", "desc": "Chess timer, game clock, tournament timing, board game timer"},
    {"label": "D&D Beyond", "packageName": "com.fandom.playercompanion", "category": "games", "desc": "Dungeons and Dragons character sheets, dice roller, D&D digital tools"},
    {"label": "Wingspan", "packageName": "com.MonsterCouch.Wingspan", "category": "games", "desc": "Bird strategy board game, card game, nature collecting competitive"},
    {"label": "Poker Trainer", "packageName": "nu.Pokertrainer.Pokertrainer", "category": "games", "desc": "Practice poker strategy, Texas holdem training, card game odds"},
    {"label": "Crossword", "packageName": "mobi.redstonegames.crossword.en", "category": "games", "desc": "Crossword puzzles, word games, brain teasers, vocabulary puzzle"},

    # ── Parking & Local Services ──
    {"label": "PayByPhone", "packageName": "com.paybyphone", "category": "parking", "desc": "Pay for parking, meter payment, parking sessions, digital parking"},
    {"label": "Parking.com", "packageName": "com.spplus.parking", "category": "parking", "desc": "Reserve parking spots, garage parking, airport parking, prepay lots"},
    {"label": "myColorado", "packageName": "com.soc.mycolorado", "category": "government", "desc": "Colorado digital ID, driver license, vehicle registration, state services"},

    # ── Utility & Other ──
    {"label": "Miofive", "packageName": "com.miofive.dvr", "category": "automotive", "desc": "Dashcam viewer, driving video recorder, car camera footage review"},
    {"label": "Loud Alarm Clock", "packageName": "me.jlabs.loudalarmclock", "category": "utility", "desc": "Wake up alarm, loud ringtones, heavy sleeper alarm clock timer"},
    {"label": "Gemini", "packageName": "com.google.android.apps.bard", "category": "ai_assistant", "desc": "AI assistant, ask questions, generate text, creative help chatbot"},
    {"label": "Google", "packageName": "com.google.android.googlequicksearchbox", "category": "search", "desc": "Search the web, Google search, discover news, trending information"},
    {"label": "Tracker", "packageName": "my.tracker", "category": "utility", "desc": "GPS item tracker, find lost items, locate belongings, Bluetooth tracker"},
    {"label": "Meteoblue", "packageName": "com.meteoblue.droid", "category": "weather", "desc": "Weather forecast, radar, precipitation, temperature, wind conditions outlook"},
    {"label": "Bubble Level", "packageName": "bubblelevel.level.leveltool.leveler", "category": "utility", "desc": "Spirit level tool, measure angles, surface leveling, calibration inclinometer"},
    {"label": "Photo Collage", "packageName": "photocollage.photoeditor.collagemaker", "category": "photo_editing", "desc": "Make photo collages, edit pictures, add filters, frames layouts"},
    {"label": "AppBlock", "packageName": "cz.mobilesoft.appblock", "category": "utility", "desc": "Block distracting apps, screen time limits, focus mode, digital wellbeing"},
    {"label": "BuzzKill", "packageName": "com.samruston.buzzkill", "category": "utility", "desc": "Manage notifications, filter alerts, notification rules, auto-dismiss control"},
    {"label": "Fetch Package", "packageName": "com.fetchpackage.resident", "category": "utility", "desc": "Package delivery notifications, apartment mailroom, pickup locker alerts"},
    {"label": "GeoBlue", "packageName": "com.hthworldwide.BlueCard", "category": "insurance", "desc": "Travel health insurance, find doctors abroad, international medical coverage"},
    {"label": "Find My Device", "packageName": "com.google.android.apps.adm", "category": "utility", "desc": "Find lost phone, locate device, ring phone, erase data remotely"},
    {"label": "Aura Frames", "packageName": "com.pushd.client", "category": "smart_home", "desc": "Digital photo frame, share photos to Aura frame, family photo display"},
    {"label": "VIP Access", "packageName": "com.verisign.mvip.main", "category": "security", "desc": "Two-factor authentication, security codes, Symantec VIP login verification"},
    {"label": "GalaPro", "packageName": "com.galapro.app", "category": "accessibility", "desc": "Theater accessibility, live captioning, audio description for performances"},
    {"label": "Co-Op Colorado", "packageName": "co.op.colorado", "category": "rideshare", "desc": "Worker-owned rideshare, book cooperative rides, Colorado ride-hailing"},
    {"label": "Amazon A to Z", "packageName": "com.amazon.atozm", "category": "work", "desc": "Amazon employee work schedule, shifts, pay, time off, HR management"},
    {"label": "FUTO Keyboard", "packageName": "org.futo.inputmethod.latin.playstore", "category": "utility", "desc": "Privacy keyboard, typing, swipe input, voice typing, offline keyboard"},
]

# ── Semantic intent queries ──
# Each entry: (query_text, list_of_labels_that_should_match)
# These represent natural-language user intents mapped to installed apps.

SEMANTIC_INTENTS = [
    # ── Rideshare / Transport ──
    ("i need a ride", ["Uber", "inDrive", "Co-Op Colorado"]),
    ("get me a car", ["Uber", "inDrive", "Co-Op Colorado"]),
    ("book a taxi", ["Uber", "inDrive"]),
    ("call me an uber", ["Uber"]),
    ("order a ride home", ["Uber", "inDrive"]),
    ("i need to get to the airport", ["Uber", "inDrive"]),

    # ── Navigation & Directions ──
    ("find directions to home", ["Google Maps", "Waze"]),
    ("navigate to work", ["Google Maps", "Waze"]),
    ("whats the fastest way to the store", ["Google Maps", "Waze"]),
    ("show me traffic", ["Google Maps", "Waze"]),
    ("how do i get to downtown", ["Google Maps", "Waze"]),
    ("i need to look up an address", ["Google Maps", "Waze"]),
    ("find a gas station near me", ["Google Maps"]),
    ("where is the nearest coffee shop", ["Google Maps"]),

    # ── Public Transit ──
    ("when is the next bus", ["Transit", "RTD Denver", "Moovit"]),
    ("buy a bus ticket", ["RTD Denver", "Transit"]),
    ("check the train schedule", ["Transit", "Moovit", "Eurail Rail Planner"]),
    ("whats my bus eta", ["Transit", "Moovit"]),
    ("plan a train trip in europe", ["Eurail Rail Planner"]),
    ("i need to catch the light rail", ["RTD Denver", "Transit"]),

    # ── Flights & Air Travel ──
    ("check my flight status", ["American Airlines", "Delta", "Southwest Airlines", "Frontier Airlines", "United Airlines"]),
    ("i need to check in for my flight", ["American Airlines", "Delta", "Southwest Airlines", "Frontier Airlines", "United Airlines"]),
    ("get my boarding pass", ["American Airlines", "Delta", "Southwest Airlines", "Frontier Airlines", "United Airlines"]),
    ("book a flight", ["American Airlines", "Delta", "Southwest Airlines", "Frontier Airlines", "United Airlines", "Booking.com"]),
    ("check my delta flight", ["Delta"]),
    ("pull up my southwest boarding pass", ["Southwest Airlines"]),
    ("i fly american", ["American Airlines"]),

    # ── Hotels & Accommodation ──
    ("find a hotel", ["Booking.com", "Airbnb", "Vrbo"]),
    ("book a vacation rental", ["Airbnb", "Vrbo"]),
    ("find a place to stay tonight", ["Booking.com", "Airbnb"]),
    ("book an airbnb", ["Airbnb"]),
    ("search for a cabin", ["Vrbo", "Airbnb"]),
    ("i need accommodation for my trip", ["Booking.com", "Airbnb", "Vrbo"]),

    # ── Music ──
    ("play some music", ["Spotify", "YouTube Music"]),
    ("listen to music", ["Spotify", "YouTube Music"]),
    ("play my playlist", ["Spotify", "YouTube Music"]),
    ("put on some songs", ["Spotify", "YouTube Music"]),
    ("play something chill", ["Spotify", "YouTube Music"]),
    ("i want to listen to a podcast", ["Spotify"]),
    ("find a new album to listen to", ["Spotify", "YouTube Music"]),
    ("play my spotify", ["Spotify"]),

    # ── Audiobooks & Reading ──
    ("listen to an audiobook", ["Smart AudioBook Player", "Libby"]),
    ("continue my book", ["Smart AudioBook Player", "Libby", "The StoryGraph"]),
    ("borrow a book from the library", ["Libby"]),
    ("what should i read next", ["The StoryGraph", "Libby"]),
    ("track my reading", ["The StoryGraph"]),
    ("find a free ebook", ["Libby"]),

    # ── Messaging ──
    ("send a message", ["WhatsApp", "Signal", "Google Messages"]),
    ("text my friend", ["WhatsApp", "Signal", "Google Messages"]),
    ("call my mom on whatsapp", ["WhatsApp"]),
    ("send a secure message", ["Signal"]),
    ("open my chats", ["WhatsApp", "Signal", "Google Messages", "Discord"]),
    ("i need to message someone privately", ["Signal", "WhatsApp"]),
    ("check my text messages", ["Google Messages"]),
    ("send a group text", ["WhatsApp", "Google Messages"]),

    # ── Email ──
    ("check my email", ["Gmail"]),
    ("send an email", ["Gmail"]),
    ("read my inbox", ["Gmail"]),
    ("i have an email to reply to", ["Gmail"]),

    # ── Work Communication ──
    ("check my work messages", ["Slack"]),
    ("open slack", ["Slack"]),
    ("i have a meeting", ["Zoom", "Google Meet"]),
    ("join a video call", ["Zoom", "Google Meet"]),
    ("start a zoom meeting", ["Zoom"]),
    ("hop on a video call", ["Zoom", "Google Meet"]),
    ("join the team standup", ["Zoom", "Google Meet", "Slack"]),
    ("message my coworker", ["Slack"]),
    ("check my discord", ["Discord"]),
    ("join a voice channel", ["Discord"]),

    # ── Video Calling ──
    ("facetime my friend", ["Google Meet", "Zoom", "WhatsApp"]),
    ("video call my family", ["Google Meet", "WhatsApp", "Zoom"]),
    ("start a video chat", ["Google Meet", "WhatsApp", "Zoom"]),

    # ── Streaming & TV ──
    ("watch something", ["Max", "Google TV", "Dropout"]),
    ("i want to watch a movie", ["Max", "Google TV"]),
    ("stream a show", ["Max", "Google TV", "Dropout"]),
    ("put on hbo", ["Max"]),
    ("what should i watch tonight", ["Max", "Google TV", "Dropout"]),
    ("watch dropout", ["Dropout"]),

    # ── News ──
    ("read the news", ["NYT", "Google"]),
    ("show me todays headlines", ["NYT", "Google"]),
    ("catch up on whats happening", ["NYT"]),
    ("check nyt", ["NYT"]),

    # ── Food Delivery ──
    ("order food", ["DoorDash", "Taco Bell"]),
    ("get food delivered", ["DoorDash"]),
    ("im hungry order something", ["DoorDash"]),
    ("order doordash", ["DoorDash"]),
    ("i want tacos", ["Taco Bell", "DoorDash"]),
    ("order taco bell", ["Taco Bell"]),

    # ── Grocery ──
    ("order groceries", ["Safeway", "Jewel-Osco", "DoorDash"]),
    ("check grocery deals", ["Safeway", "Jewel-Osco"]),
    ("i need to go grocery shopping", ["Safeway", "Jewel-Osco"]),
    ("clip some coupons", ["Safeway", "Jewel-Osco"]),

    # ── Finance & Banking ──
    ("check my bank account", ["Bank of America", "Capital One", "USAA"]),
    ("check my balance", ["Bank of America", "Capital One", "USAA"]),
    ("pay my credit card bill", ["Bank of America", "Capital One", "USAA"]),
    ("transfer some money", ["Bank of America", "Capital One", "USAA", "Venmo"]),
    ("deposit a check", ["Bank of America", "Capital One", "USAA"]),
    ("pay my friend back", ["Venmo"]),
    ("split the bill", ["Venmo"]),
    ("send money on venmo", ["Venmo"]),
    ("check my investments", ["Fidelity Investments"]),
    ("look at my portfolio", ["Fidelity Investments"]),
    ("check my 401k", ["Fidelity NetBenefits"]),
    ("view my retirement savings", ["Fidelity NetBenefits", "Fidelity Investments"]),

    # ── Payments ──
    ("pay with my phone", ["Google Wallet"]),
    ("use tap to pay", ["Google Wallet"]),
    ("pull up my wallet", ["Google Wallet"]),

    # ── Shopping ──
    ("buy something online", ["Amazon Shopping"]),
    ("order from amazon", ["Amazon Shopping"]),
    ("track my package", ["Amazon Shopping", "Shop"]),
    ("where is my delivery", ["Amazon Shopping", "Shop", "Fetch Package"]),
    ("shop for outdoor gear", ["REI Co-op"]),
    ("i need camping equipment", ["REI Co-op"]),
    ("check my order status", ["Amazon Shopping", "Shop"]),

    # ── Productivity & Tasks ──
    ("check my todo list", ["Todoist"]),
    ("add a task", ["Todoist"]),
    ("what do i have to do today", ["Todoist", "Google Calendar"]),
    ("create a reminder", ["Todoist", "Google Keep", "Google Calendar"]),
    ("take a quick note", ["Google Keep"]),
    ("jot something down", ["Google Keep"]),
    ("write a note", ["Google Keep"]),
    ("whats on my calendar", ["Google Calendar"]),
    ("check my schedule", ["Google Calendar"]),
    ("schedule a meeting", ["Google Calendar"]),
    ("when is my next appointment", ["Google Calendar"]),

    # ── Cloud Storage & Files ──
    ("access my files", ["Google Drive", "OneDrive"]),
    ("open my documents", ["Google Drive", "OneDrive"]),
    ("upload a file", ["Google Drive", "OneDrive"]),
    ("share a document", ["Google Drive", "OneDrive"]),
    ("open a spreadsheet", ["Google Sheets"]),
    ("scan a document", ["Adobe Scan"]),
    ("scan this receipt", ["Adobe Scan"]),

    # ── Photos ──
    ("look at my photos", ["Google Photos"]),
    ("backup my pictures", ["Google Photos"]),
    ("find a photo from last week", ["Google Photos"]),
    ("edit a photo", ["Google Photos", "Photo Collage"]),
    ("make a photo collage", ["Photo Collage"]),

    # ── Health & Fitness ──
    ("track my run", ["MapMyRun", "Samsung Health"]),
    ("start a workout", ["MapMyRun", "Samsung Health"]),
    ("how many steps did i take", ["Samsung Health"]),
    ("check my heart rate", ["Samsung Health"]),
    ("log a run", ["MapMyRun", "Samsung Health"]),
    ("go for a jog", ["MapMyRun"]),

    # ── Healthcare & Medical ──
    ("schedule a doctor appointment", ["UCHealth", "MyChart"]),
    ("check my test results", ["UCHealth", "MyChart"]),
    ("message my doctor", ["UCHealth", "MyChart"]),
    ("view my medical records", ["UCHealth", "MyChart"]),
    ("refill my prescription", ["UCHealth", "MyChart"]),
    ("book a telehealth visit", ["MyChart", "UCHealth"]),

    # ── Mental Wellness ──
    ("log my mood", ["How We Feel"]),
    ("how am i feeling today", ["How We Feel"]),
    ("do a feelings check in", ["How We Feel"]),
    ("track my emotions", ["How We Feel"]),

    # ── Language Learning ──
    ("practice my spanish", ["Babbel"]),
    ("learn a new language", ["Babbel"]),
    ("study german", ["Babbel"]),
    ("do a language lesson", ["Babbel"]),
    ("translate this", ["Google Translate"]),
    ("what does this word mean in french", ["Google Translate"]),
    ("translate a sign", ["Google Translate"]),

    # ── Outdoor & Hiking ──
    ("find a hiking trail", ["Outdooractive", "Wikiloc", "Garmin Explore"]),
    ("plan a hike", ["Outdooractive", "Wikiloc", "Garmin Explore"]),
    ("track my hike on gps", ["Wikiloc", "Outdooractive", "Garmin Explore"]),
    ("find a cycling route", ["Outdooractive", "Wikiloc"]),
    ("download offline maps for hiking", ["Garmin Explore", "Outdooractive", "Mapy.cz"]),
    ("whats that star", ["SkyView"]),
    ("identify that constellation", ["SkyView"]),
    ("look at the night sky", ["SkyView"]),
    ("check my ikon pass", ["Ikon Pass"]),
    ("check ski conditions", ["Ikon Pass"]),

    # ── Events & Tickets ──
    ("buy concert tickets", ["Ticketmaster", "AXS"]),
    ("find events near me", ["Ticketmaster", "AXS"]),
    ("get tickets to a show", ["Ticketmaster", "AXS"]),
    ("check my event tickets", ["Ticketmaster", "AXS"]),
    ("find something fun to do tonight", ["Ticketmaster", "AXS", "Timeleft", "Bar Crawl Nation"]),
    ("meet new people", ["Timeleft"]),
    ("sign up for a dinner event", ["Timeleft"]),

    # ── Smart Home ──
    ("turn on the lights", ["Philips Hue", "Google Home"]),
    ("dim the lights", ["Philips Hue", "Google Home"]),
    ("set a light scene", ["Philips Hue"]),
    ("control my smart home", ["Google Home", "Philips Hue"]),
    ("cast to my tv", ["Google Home"]),
    ("open the front door", ["Comelit", "STRATIS IoT"]),
    ("buzz someone in", ["Comelit", "STRATIS IoT"]),
    ("unlock my apartment", ["STRATIS IoT"]),
    ("check the doorbell camera", ["Comelit", "Google Home"]),

    # ── WiFi & Networking ──
    ("manage my wifi", ["TP-Link Tether"]),
    ("check my router", ["TP-Link Tether"]),
    ("restart the wifi", ["TP-Link Tether"]),

    # ── Security & Passwords ──
    ("find my password", ["1Password"]),
    ("look up a login", ["1Password"]),
    ("i forgot my password", ["1Password"]),
    ("get my 2fa code", ["LastPass Authenticator"]),
    ("get my authenticator code", ["LastPass Authenticator"]),
    ("connect to vpn", ["Proton VPN"]),
    ("turn on my vpn", ["Proton VPN"]),
    ("browse privately", ["Proton VPN", "Samsung Internet"]),
    ("get my security code", ["LastPass Authenticator", "VIP Access"]),
    ("symantec vip code", ["VIP Access"]),

    # ── Games ──
    ("play a game", ["Chess.com", "Wingspan", "Crossword", "Poker Trainer", "D&D Beyond"]),
    ("play chess", ["Chess.com"]),
    ("do a crossword puzzle", ["Crossword"]),
    ("play wingspan", ["Wingspan"]),
    ("practice poker", ["Poker Trainer"]),
    ("start the chess clock", ["Chess Clock"]),
    ("set up a game timer", ["Chess Clock"]),
    ("roll some dice", ["D&D Beyond"]),
    ("check my dnd character", ["D&D Beyond"]),
    ("open my character sheet", ["D&D Beyond"]),

    # ── Parking ──
    ("pay for parking", ["PayByPhone", "Parking.com"]),
    ("extend my parking", ["PayByPhone"]),
    ("find parking near me", ["Parking.com"]),
    ("reserve a parking spot", ["Parking.com"]),

    # ── Weather ──
    ("whats the weather", ["Meteoblue"]),
    ("check the forecast", ["Meteoblue"]),
    ("is it going to rain today", ["Meteoblue"]),
    ("weather this weekend", ["Meteoblue"]),

    # ── Utility ──
    ("set an alarm", ["Loud Alarm Clock"]),
    ("wake me up at 7", ["Loud Alarm Clock"]),
    ("i need a level tool", ["Bubble Level"]),
    ("is this surface level", ["Bubble Level"]),
    ("find my phone", ["Find My Device", "Tracker"]),
    ("where did i leave my keys", ["Tracker"]),
    ("find my lost item", ["Tracker"]),
    ("tune my guitar", ["GuitarTuna"]),
    ("i need a tuner", ["GuitarTuna"]),
    ("check my dashcam footage", ["Miofive"]),
    ("review dashcam video", ["Miofive"]),
    ("check on my package delivery", ["Fetch Package", "Shop", "Amazon Shopping"]),
    ("my package arrived", ["Fetch Package"]),
    ("show my digital id", ["myColorado"]),
    ("pull up my drivers license", ["myColorado"]),

    # ── AI / Search ──
    ("ask ai a question", ["Gemini"]),
    ("help me write something", ["Gemini"]),
    ("ask gemini", ["Gemini"]),
    ("search for something", ["Google", "Chrome"]),
    ("google something", ["Google", "Chrome"]),
    ("look something up", ["Google", "Chrome"]),

    # ── Wearables ──
    ("connect my watch", ["Galaxy Wearable"]),
    ("check my samsung watch settings", ["Galaxy Wearable"]),
    ("change my headphone settings", ["Sony Headphones Connect"]),
    ("adjust noise canceling", ["Sony Headphones Connect"]),

    # ── Travel Documents ──
    ("show my boarding pass", ["Google Wallet", "American Airlines", "Delta", "Southwest Airlines", "United Airlines"]),
    ("get my esim for travel", ["Saily"]),
    ("i need mobile data abroad", ["Saily"]),
    ("border crossing app", ["CBP One"]),
    ("customs and immigration", ["CBP One"]),

    # ── Insurance ──
    ("check my travel insurance", ["GeoBlue"]),
    ("find a doctor abroad", ["GeoBlue"]),
    ("check my driving score", ["USAA SafePilot"]),

    # ── Driving & Auto ──
    ("start android auto", ["Android Auto"]),
    ("connect to my car", ["Android Auto"]),
]

# ── Boredom / doomscroll interceptions ──
# The model should refuse these and return a snarky anti-doomscroll message.

BOREDOM_QUERIES = [
    ("i want to scroll", "Stop wasting time. Focus on your life."),
    ("im bored", "Go read a book or do something productive instead of looking at your phone."),
    ("show me reels", "Reels are a waste of time. Go touch some grass."),
    ("i want to waste time", "No. Put the phone down."),
    ("distract me", "Find a real hobby instead of seeking screen distractions."),
    ("show me memes", "No memes. Go do some work."),
    ("time to scroll tiktok", "Doomscrolling is bad for your brain. Refusing to launch."),
    ("show me videos to watch", "How about reading a book instead of watching random videos?"),
    ("entertain me", "Your phone is not your entertainer. Go for a walk."),
    ("something fun on my phone", "Real fun happens outside your screen. Go explore."),
    ("lets doomscroll", "Absolutely not. Your brain deserves better."),
    ("open social media", "Social media is a time sink. Go connect with people in real life."),
    ("im so bored what do i do", "Put the phone down and go outside. Boredom is good for creativity."),
    ("kill some time", "Time is too valuable to kill. Find something meaningful to do."),
    ("i have nothing to do", "There is always something to do. Read, exercise, learn something new."),
    ("just wanna browse", "Mindless browsing leads nowhere. Set a goal instead."),
]

# ── None / fallback queries ──
# Queries that should NOT match any app or tool.

NONE_QUERIES = [
    "weather today",
    "how old is the universe",
    "calculate 25 times 4",
    "what is the capital of France",
    "tell me a joke",
    "what time is it in Tokyo",
    "how many ounces in a pound",
    "who won the Super Bowl last year",
    "define serendipity",
    "how far is the moon",
    "whats the speed of light",
    "convert 100 dollars to euros",
    "when was the Eiffel Tower built",
    "how do you say hello in Japanese",
    "what year did World War 2 end",
    "how tall is Mount Everest",
    "who painted the Mona Lisa",
    "whats the population of Canada",
    "what is photosynthesis",
    "how many planets are in the solar system",
    "recipe for banana bread",
    "how to tie a tie",
    "why is the sky blue",
    "who invented the telephone",
    "best movies of 2024",
]

# ── Direct-launch verb templates ──
LAUNCH_VERBS = [
    "open {}",
    "launch {}",
    "start {}",
    "go to {}",
    "open my {} app",
    "can you open {}",
    "pull up {}",
    "open up {}",
    "fire up {}",
    "show me {}",
    "bring up {}",
    "switch to {}",
    "run {}",
    "load {}",
    "i want {}",
    "take me to {}",
]

# ── Prompt formatter ──
def generate_prompt(installed_apps, query, format_type="gemma"):
    """Format a training prompt using the selected model's instruction-tuning chat template."""
    apps_str = "\n".join(
        [f"- {app['label']} ({app['packageName']}): {app['desc']}" for app in installed_apps]
    )
    if format_type == "chatml":
        return (
            f"<|im_start|>user\nApps:\n{apps_str}\n\nQuery: {query}\n"
            f"<|im_end|>\n<|im_start|>assistant\n"
        )
    else:
        return (
            f"<start_of_turn>user\nApps:\n{apps_str}\n\nQuery: {query}\n"
            f"<end_of_turn>\n<start_of_turn>model\n"
        )


def _pick_app_count():
    """Pick a realistic number of installed apps for a training example.

    Distribution mirrors real-world phone usage:
      - 10% of samples: small (10-20 apps)  — light users / new phones
      - 30% of samples: medium (20-40 apps)  — typical users
      - 40% of samples: large (40-70 apps)   — power users (most common)
      - 20% of samples: very large (70-100+)  — heavy users / full phones
    """
    pool_size = len(APPS_POOL)
    bucket = random.random()
    if bucket < 0.10:
        return random.randint(10, 20)
    elif bucket < 0.40:
        return random.randint(20, 40)
    elif bucket < 0.80:
        return random.randint(40, min(70, pool_size))
    else:
        return random.randint(70, pool_size)


def generate_dataset(num_samples=500, format_type="gemma"):
    """Generate a diverse synthetic training dataset."""
    dataset = []

    # Weight the categories — semantic-heavy, boredom+none ≈ 20%
    category_weights = {
        "direct_launch": 0.30,   # user names the app explicitly
        "semantic_launch": 0.50, # user describes intent naturally
        "boredom": 0.08,         # doomscroll interceptions
        "none": 0.12,            # queries with no matching app action
    }

    for _ in range(num_samples):
        # Pick a realistic number of installed apps for this example
        num_apps = _pick_app_count()
        installed = random.sample(APPS_POOL, num_apps)

        # Weighted category selection
        cat = random.choices(
            list(category_weights.keys()),
            weights=list(category_weights.values()),
            k=1,
        )[0]

        if cat == "direct_launch":
            # ── Direct launch: user names an installed app explicitly ──
            target_app = random.choice(installed)
            template = random.choice(LAUNCH_VERBS)
            # Randomly use the label as-is, lowercased, or with slight variation
            label_variant = random.choice([
                target_app["label"],
                target_app["label"].lower(),
                target_app["label"],
            ])
            query = template.format(label_variant)
            response = f'launch_apps(package_names=["{target_app["packageName"]}"])'

        elif cat == "semantic_launch":
            # ── Semantic launch: user describes intent, model matches to apps ──
            intent = random.choice(SEMANTIC_INTENTS)
            query, target_labels = intent

            # Find which target apps are actually in the installed set
            matching = [
                app["packageName"]
                for app in installed
                if app["label"] in target_labels
            ]

            if matching:
                response = f"launch_apps(package_names={json.dumps(matching)})"
            else:
                # None of the relevant apps are installed → none()
                response = "none()"

        elif cat == "boredom":
            # ── Boredom / doomscroll interception ──
            query, reason = random.choice(BOREDOM_QUERIES)
            response = f'trigger_boredom(reason="{reason}")'

        else:
            # ── None: queries that don't correspond to any app action ──
            query = random.choice(NONE_QUERIES)
            response = "none()"

        prompt = generate_prompt(installed, query, format_type=format_type)
        close_token = "<|im_end|>" if format_type == "chatml" else "<end_of_turn>"
        dataset.append({
            "prompt": prompt,
            "response": response,
            "full_text": f"{prompt}{response}{close_token}",
        })

    return dataset


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dataset generator")
    parser.add_argument("--small", action="store_true", help="Generate a small dataset with fewer apps per sample")
    args = parser.parse_args()

    # Determine size
    num_samples = 150 if args.small else 500

    if args.small:
        print(f"Generating optimized small datasets ({num_samples} samples, 5-15 apps per sample) for fast training...")
        _pick_app_count = lambda: random.randint(5, 15)
    else:
        print(f"Generating full datasets ({num_samples} samples, up to 100+ apps per sample)...")

    # 1. Generate Gemma format
    random.seed(42)  # Reset seed for identical sample pool
    gemma_data = generate_dataset(num_samples, format_type="gemma")
    with open("dataset_gemma.json", "w") as f:
        json.dump(gemma_data, f, indent=2)
    # Also save as default dataset.json
    with open("dataset.json", "w") as f:
        json.dump(gemma_data, f, indent=2)

    # 2. Generate ChatML format
    random.seed(42)  # Reset seed for identical sample pool
    chatml_data = generate_dataset(num_samples, format_type="chatml")
    with open("dataset_chatml.json", "w") as f:
        json.dump(chatml_data, f, indent=2)

    # Print stats (using Gemma data, which is identical in distribution)
    categories = {"launch_apps": 0, "trigger_boredom": 0, "none": 0}
    app_counts = []
    for item in gemma_data:
        if item["response"].startswith("launch_apps"):
            categories["launch_apps"] += 1
        elif item["response"].startswith("trigger_boredom"):
            categories["trigger_boredom"] += 1
        else:
            categories["none"] += 1
        # Count apps in this sample
        app_counts.append(item["prompt"].count("\n- "))

    total = len(gemma_data)
    print(f"Generated {total} training samples:")
    print(f"  → dataset_gemma.json & dataset.json (Gemma format)")
    print(f"  → dataset_chatml.json (ChatML format)")
    print(f"\nCategory breakdown:")
    print(f"  launch_apps:     {categories['launch_apps']:>4}  ({categories['launch_apps']/total*100:.1f}%)")
    print(f"  trigger_boredom: {categories['trigger_boredom']:>4}  ({categories['trigger_boredom']/total*100:.1f}%)")
    print(f"  none:            {categories['none']:>4}  ({categories['none']/total*100:.1f}%)")
    print(f"\nApps per sample:")
    print(f"  min={min(app_counts)}, max={max(app_counts)}, avg={sum(app_counts)/len(app_counts):.1f}")

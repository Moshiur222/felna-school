import random, re, hashlib, requests
from django.core.cache import cache

SMS_API_URL = "http://sms.iglweb.com/api/v1/send"
SMS_API_KEY = "44517757228316931775722831 "
SMS_SENDER_ID = "01844532630"

def normalize_phone(mobile):
    if not mobile: return None
    cleaned = re.sub(r'\D', '', str(mobile))
    if len(cleaned) == 11 and cleaned.startswith('01'): return '88' + cleaned
    if len(cleaned) == 13 and cleaned.startswith('8801'): return cleaned
    return None

def hash_otp(otp):
    """ওটিপি হ্যাশ করার ফাংশন"""
    return hashlib.sha256(otp.encode()).hexdigest()

# def send_otp(mobile):
#     normalized = normalize_phone(mobile)
#     if not normalized: return False, "সঠিক মোবাইল নম্বর দিন।"

#     otp_count_key = f"otp_count:{normalized}"
#     otp_count = cache.get(otp_count_key, 0)

#     if otp_count >= 2:
#         return False, "আপনি ২৪ ঘণ্টায় সর্বোচ্চ ২ বার ওটিপি নিতে পারবেন।"

#     # ৬ ডিজিটের র (Raw) ওটিপি জেনারেট করুন
#     otp_raw = str(random.randint(100000, 999999))
#     # প্রদর্শনের জন্য xxx-xxx ফরম্যাট তৈরি করুন
#     otp_display = f"{otp_raw[:3]}-{otp_raw[3:]}"

#     # ক্যাশে হাইফেন ছাড়া Raw ওটিপি হ্যাশ করে সেভ করুন
#     cache.set(f"otp:{normalized}", hash_otp(otp_raw), timeout=300) # ৫ মিনিট মেয়াদ
#     cache.set(otp_count_key, otp_count + 1, timeout=86400) # ২৪ ঘণ্টা মেয়াদ

#     msg = f"Welcome to Felna High School, Your OTP Is: {otp_display}, Expire for 5 Min, Don't Share With Any One.\nfelnahs.edu.bd"
    
#     try:
#         response = requests.post(SMS_API_URL, data={"api_key": SMS_API_KEY, "contacts": normalized, "senderid": SMS_SENDER_ID, "msg": msg}, timeout=10)
#         return True, "OTP Sent"
#     except:
#         return False, "এসএমএস পাঠানো সম্ভব হয়নি।"

def send_otp(mobile):
    normalized = normalize_phone(mobile)
    if not normalized:
        return False, "সঠিক মোবাইল নম্বর দিন।"

    otp_count_key = f"otp_count:{normalized}"
    otp_count = cache.get(otp_count_key, 0)

    if otp_count >= 2:
        return False, "আপনি ২৪ ঘণ্টায় সর্বোচ্চ ২ বার ওটিপি নিতে পারবেন।"

    # Generate OTP
    otp_raw = str(random.randint(100000, 999999))
    otp_display = f"{otp_raw[:3]}-{otp_raw[3:]}"

    # Save OTP hash
    cache.set(f"otp:{normalized}", hash_otp(otp_raw), timeout=300)
    cache.set(otp_count_key, otp_count + 1, timeout=86400)

    # Terminal এ OTP দেখাবে
    print("\n========== OTP TEST MODE ==========")
    print("Mobile:", normalized)
    print("OTP:", otp_raw)
    print("Display OTP:", otp_display)
    print("Expire: 5 Minutes")
    print("====================================\n")

    return True, "OTP Sent (Test Mode - Terminal)"

def verify_otp(mobile, user_otp):
    normalized = normalize_phone(mobile)
    if not normalized: return False, "মোবাইল নম্বর সঠিক নয়।"

    saved_hash = cache.get(f"otp:{normalized}")
    if not saved_hash: return False, "ওটিপির মেয়াদ শেষ অথবা পাওয়া যায়নি।"

    # ইউজারের ইনপুট থেকে হাইফেন বা অন্য কোনো স্পেশাল ক্যারেক্টার সরিয়ে ফেলুন
    clean_user_otp = re.sub(r'\D', '', user_otp)

    # হ্যাশ মিলিয়ে দেখুন
    if hash_otp(clean_user_otp) == saved_hash:
        cache.delete(f"otp:{normalized}") # সফল হলে ডিলিট করে দিন
        return True, "Verified"
    
    return False, "ভুল ওটিপি কোড।"
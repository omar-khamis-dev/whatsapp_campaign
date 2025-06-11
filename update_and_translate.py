import os
import subprocess
import polib
from googletrans import Translator

# إعدادات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANGUAGES = ['ar', 'de', 'nl']
DEFAULT_LANG = 'en'

print("🔄 بدء التحديث والترجمة التلقائية...")

# 1. تحديث ملفات .po
print("📦 تشغيل makemessages...")
subprocess.run(["django-admin", "makemessages", "-a"], cwd=BASE_DIR)

# 2. الترجمة التلقائية
print("🧠 بدء الترجمة التلقائية...")
translator = Translator()

for lang in LANGUAGES:
    po_path = os.path.join(BASE_DIR, 'locale', lang, 'LC_MESSAGES', 'django.po')
    if not os.path.exists(po_path):
        os.makedirs(os.path.dirname(po_path), exist_ok=True)
        open(po_path, 'w', encoding='utf-8').close()
        print(f"🆕 تم إنشاء ملف جديد: {po_path}")

    po = polib.pofile(po_path)
    changed = False

    for entry in po:
        # تحقق من السلاسل الفارغة أو المتغيرات البرمجية
        if entry.translated() or not entry.msgid.strip() or any(x in entry.msgid for x in ['{', '}', '%']):
            continue

        try:
            translated = translator.translate(entry.msgid, src=DEFAULT_LANG, dest=lang)
            entry.msgstr = translated.text.strip()
            entry.flags = []  # إزالة "fuzzy"
            entry.previous_msgid = None  # إزالة "#| msgid"
            changed = True
            print(f"✅ [{lang}] '{entry.msgid}' → '{entry.msgstr}'")
        except Exception as e:
            print(f"❌ خطأ في الترجمة [{lang}]: {entry.msgid} → {e}")

    if changed:
        po.save()
        print(f"💾 تم حفظ الترجمة: {po_path}")

# 3. تجميع ملفات .mo
print("🛠️ تشغيل compilemessages...")
subprocess.run(["django-admin", "compilemessages"], cwd=BASE_DIR)

print("🎉 اكتملت العملية بنجاح.")

import os
import subprocess
import polib
from googletrans import Translator

# إعدادات عامة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANGUAGES = ['ar', 'de', 'nl']  # أضف لغاتك هنا
DEFAULT_LANG = 'en'

print("🔄 بدء التحديث والترجمة التلقائية...")

# 1. تحديث ملفات .po
print("📦 تشغيل makemessages...")
subprocess.run(["django-admin", "makemessages", "-a"], cwd=BASE_DIR)

# 2. ترجمة السطور غير المترجمة تلقائيًا
print("🧠 بدء الترجمة التلقائية...")
translator = Translator()

for lang in LANGUAGES:
    po_path = os.path.join(BASE_DIR, 'locale', lang, 'LC_MESSAGES', 'django.po')
    if not os.path.exists(po_path):
        print(f"⚠️ ملف الترجمة غير موجود: {po_path}")
        continue

    po = polib.pofile(po_path)
    changed = False

    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            try:
                translated = translator.translate(entry.msgid, src=DEFAULT_LANG, dest=lang)
                entry.msgstr = translated.text
                entry.flags.discard("fuzzy")
                changed = True
                print(f"✅ [{lang}] '{entry.msgid}' → '{entry.msgstr}'")
            except Exception as e:
                print(f"❌ خطأ في الترجمة [{lang}]: {entry.msgid} → {e}")

    if changed:
        po.save()
        print(f"💾 تم حفظ الترجمة التلقائية: {po_path}")

# 3. تجميع ملفات .mo
print("🛠️  تجميع الترجمة (compilemessages)...")
subprocess.run(["django-admin", "compilemessages"], cwd=BASE_DIR)

print("🎉 اكتملت جميع المهام بنجاح!")

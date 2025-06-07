import os
import subprocess
import polib
from googletrans import Translator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')
LANGUAGES = ['ar', 'de', 'nl']
DEFAULT_LANG = 'en'

print("🔄 بدء التحديث والترجمة التلقائية...")

# 1. استخراج العبارات الجديدة
print("📦 تشغيل makemessages...")
subprocess.run(["django-admin", "makemessages", "-a"], cwd=BASE_DIR)

# 2. الترجمة التلقائية
print("🧠 بدء الترجمة التلقائية...")
translator = Translator()

for lang_code in LANGUAGES:
    po_path = os.path.join(LOCALE_DIR, lang_code, 'LC_MESSAGES', 'django.po')
    if not os.path.exists(po_path):
        print(f"⚠️ ملف غير موجود: {po_path}")
        continue

    print(f'🔄 جاري ترجمة: {lang_code}')
    po = polib.pofile(po_path)
    updated = False

    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            try:
                translation = translator.translate(entry.msgid, src=DEFAULT_LANG, dest=lang_code)
                entry.msgstr = translation.text
                updated = True
                print(f"✅ [{lang_code}] '{entry.msgid}' → '{entry.msgstr}'")
            except Exception as e:
                print(f'❌ فشل "{entry.msgid}": {e}')

    if updated:
        po.save()
        print(f'💾 تم حفظ: {po_path}')

# 3. تجميع ملفات mo
print("🛠️ تجميع ملفات الترجمة...")
subprocess.run(["django-admin", "compilemessages"], cwd=BASE_DIR)

print("🎉 التحديث والترجمة التلقائية اكتملت.")

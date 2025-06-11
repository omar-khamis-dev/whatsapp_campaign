import os
import subprocess
import glob

# اسم الحزمة المطلوبة
package_name = "vobject"
packages_dir = r"E:\pip_packages"

# تأكد من وجود المجلد
if not os.path.exists(packages_dir):
    os.makedirs(packages_dir)

# ابحث عن ملف .whl الخاص بالحزمة
whl_files = glob.glob(os.path.join(packages_dir, f"{package_name}-*.whl"))

if whl_files:
    # إذا وُجدت ملفات الحزمة، ثبتها من المجلد المحلي
    print(f"🔍 تم العثور على {package_name} في المجلد، يتم التثبيت محليًا...")
    subprocess.run(["pip", "install", "--no-index", "--find-links", packages_dir, package_name])
else:
    # لم يتم العثور على الحزمة، تنزيلها أولًا
    print(f"⚠️ لم يتم العثور على {package_name} في {packages_dir}، يتم تنزيلها...")
    subprocess.run(["pip", "download", "--dest", packages_dir, package_name])
    
    # ثم تثبيتها
    print(f"⬇️ تم التنزيل، الآن يتم التثبيت...")
    subprocess.run(["pip", "install", "--no-index", "--find-links", packages_dir, package_name])

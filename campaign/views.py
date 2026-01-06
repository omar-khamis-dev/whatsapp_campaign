from django.contrib import messages
import pandas as pd
import vobject
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .forms import ContactImportForm, ContactSearchForm, CampaignForm
from .models import Contact, Group, Campaign
from django.db.models import Count, Q, Min, Max
from django.shortcuts import get_object_or_404

# from django.db.models import Count
# from datetime import datetime, timedelta


def home(request):
    page_title = _("Home")
    greeting = _("Welcome to the WhatsApp Campaign System")
    return render(
        request, "campaign/home.html", {"greeting": greeting, "page_title": page_title}
    )


def dashboard(request):
    contact_count = Contact.objects.count()
    group_count = Group.objects.count()
    # message_count = Message.objects.count()
    # campaign_count = Campaign.objects.count()
    user_count = User.objects.count()
    # sent_success = Message.objects.filter(status='sent').count()
    # sent_failed = Message.objects.filter(status='failed').count()

    # بيانات الرسم البياني (عدد الرسائل لكل شهر في آخر 6 أشهر)
    # monthly_stats = []
    # today = datetime.today()
    # for i in range(5, -1, -1):
    #     month = (today.replace(day=1) - timedelta(days=i * 30)).strftime('%Y-%m')
    # count = Message.objects.filter(
    #     timestamp__year=month.split('-')[0],
    #     timestamp__month=month.split('-')[1]
    # ).count()
    # monthly_stats.append({'month': month, 'count': count})

    context = {
        "page_title": _("Dashboard"),
        "contact_count": contact_count,
        "group_count": group_count,
        # "message_count": message_count,
        # "campaign_count": campaign_count,
        "user_count": user_count,
        # "sent_success": sent_success,
        # "sent_failed": sent_failed,
        # "monthly_stats": monthly_stats,
    }
    return render(request, "campaign/dashboard.html", context)


def import_contacts(request):
    page_title = _("Import Contacts")
    form = ContactImportForm()
    preview_data = None
    columns = []
    error = None
    ready_to_save = False

    # حالة الحفظ النهائي بعد المعاينة
    if request.method == "POST" and "save_contacts" in request.POST:
        import_data = request.session.get("import_data")
        group_name = request.session.get("import_group")

        if import_data:
            # إنشاء المجموعة إن لم تكن موجودة
            group = None
            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)

            for entry in import_data:
                try:
                    contact = Contact.objects.create(
                        full_name=entry.get("full_name", ""),
                        phone_number=entry.get("phone_number", ""),
                        email=entry.get("email", ""),
                        gender=entry.get("gender", ""),
                        birth_date=entry.get("birth_date") or None,
                        birth_place=entry.get("birth_place", ""),
                        country_code=entry.get("country_code", ""),
                        residence=entry.get("residence", ""),
                        qualification=entry.get("qualification", ""),
                        specialty=entry.get("specialty", ""),
                        interests=entry.get("interests", ""),
                        status="pending",
                        source="imported",
                    )
                    if group:
                        contact.groups.add(group)
                except Exception as e:
                    continue  # يمكن تحسين السجلات الفاشلة لاحقًا
            # بعد حفظ جميع جهات الاتصال
            messages.success(request, _("Contacts have been saved successfully."))
            # حذف البيانات المؤقتة من الجلسة
            del request.session["import_data"]
            del request.session["import_group"]
            return redirect(
                "import_contacts"
            )  # إعادة التوجيه لتجنب إعادة الحفظ عند التحديث

    # رفع الملف ومعاينته
    if request.method == "POST" and "file" in request.FILES:
        form = ContactImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                    # معالجتك المعتادة
                    df = df.fillna("")
                    df = df.applymap(
                        lambda x: (
                            x.strftime("%Y-%m-%d") if isinstance(x, pd.Timestamp) else x
                        )
                    )
                    import_data = df.to_dict(orient="records")
                    columns = df.columns.tolist()

                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                    df = df.fillna("")
                    df = df.applymap(
                        lambda x: (
                            x.strftime("%Y-%m-%d") if isinstance(x, pd.Timestamp) else x
                        )
                    )
                    import_data = df.to_dict(orient="records")
                    columns = df.columns.tolist()

                elif uploaded_file.name.endswith(".vcf"):
                    # قراءة ملف vcf وتحويله إلى قائمة dict
                    vcf_text = uploaded_file.read().decode("utf-8")
                    contacts = []
                    for vcard in vobject.readComponents(vcf_text):
                        full_name = getattr(vcard, "fn", None)
                        phone = None
                        if hasattr(vcard, "tel"):
                            phone = vcard.tel.value
                        contact = {
                            "full_name": full_name.value if full_name else "",
                            "phone_number": phone if phone else "",
                        }
                        contacts.append(contact)
                    import_data = contacts
                    columns = ["full_name", "phone_number"]

                else:
                    error = "نوع الملف غير مدعوم. يرجى رفع ملف CSV أو Excel أو VCF."
                    return render(
                        request,
                        "campaign/import_contacts.html",
                        {
                            "form": form,
                            "error": error,
                        },
                    )

                # تحقق وجود الأعمدة المطلوبة لو لم تكن ملف vcf
                if uploaded_file.name.endswith(".vcf") is False:
                    expected_columns = ["full_name", "phone_number"]
                    if not all(col in columns for col in expected_columns):
                        error = "الأعمدة المطلوبة مفقودة (full_name, phone_number)"
                        return render(
                            request,
                            "campaign/import_contacts.html",
                            {
                                "form": form,
                                "error": error,
                            },
                        )

                # حفظ البيانات مؤقتًا للمعاينة أو الحفظ لاحقاً
                request.session["import_data"] = import_data
                request.session["import_group"] = form.cleaned_data["group_name"]

                preview_data = import_data[:50]
                ready_to_save = True

            except Exception as e:
                error = f"خطأ في قراءة الملف: {e}"
                return render(
                    request,
                    "campaign/import_contacts.html",
                    {
                        "form": form,
                        "error": error,
                    },
                )

    else:
        form = ContactImportForm()

    return render(
        request,
        "campaign/import_contacts.html",
        {
            "form": form,
            "preview_data": preview_data if "preview_data" in locals() else None,
            "columns": columns if "columns" in locals() else None,
            "error": error if "error" in locals() else None,
            "ready_to_save": ready_to_save if "ready_to_save" in locals() else False,
            "page_title": page_title,
        },
    )


def contact_list(request):
    page_title = _("Contact List")
    form = ContactSearchForm(request.GET or None)
    contacts = Contact.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        group = form.cleaned_data.get("group")
        status = form.cleaned_data.get("status")
        gender = form.cleaned_data.get("gender")

        if query:
            contacts = contacts.filter(
                Q(full_name__icontains=query)
                | Q(phone_number__icontains=query)
                | Q(email__icontains=query)
            )

        if group:
            contacts = contacts.filter(groups=group)

        if status:
            contacts = contacts.filter(status=status)

        if gender:
            contacts = contacts.filter(gender__iexact=gender)

    contacts = contacts.order_by("-created_at")

    return render(
        request,
        "campaign/contact_list.html",
        {
            "contacts": contacts,
            "form": form,
            "page_title": page_title,
        },
    )


def create_campaign(request):
    page_title = _("Create New Campaign")
    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Campaign created successfully."))
            return redirect("campaign_list")  # غيّرها لاحقًا لصفحة عرض الحملات
    else:
        form = CampaignForm()

    return render(
        request,
        "campaign/create_campaign.html",
        {
            "form": form,
            "page_title": page_title,
        },
    )


def campaign_list(request):
    page_title = _("Campaigns")
    campaigns = Campaign.objects.select_related("group").all().order_by("-created_at")
    return render(
        request,
        "campaign/campaign_list.html",
        {
            "campaigns": campaigns,
            "page_title": page_title,
        },
    )


def campaign_reports(request):
    page_title = _("Campaign Reports")
    campaigns = Campaign.objects.all().annotate(
        sent_count=Count("messages", filter=Q(messages__status="sent")),
        failed_count=Count("messages", filter=Q(messages__status="failed")),
        start_time=Min("messages__sent_at"),
        end_time=Max("messages__sent_at"),
    )

    for campaign in campaigns:
        if campaign.start_time and campaign.end_time:
            duration = campaign.end_time - campaign.start_time
            campaign.duration_seconds = duration.total_seconds()
        else:
            campaign.duration_seconds = 0

        total = campaign.sent_count + campaign.failed_count
        campaign.success_rate = (campaign.sent_count / total * 100) if total > 0 else 0

    return render(
        request,
        "campaign/campaign_reports.html",
        {
            "campaigns": campaigns,
            "page_title": page_title,
        },
    )


def campaign_detail_report(request, campaign_id):
    page_title = _("Campaign Reports")
    campaign = get_object_or_404(Campaign, id=campaign_id)
    messages = campaign.messages.all()

    status_counts = messages.values("status").annotate(count=Count("id"))
    reaction_counts = messages.values("reaction_status").annotate(count=Count("id"))

    # تحويل القيم إلى dict مرتب
    status_summary = {entry["status"]: entry["count"] for entry in status_counts}
    reaction_summary = {
        entry["reaction_status"]: entry["count"] for entry in reaction_counts
    }

    return render(
        request,
        "campaign/campaign_detail_report.html",
        {
            "campaign": campaign,
            "messages": messages,
            "status_summary": status_summary,
            "reaction_summary": reaction_summary,
            "page_title": page_title,
        },
    )


def top_engaged_campaign(request):
    page_title = _("Top Engaged Campaign")
    from django.db.models import Count, Q

    campaigns = Campaign.objects.annotate(
        engagement_score=Count(
            "messages",
            filter=Q(messages__reaction_status__in=["read", "replied", "reacted"]),
        )
    ).order_by("-engagement_score")

    top_campaign = campaigns.first()

    return render(
        request,
        "campaign/top_campaign.html",
        {
            "top_campaign": top_campaign,
            "page_title": page_title,
        },
    )

# خطوات إصدار DOI للحزمة (Zenodo) — 5 دقائق

> الهدف: معرّف دائم (DOI) للحزمة `germline-corpus-v0.1.0` — يصبح العمل «قابلاً للاقتباس» أكاديمياً.

## الطريق الأسرع (ربط GitHub بـZenodo — مرة واحدة فقط)

1. افتح **zenodo.org** ← سجّل بحساب GitHub («Sign up with GitHub»).
2. من القائمة: **Settings → GitHub** ← ابحث عن `germline` ← **شغّل المفتاح** (Flip switch).
   - إن طلب Zenodo صلاحيات، وافق — سيُضاف خطاف (webhook) ينسخ الإصدارات تلقائياً.
3. ارجع إلى صفحة الإصدار: **github.com/FerasFuad34/germline/releases/tag/v0.1.0**
   ← عدّل الإصدار (Edit) ← ثم **أنقذ/أعد النشر** (Publish) — سيصل إشعار لـZenodo.
4. في **zenodo.org → Uploads** ستجد نسخة منشورة برقم DOI مثل `10.5281/zenodo.XXXXXXX`.
5. انسخ رقم DOI وأرسله لي — سأضيفه إلى: `CITATION.cff` و`README` وصفحة الإصدار و`DATASHEET.md` وُيبقى كل شيء متسقاً.

## الطريق اليدوي (بديل)

1. حزمة جاهزة: من الإصدار نزّل `germline-corpus-v0.1.0.zip`.
2. في Zenodo: **New upload** ← ارفع الملف ← الصق الحقول من الملف الموجود في المستودع:
   `dataset/metadata/zenodo-deposit.json` (العنوان، الوصف، الكلمات المفتاحية، الترخيص `cc-by-4.0`).
3. **مهم**: في حقل المؤلفين، استبدل `TODO: Family name, Given name` باسمك الكامل (كما تريده أن يظهر في الاقتباسات).
4. نوع الحزمة: `Dataset` ← الترخيص: `CC-BY-4.0` ← **Publish**.

## بعد النشر

- ابنِ «اقتباس» جاهز يُعرض في Zenodo (Copy citation) وأرسله لي لأضيفه في `CITATION.cff`.
- أي إصدار جديد لاحق (v0.2، v1.0) سيحصل تلقائياً على DOI خاص به — الأقدم يبقى مؤرشفاً للأبد.

# 90-second demo video — script & storyboard

Target: **~90 seconds**, English narration, screen-quality slides (1280×720).
Purpose: linked from the NLnet application, the README, and the first public post.

## Narration script (≈1,150 characters ≈ 90 s)

> Software is being rewritten by AI faster than its security memory can survive.
> A C library accumulates twenty years of fixes. An AI-assisted rewrite turns it
> into Rust. The tests pass. But do the old attacks still fail?
>
> Nobody measures that. So we turned history into a test format.
>
> An antibody is one historical vulnerability, reduced to a discriminating
> experiment: a vulnerable build that must fail, and a fixed build that must stay
> clean. If it cannot tell the two apart, it is not an antibody.
>
> Today the corpus holds a hundred antibodies across seventeen critical projects —
> libxml2, ffmpeg, ImageMagick, curl, OpenSSL — each one reproducible from a
> public OSS-Fuzz report and an upstream fix commit. Three are already verified
> end-to-end on real containers, with an append-only public log. The rest say
> "draft" — because absence of verification must never be rendered as success.
>
> ABX, our open format — RFC zero — makes these antibodies portable: strict,
> canonical, signable. Evidence travels with the check.
>
> The goal is an Immune Gate: replay every ancestor's antibodies against every
> new generation, and issue a signed Immune Passport.
>
> Everything is public today: repository, corpus, format, verification log.
> GitHub dot com slash FerasFuad34 slash germline.
>
> SBOM tells you what's in your code. GERMLINE tells you what your code survived.

## Storyboard (scene → visual → duration)

| # | Scene | Visual | s |
|---|---|---|---|
| 1 | Title | GERMLINE — immune inheritance for software | 7 |
| 2 | Problem | "AI rewrites code fast. Its security memory does not survive." | 12 |
| 3 | Antibody | two cards: vulnerable must FAIL / fixed must stay CLEAN | 12 |
| 4 | Corpus | 100 · 17 · 3 verified · 100 ABX docs | 12 |
| 5 | ABX | RFC-0 code fragment (expect / detector / integrity) | 13 |
| 6 | Evidence | terminal log: ✅ verified … append-only | 11 |
| 7 | Gate | lineage g0→g1→g2 → IMMUNE GATE → passport | 12 |
| 8 | Close | repo URL + one-liner | 10 |

## Build

```bash
python3 tools/make-demo-video.py slides
python3 tools/make-demo-video.py assemble --audio dist/video/narration-en.mp3 --total 90
```

(Assembler uses a static ffmpeg via `pip install imageio-ffmpeg`; scenes are
scaled proportionally to the narration length.)

## نسخة عربية للشرح (للنشر المحلي — بدون فيديو)

> البرمجيات تُعاد كتابتها بالذكاء الاصطناعي أسرع مما تنجو ذاكرتها الأمنية.
> مكتبة بلغة C تجمع عشرين سنة من الإصلاحات الأمنية، ثم يُعيد الذكاء الاصطناعي
> كتابتها بلغة Rust. الاختبارات تنجح… لكن هل ما زالت الهجمات القديمة تفشل؟
> لا أحد يقيس ذلك. لذلك حوّلنا التاريخ إلى صيغة اختبار:
> «المصل» = ثغرة تاريخية تتحول إلى تجربة فاصلة: نسخة مصابة يجب أن تفشل، ونسخة
> مُصلَحة يجب أن تبقى نظيفة. اليوم لدينا 100 مصل من 17 مشروعاً حساساً، و3 منها
> موثّقة التشغيل فعلياً بسجل علني، والباقي يقول بصراحة: «مسودة».
> وصيغة ABX المفتوحة تجعل هذه الأمصال قابلة للانتقال بين المؤسسات.
> الهدف النهائي: «بوابة مناعية» تُشغّل أمصال كل الأسلاف على أي جيل جديد وتُصدر
> جواز سفر مناعي موقّعاً. كل شيء علني اليوم: المستودع والمصـل والصيغة وسجل التحقق.

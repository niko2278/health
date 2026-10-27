#!/usr/bin/env python3
"""Generate one savings page per drug, the /drugs index, and sitemap.xml.

Run from the repo root:  python3 tools/build_drug_pages.py
Edit DRUGS below to add or change a drug, then run again.
Change SITE when the custom domain is connected.
"""
import html, json, pathlib

SITE = "https://health-chi.vercel.app"
ROOT = pathlib.Path(__file__).resolve().parent.parent

# slug, name, also known as, drug class, used for, group, tip
# group: generic | brand | other
DRUGS = [
 ("atorvastatin","Atorvastatin","generic of Lipitor","statin","lowering LDL (\"bad\") cholesterol and reducing the risk of heart attack and stroke","generic",
  "Atorvastatin is one of the most prescribed drugs in the U.S. and is widely available as a generic, so discount card prices are often very low."),
 ("lisinopril","Lisinopril","generic of Zestril and Prinivil","ACE inhibitor","high blood pressure and heart failure","generic",
  "Lisinopril is an older generic. If you take it every day, ask for a 90-day supply: the discounted price per pill is often lower."),
 ("metformin","Metformin","generic of Glucophage","biguanide","type 2 diabetes","generic",
  "Metformin comes as immediate-release and extended-release (ER) tablets. The ER version can cost more, so compare both with your card if your doctor allows either."),
 ("amlodipine","Amlodipine","generic of Norvasc","calcium channel blocker","high blood pressure and chest pain (angina)","generic",
  "Amlodipine is a low-cost generic at most pharmacies. Prices still vary a lot from store to store, so compare before you fill."),
 ("levothyroxine","Levothyroxine","generic of Synthroid, Levoxyl and Unithroid","thyroid hormone","an underactive thyroid (hypothyroidism)","generic",
  "Some doctors prefer that you stay on the same levothyroxine manufacturer. Ask your doctor or pharmacist before switching to a cheaper version."),
 ("losartan","Losartan","generic of Cozaar","angiotensin receptor blocker (ARB)","high blood pressure and protecting the kidneys in people with diabetes","generic",
  "Losartan is a common generic. A 90-day supply with a discount card is often cheaper per dose than a 30-day fill."),
 ("gabapentin","Gabapentin","generic of Neurontin","anticonvulsant","seizures and nerve pain after shingles","generic",
  "Gabapentin comes in capsules, tablets and liquid. The price depends heavily on the strength and form, so check the exact one on your prescription."),
 ("sertraline","Sertraline","generic of Zoloft","SSRI antidepressant","depression, anxiety disorders, OCD and PTSD","generic",
  "Sertraline is a widely available generic. Discount cards often bring a month's supply well below the usual cash price."),
 ("omeprazole","Omeprazole","generic of Prilosec","proton pump inhibitor (PPI)","acid reflux (GERD) and stomach ulcers","generic",
  "Some omeprazole strengths are sold over the counter. Your prescription strength may differ, so ask the pharmacist which option is cheapest for you."),
 ("amoxicillin","Amoxicillin","generic of Amoxil","penicillin-type antibiotic","bacterial infections such as ear, throat and sinus infections","generic",
  "Amoxicillin is usually a short course. Without insurance, a discount card can make a real difference on a one-time fill."),
 ("escitalopram","Escitalopram","generic of Lexapro","SSRI antidepressant","depression and generalized anxiety disorder","generic",
  "Escitalopram is a common generic. Compare prices at two or three pharmacies near you: the gap can be large."),
 ("bupropion","Bupropion","generic of Wellbutrin and Zyban","antidepressant","depression, seasonal depression and help with quitting smoking","generic",
  "Bupropion comes as SR and XL tablets, and their prices differ. Check the exact version written on your prescription."),
 ("montelukast","Montelukast","generic of Singulair","leukotriene receptor antagonist","asthma and seasonal allergies","generic",
  "Montelukast is an inexpensive generic at most pharmacies when you pay with a discount card."),
 ("rosuvastatin","Rosuvastatin","generic of Crestor","statin","lowering cholesterol and reducing heart disease risk","generic",
  "Rosuvastatin became generic years ago. With a discount card, its price is often close to other low-cost statins."),
 ("prednisone","Prednisone","corticosteroid (several brand names)","corticosteroid","inflammation, allergic reactions, asthma flares and some autoimmune conditions","generic",
  "Prednisone is often prescribed for a short time. It is a low-cost generic, so a card can cover most of the cash price."),
 ("tamsulosin","Tamsulosin","generic of Flomax","alpha blocker","urinary symptoms of an enlarged prostate (BPH)","generic",
  "Tamsulosin is a common generic. A 90-day supply can lower the cost per capsule."),
 ("ozempic","Ozempic","semaglutide","GLP-1 receptor agonist","type 2 diabetes (weekly injection)","brand",
  "Ozempic is a brand-name drug. Discount cards may lower the cash price only a little, so also check the manufacturer's (Novo Nordisk) savings programs before you pay."),
 ("wegovy","Wegovy","semaglutide","GLP-1 receptor agonist","chronic weight management (weekly injection)","brand",
  "Insurance often doesn't cover weight-loss drugs. Check the manufacturer's (Novo Nordisk) self-pay and savings options, and compare them with your card price."),
 ("mounjaro","Mounjaro","tirzepatide","GIP/GLP-1 receptor agonist","type 2 diabetes (weekly injection)","brand",
  "Mounjaro is a brand-name drug. Compare your discount card price with the manufacturer's (Eli Lilly) savings card, which can be lower if you have commercial insurance."),
 ("zepbound","Zepbound","tirzepatide","GIP/GLP-1 receptor agonist","chronic weight management and obstructive sleep apnea in adults with obesity","brand",
  "The manufacturer (Eli Lilly) offers self-pay options through its own pharmacy service. Compare that price with your discount card before you pay."),
 ("eliquis","Eliquis","apixaban","anticoagulant (blood thinner)","reducing stroke risk with atrial fibrillation and treating or preventing blood clots","brand",
  "Eliquis is expensive without coverage. If you have Medicare Part D, check your plan's price first; otherwise compare your card with the manufacturer's savings program."),
 ("xarelto","Xarelto","rivaroxaban","anticoagulant (blood thinner)","reducing stroke risk with atrial fibrillation and treating or preventing blood clots","brand",
  "Ask the pharmacist whether a generic rivaroxaban is available for your strength. If not, compare your card price with the manufacturer's savings program."),
 ("jardiance","Jardiance","empagliflozin","SGLT2 inhibitor","type 2 diabetes, heart failure and chronic kidney disease","brand",
  "Jardiance is a brand-name drug. If you have Medicare Part D, check your plan's price first. With commercial insurance, the manufacturer's savings card may beat a discount card."),
 ("farxiga","Farxiga","dapagliflozin","SGLT2 inhibitor","type 2 diabetes, heart failure and chronic kidney disease","brand",
  "Ask the pharmacist whether a lower-cost dapagliflozin is available. Then compare it with your discount card and the manufacturer's savings program."),
 ("trulicity","Trulicity","dulaglutide","GLP-1 receptor agonist","type 2 diabetes (weekly injection)","brand",
  "Trulicity is a brand-name drug. Compare your card price with the manufacturer's (Eli Lilly) savings card before you fill."),
 ("rybelsus","Rybelsus","oral semaglutide","GLP-1 receptor agonist (tablet)","type 2 diabetes","brand",
  "Rybelsus is the tablet form of semaglutide. Compare your card price with the manufacturer's (Novo Nordisk) savings program."),
 ("adderall","Adderall","amphetamine and dextroamphetamine","stimulant (Schedule II controlled substance)","ADHD and narcolepsy","other",
  "Generic Adderall comes as immediate-release (IR) and extended-release (XR). Their prices differ, and availability can vary by pharmacy, so call ahead."),
 ("vyvanse","Vyvanse","lisdexamfetamine","stimulant (Schedule II controlled substance)","ADHD and moderate to severe binge eating disorder in adults","other",
  "Generic lisdexamfetamine is available in the U.S. Ask for the generic and compare its card price at a few pharmacies."),
 ("sildenafil","Sildenafil","generic of Viagra and Revatio","PDE5 inhibitor","erectile dysfunction and pulmonary arterial hypertension","other",
  "Generic sildenafil costs far less than the brand. Prices vary a lot by strength and quantity, so compare the exact prescription."),
 ("tadalafil","Tadalafil","generic of Cialis and Adcirca","PDE5 inhibitor","erectile dysfunction, enlarged prostate symptoms and pulmonary arterial hypertension","other",
  "Generic tadalafil is widely available. Ask the pharmacist to compare your card price with your insurance copay."),
]

GROUPS = {"generic":"Common generics","brand":"Brand-name drugs","other":"ADHD and men's health"}

STYLE = """:root{--bg:#f7faf9;--surface:#fff;--ink:#0f1f1c;--muted:#4b5d59;--line:#dbe5e2;--brand:#0f766e;--brand-ink:#fff;--brand-soft:#e6f4f1}
@media (prefers-color-scheme: dark){:root{--bg:#0c1513;--surface:#13201d;--ink:#e8f1ee;--muted:#9bb0aa;--line:#24352f;--brand:#2dd4bf;--brand-ink:#05211d;--brand-soft:#153029}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--brand)}.wrap{max-width:820px;margin:0 auto;padding:0 20px}
header.top{display:flex;align-items:center;justify-content:space-between;padding:18px 0;gap:12px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--ink);text-decoration:none}
.logo span{display:inline-grid;place-items:center;width:32px;height:32px;border-radius:9px;background:var(--brand);color:var(--brand-ink);font-weight:800}
nav a{color:var(--muted);text-decoration:none;margin-left:16px;font-size:15px}
.crumbs{font-size:14px;color:var(--muted);margin:8px 0 0}.crumbs a{color:var(--muted)}
h1{font-size:clamp(28px,4.6vw,42px);line-height:1.15;margin:10px 0 10px;letter-spacing:-.02em}
.lead{font-size:18px;color:var(--muted);margin:0 0 24px;max-width:38em}
.cta{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 12px}
.cta a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px;text-decoration:none;color:var(--ink)}
.cta a.main{border:2px solid var(--brand)}.cta b{display:block;font-size:19px}.cta small{color:var(--muted);font-size:14px}
.cta span{display:inline-block;margin-top:10px;background:var(--brand);color:var(--brand-ink);padding:9px 14px;border-radius:10px;font-weight:650;font-size:15px}
.free{color:var(--muted);font-size:14px;margin:0 0 8px}
section{padding:36px 0;border-top:1px solid var(--line);margin-top:28px}
h2{font-size:clamp(21px,3vw,27px);margin:0 0 12px}
.facts{display:grid;grid-template-columns:max-content 1fr;gap:8px 18px;margin:0}
.facts dt{color:var(--muted);font-size:14px}.facts dd{margin:0}
.tip{background:var(--brand-soft);border-radius:14px;padding:16px 18px;margin-top:20px}
ol.steps{padding-left:22px}ol.steps li{margin-bottom:8px}
details{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:10px}
summary{cursor:pointer;font-weight:620}details p{color:var(--muted);margin:8px 0 0}
.related{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}
.related a{display:inline-block;border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 12px;text-decoration:none;color:var(--ink);font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;padding:0;list-style:none}
.grid a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--ink)}
.grid small{display:block;color:var(--muted);font-size:13px}
footer{border-top:1px solid var(--line);padding:28px 0 44px;color:var(--muted);font-size:13.5px;margin-top:40px}
footer .links a{color:var(--muted);margin-right:16px}
@media (max-width:640px){.cta{grid-template-columns:1fr}nav{display:none}}"""

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f766e'/%3E%3Cpath d='M20 18h14a10 10 0 0 1 0 20h-6v8h-8zm8 7v6h6a3 3 0 0 0 0-6z' fill='white'/%3E%3C/svg%3E"

def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="{FAVICON}">
<style>{STYLE}</style>
{extra}</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="logo" href="/"><span>Rx</span>RxSavings Guide</a>
    <nav><a href="/drugs">Drug savings</a><a href="/#cards">Get a card</a><a href="/#faq">FAQ</a></nav>
  </header>
"""

FOOT = """  <footer>
    <div class="links"><a href="/drugs">All drugs</a><a href="/legal.html#terms">Terms</a><a href="/legal.html#privacy">Privacy</a><a href="/legal.html#disclosure">Affiliate disclosure</a></div>
    <p>RxSavings Guide is an independent information site operated by DELABARRE INC. It is not a pharmacy, not an insurance plan and does not give medical advice. Prices and savings vary by drug, dose, quantity and pharmacy and are not guaranteed. Some links are affiliate links: we may earn a commission at no cost to you. Brand names are trademarks of their respective owners, which do not endorse this site.</p>
  </footer>
</div>
<script src="/cards.js"></script>
</body>
</html>
"""

def cta():
    return """  <div class="cta">
    <a class="main" data-card="ndc" href="https://www.nationaldrugcard.com/" rel="sponsored noopener" target="_blank"><b>National Drug Card</b><small>Free, no form. Print it or save it to your phone.</small><br><span>Get free card →</span></a>
    <a data-card="goodrx" href="https://www.goodrx.com/" rel="sponsored noopener" target="_blank"><b>GoodRx</b><small>Compare prices at pharmacies near you.</small><br><span>Check prices →</span></a>
  </div>
  <p class="free">Both cards are free, with or without insurance. No sign-up on this site.</p>
"""

def drug_page(d):
    slug, name, aka, cls, use, group, tip = d
    path = f"/{slug}-coupon"
    title = f"{name} Coupon: Free Discount Card to Save at the Pharmacy | RxSavings Guide"
    desc = f"Save on {name} ({aka}) with a free prescription discount card. No insurance needed. See how to pay less for {name} at U.S. pharmacies."
    is_brand = group == "brand"
    faqs = [
        (f"Can I use a discount card for {name}?",
         f"Yes. You can show a free discount card at most U.S. pharmacies when you fill {name}. The pharmacist applies the discounted price if it is available for your drug and dose."),
        (f"How much does {name} cost without insurance?",
         f"It depends on the strength, the quantity and the pharmacy. Prices for the same prescription can differ a lot between stores, so check the price with a card before you pay."),
        (f"Can I use a {name} coupon with my insurance?",
         "Not on the same prescription. You can choose the discount card price instead of your insurance when it is lower. Payments made with a card may not count toward your deductible."),
    ]
    if is_brand:
        faqs.append((f"Is there a manufacturer savings program for {name}?",
         f"Brand-name drugs like {name} often have savings programs run by the manufacturer. They are usually best for people with commercial insurance. Compare that offer with your discount card price and use the lower one."))
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in faqs)
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    related = [x for x in DRUGS if x[5]==group and x[0]!=slug][:8]
    rel_html = "".join(f'<li><a href="/{x[0]}-coupon">{x[1]} coupon</a></li>' for x in related)
    return head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld)}</script>\n') + f"""  <p class="crumbs"><a href="/">Home</a> › <a href="/drugs">Drug savings</a> › {name}</p>
  <h1>{name} coupon: pay less at the pharmacy</h1>
  <p class="lead">Get a free prescription discount card and show it when you fill {name} ({html.escape(aka)}). No insurance needed, no sign-up.</p>
{cta()}
  <section>
    <h2>About {name}</h2>
    <dl class="facts">
      <dt>Also known as</dt><dd>{html.escape(aka)}</dd>
      <dt>Drug class</dt><dd>{html.escape(cls)}</dd>
      <dt>Commonly prescribed for</dt><dd>{html.escape(use)}</dd>
    </dl>
    <p class="tip"><strong>Savings tip:</strong> {html.escape(tip)}</p>
  </section>
  <section>
    <h2>How to save on {name}</h2>
    <ol class="steps">
      <li>Get one of the free cards above on your phone or print it.</li>
      <li>When you drop off or pick up your {name} prescription, give the card numbers to the pharmacist.</li>
      <li>Ask the pharmacist to compare the card price with your insurance copay, and pay the lower one.</li>
      <li>If the price is still high, check another pharmacy nearby. The same card can give different prices.</li>
    </ol>
  </section>
  <section>
    <h2>{name} questions</h2>
    {faq_html}
  </section>
  <section>
    <h2>Other {GROUPS[group].lower()}</h2>
    <ul class="related">{rel_html}</ul>
    <p><a href="/drugs">See all drugs →</a></p>
  </section>
  <p class="free">This page is for information only and is not medical advice. Talk to your doctor or pharmacist before starting, stopping or changing any medication.</p>
""" + FOOT

def index_page():
    parts = []
    for g, label in GROUPS.items():
        items = "".join(f'<li><a href="/{d[0]}-coupon"><b>{d[1]}</b><small>{html.escape(d[2])}</small></a></li>' for d in DRUGS if d[5]==g)
        parts.append(f'<section><h2>{label}</h2><ul class="grid">{items}</ul></section>')
    return head("Prescription Drug Coupons: Save on Common Medications | RxSavings Guide",
                "Free discount cards for common prescription drugs in the U.S.: atorvastatin, lisinopril, metformin, Ozempic, Eliquis and more.",
                "/drugs") + """  <p class="crumbs"><a href="/">Home</a> › Drug savings</p>
  <h1>Save on your prescription</h1>
  <p class="lead">Find your medication to see how a free discount card can lower the price you pay at U.S. pharmacies.</p>
""" + cta() + "".join(parts) + FOOT

def main():
    for d in DRUGS:
        (ROOT / f"{d[0]}-coupon.html").write_text(drug_page(d))
    (ROOT / "drugs.html").write_text(index_page())
    urls = ["/", "/drugs"] + [f"/{d[0]}-coupon" for d in DRUGS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"{len(DRUGS)} drug pages + drugs.html + sitemap.xml")

if __name__ == "__main__":
    main()

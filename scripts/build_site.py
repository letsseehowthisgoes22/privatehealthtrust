"""Build the editorial landing pages and source-linked directories. No dependencies."""
from pathlib import Path
import json, html, re
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/providers.json').read_text())
BASE='https://privatehealthtrust.com'
DATE=DATA['reviewed']
def e(s):return html.escape(str(s),quote=True)
def a(url,label,cls=''):
    return f'<a href="{e(url)}"'+(f' class="{cls}"' if cls else '')+'>'+e(label)+'</a>'
NAV=[('/provider-directory.html','Treatment directory'),('/private-case-managers.html','Case managers'),('/help-for-parents.html','For parents'),('/articles/','Journal'),('/about.html','About')]
def header(active=''):
    return '<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><div class="brand-row"><a class="brand" href="/">PRIVATE HEALTH <span>TRUST</span></a><span class="brand-note">THE PRIVATE CLIENT JOURNAL</span></div><nav aria-label="Main navigation"><ul>'+''.join(f'<li><a href="{u}"'+(' aria-current="page"' if active==u else '')+f'>{t}</a></li>' for u,t in NAV)+'</ul></nav></div></header>'
def footer():
    return '<footer class="site-footer"><div class="footer-inner"><div class="footer-brand">Private Health Trust</div><p>Clearer choices. Thoughtful care. A life beyond treatment.</p><div class="footer-links"><ul>'+''.join(f'<li>{a(u,t)}</li>' for u,t in NAV)+'</ul></div><p class="footer-disclaimer">Educational resources for families and advisors. Provider information describes published services; individual care decisions belong with qualified clinicians.</p><div class="footer-bottom">© 2026 Private Health Trust <span>'+a('/llms.txt','AI reading guide')+' · '+a('/editorial-methodology.html','Directory methodology')+'</span></div></div></footer>'
def page(name,title,desc,body,schemas=None,wide=True):
    path='/' if name=='index.html' else '/'+name
    graph=[{'@context':'https://schema.org','@type':'WebPage','@id':BASE+path,'url':BASE+path,'name':title,'description':desc,'isPartOf':{'@id':BASE+'/#website'},'dateModified':DATE}, {'@context':'https://schema.org','@type':'Organization','@id':BASE+'/#organization','name':'Private Health Trust','url':BASE+'/'}, {'@context':'https://schema.org','@type':'WebSite','@id':BASE+'/#website','name':'Private Health Trust','url':BASE+'/','publisher':{'@id':BASE+'/#organization'}}]
    if path!='/':graph.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':title,'item':BASE+path}]})
    graph+=schemas or []
    verification='<meta name="google-site-verification" content="1eZF6ixdq8i9aJ_vKMq5mZqEMnEP1q1856tPU3nTIuM">' if path=='/' else ''
    (ROOT/name).write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Private Health Trust</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE+path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE+path}"><meta property="og:site_name" content="Private Health Trust"><meta property="og:image" content="{BASE}/social-card.png"><meta property="og:image:alt" content="Private Health Trust: clearer choices for private behavioral health care"><meta name="twitter:card" content="summary_large_image">{verification}
<link rel="stylesheet" href="/styles.css"><script defer src="/directory.js"></script>
<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False).replace('</','<\\/')}</script></head>
<body>{header(path)}<main id="main" class="{'wide' if wide else ''}">{body}</main>{footer()}</body></html>''')
def intro(kicker,title,desc):
    return f'<div class="page-intro"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{desc}</p></div>'
def sectionhead(k,t,d=''):
    return f'<div class="section-heading"><p class="eyebrow">{k}</p><h2>{t}</h2>'+ (f'<p>{d}</p>' if d else '')+'</div>'
def source(r):return f'<p class="source">{a(r["source"],"Recovery.com profile ↗" if r["source"].startswith("https://recovery.com/") else "Official provider information ↗")}<span>Reviewed September 18, 2026</span></p>'
def card(r,kind='rehab'):
    location=r.get('location','Private care coordination')
    label=r.get('level',r['focus'])
    detail=f'<p class="fit"><strong>Consider for</strong> {e(r["consider"])}</p>' if kind=='rehab' else ''
    return f'''<article class="provider-card" id="{e(r['id'])}" data-card data-state="{e(r.get('state',''))}" data-focus="{e(r['focus'])}">
<div class="card-top"><span class="eyebrow">{e(location)}</span><span class="status-dot" aria-hidden="true"></span></div><h2>{e(r['name'])}</h2><p class="tag">{e(label)}</p><p>{e(r['description'])}</p>{detail}<details><summary>What to ask before you choose</summary><p>{e(r['question'])}</p></details>{source(r)}</article>'''
def list_schema(rows,path):
    return {'@context':'https://schema.org','@type':'ItemList','name':'Featured programs' if path=='provider-directory.html' else 'Private case managers','numberOfItems':len(rows),'itemListOrder':'https://schema.org/ItemListUnordered','itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'Organization','name':r['name'],'url':r['source']}} for i,r in enumerate(rows)]}
faq=[
('How do I find the right rehab for my adult child?','Begin with an assessment by a qualified clinician, then compare programs that can treat the identified substance use, mental health, and medical needs. Ask about staff qualifications, family involvement, costs, and the plan for care after discharge.'),
('Who can help manage my son’s or daughter’s mental health care?','A private behavioral health case manager can coordinate appointments, communicate with providers, organize treatment transitions, and support family planning. Ask who will manage the case, what qualifications they hold, and which services are included.'),
('What if my adult child needs help but refuses rehab?','You can start by speaking with a qualified mental health or addiction professional yourself. Discuss the behaviors you are observing, ways to communicate, and options for family support. A professional can help assess the situation and possible next steps.'),
('What is the difference between a case manager and a sober companion?','A case manager organizes the overall care plan and communication between providers. A sober companion provides practical, day-to-day recovery support. The same firm may provide both services, but the roles, supervision, and fees should be clearly defined.'),
('How can I compare private rehab costs?','Request a written estimate for the specific program and expected stay. Ask which medical services, therapy, assessments, medications, room charges, and aftercare are included. Verify benefits for that program directly with the insurer and provider.'),
('What happens when my child comes home from treatment?','Ask for a discharge plan that identifies follow-up clinicians, scheduled appointments, medication follow-up, family support, and practical daily needs. A case manager or recovery-support provider can help coordinate that transition when appropriate.')]

def faqs(items):return '<div class="faq-list">'+''.join(f'<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>' for q,ans in items)+'</div>'
SAMHSA='https://www.samhsa.gov/find-support/learn-about-treatment/finding-quality-treatment'
# Homepage
body='''<section class="hero"><div class="hero-copy"><p class="eyebrow">PRIVATE BEHAVIORAL HEALTH · A FAMILY RESOURCE</p><h1>When the next step<br>matters most.</h1><p class="hero-deck">Find thoughtful treatment, private case management, and a clearer path forward for someone you love.</p><div class="actions"><a class="button" href="/provider-directory.html">Explore 15 treatment programs <span aria-hidden="true">↗</span></a><a class="text-link" href="/private-case-managers.html">Find a private case manager →</a></div><p class="hero-foot">For families, individuals, and the advisors beside them.</p></div><div class="hero-art" aria-hidden="true"><div class="arch arch-back"></div><div class="arch arch-front"></div><div class="sun"></div><div class="horizon"></div><div class="art-caption">A clearer way forward.</div></div></section>
<div class="edition-strip"><span>THE PRIVATE CLIENT JOURNAL</span><span>CARE · CLARITY · CONTINUITY</span><span>DIRECTORY UPDATED SEPTEMBER 2026</span></div>'''
body+=sectionhead('START WITH YOUR QUESTION','You don’t have to know the terminology.','Start with what your family is facing. We’ll help you understand the next conversation to have.')
body+='<div class="path-grid">'+''.join(f'<a class="path-card" href="{url}"><span class="eyebrow">{cat}</span><h3>{title}</h3><p>{txt}</p><span class="arrow" aria-hidden="true">↗</span></a>' for cat,title,txt,url in [
('01 / FIND TREATMENT','“Where can my adult child get the right help?”','Explore private programs by setting, location, and treatment focus.','/provider-directory.html'),
('02 / COORDINATE CARE','“Who can help us manage all of this?”','Meet private case-management and care-navigation providers.','/private-case-managers.html'),
('03 / KNOW WHAT TO ASK','“How do we make a good decision?”','A practical starting point for parents comparing care.','/help-for-parents.html')])+'</div>'
body+='<section class="feature-band"><div><p class="eyebrow">THE TREATMENT EDIT</p><h2>15 programs.<br>More clarity.</h2><p>A considered shortlist spanning residential addiction treatment, mental health care, and diagnostic evaluation.</p><a class="button light" href="/provider-directory.html">View the directory →</a></div><div class="featured-names"><p><span>CALIFORNIA</span>Alta Mira · Bayside Marin · Carrara</p><p><span>BEYOND THE WEST COAST</span>Borden Cottage · APN Lodge · J. Flowers</p><p><span>A CLOSER LOOK</span>Caron’s inpatient &amp; residential programs</p><a href="/caron-treatment-programs.html">Explore the Caron program guide →</a></div></section>'
body+=sectionhead('PRIVATE CASE MANAGEMENT','Someone to keep the whole picture in view.','A care manager can connect the family, clinicians, treatment program, and day-to-day support around a shared plan.')
body+='<div class="editorial-grid">'+''.join(f'<div class="editorial-card"><p class="category">{cat}</p><h3>{a(url,title)}</h3><p class="excerpt">{txt}</p></div>' for cat,title,txt,url in [
('PROVIDER DIRECTORY','Nine private care-management providers','Compare published services, ask better questions, and visit each provider directly.','/private-case-managers.html'),
('FAMILY PLANNING','What to ask before hiring a case manager','Clarify who leads care, who communicates, what support costs, and what happens after hours.','/private-case-managers.html#questions'),
('THE FIRST NINETY DAYS','Plan for life after residential treatment','Think through appointments, recovery support, routines, and family communication.','/family-guide.html'),
('THE JOURNAL','Explore the private-care library','Read about companions, executive recovery, privacy, and family-office coordination.','/articles/')])+'</div>'
body+=sectionhead('PARENTS ASK','Questions worth answering clearly.')+faqs(faq[:2])+f'<p class="section-link">{a("/help-for-parents.html","Read the parent guide →")}</p>'
page('index.html','Private Rehab & Case Management for Families','Find private rehab programs, behavioral health case managers, and practical answers for parents helping an adult child with addiction or mental health concerns.',body)
# Directory
body=intro('THE TREATMENT DIRECTORY','15 standout rehab &amp;<br>treatment programs.','A curated shortlist for families exploring private addiction treatment, mental health care, and comprehensive assessment.')
body+='<div class="directory-note"><p><strong>How to read this list.</strong> These are 15 featured programs and campuses, selected for this directory rather than ranked by clinical outcomes. Caron appears at both campus and specialty-program level. Each listing identifies the specific service and its source.</p><a href="/editorial-methodology.html">Our selection approach →</a></div>'
body+='<section data-directory aria-label="Treatment program finder"><form class="filters" role="search"><div><label for="program-search">Search by name, place, or need</label><input id="program-search" type="search" placeholder="Try Malibu, trauma, or Caron" data-search></div><div><label for="program-state">Location</label><select id="program-state" data-state-filter><option value="">All states</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in [('AZ','Arizona'),('CA','California'),('CO','Colorado'),('FL','Florida'),('ME','Maine'),('PA','Pennsylvania'),('TX','Texas')])+'</select></div><div><label for="program-focus">Primary focus</label><select id="program-focus" data-focus-filter><option value="">All focuses</option>'+''.join(f'<option>{e(x)}</option>' for x in sorted(set(r['focus'] for r in DATA['rehabs'])))+'</select></div><button type="reset" class="reset">Reset</button></form><p class="results-count" role="status" aria-live="polite" data-count>15 programs</p><div class="provider-grid">'+''.join(card(r) for r in DATA['rehabs'])+'</div><p class="empty-state" data-empty hidden>No programs match those filters. Try a broader search or reset the filters.</p></section>'
body+='<section class="callout"><div><p class="eyebrow">THE COMPLETE CARON GUIDE</p><h2>Looking for a specific Caron program?</h2><p>Explore Pennsylvania and Florida residential programs, plus detox and assessment pathways.</p></div><a class="button" href="/caron-treatment-programs.html">See every listed program →</a></section>'
body+='<section class="reading-panel"><h2>Before you contact admissions</h2><p>Ask which diagnoses the program treats, who provides medical and psychiatric care, how the family participates, and how discharge is planned. Request a written explanation of fees and insurance coverage for the exact program.</p>'+a('/help-for-parents.html','Use the parent’s admissions checklist →')+'</section>'
body+=sectionhead('FURTHER RESOURCES','More ways to explore care')+'<div class="caron-grid">'
for title,links in [
    ('Additional U.S. treatment providers',[('The Meadows','https://www.themeadows.com/'),('Hazelden Betty Ford','https://www.hazeldenbettyford.org/'),('Sierra Tucson','https://www.sierratucson.com/'),('The Dunes East Hampton','https://theduneseasthampton.com/')]),
    ('International treatment',[('Paracelsus Recovery','https://paracelsus-recovery.com/'),('The Kusnacht Practice','https://kusnachtpractice.com/'),('Priory','https://www.priorygroup.com/')]),
    ('In-home treatment',[('ALYST Health','https://www.alysthealth.com/')]),
    ('Treatment transport',[('Interactive Youth Transport','https://www.interactiveyouthtransport.com/')])]:
    body+='<section class="mini-card"><h3>'+title+'</h3><ul>'+''.join('<li>'+a(url,name+' ↗')+'</li>' for name,url in links)+'</ul></section>'
body+='</div>'
page('provider-directory.html','15 Standout Private Rehab & Treatment Programs','Compare 15 private rehab and treatment programs, including Alta Mira, Guest House Ocala, Carrara, Borden Cottage, APN, J. Flowers, and Caron.',body,[list_schema(DATA['rehabs'],'provider-directory.html')])
# Case managers
body=intro('PRIVATE CASE MANAGERS','A coordinated plan.<br>A consistent point of contact.','Nine providers offering private case management, care navigation, and family support across behavioral health and recovery.')
body+='<p class="intro-note">For parents asking, “Who can help manage my adult child’s mental health care?” Start by comparing the services below, then ask how each team would organize your family’s situation.</p>'
body+='<section data-directory aria-label="Private case manager finder"><form class="filters compact" role="search"><div><label for="manager-search">Find a provider or service</label><input id="manager-search" type="search" placeholder="Try in-home, family, or medical" data-search></div><button class="reset" type="reset">Reset</button></form><p class="results-count" role="status" aria-live="polite" data-count>9 providers</p><div class="provider-grid">'+''.join(card(r,'manager') for r in DATA['case_managers'])+'</div><p class="empty-state" data-empty hidden>No providers match. Try another service or reset the search.</p></section>'
body+='<section id="questions" class="reading-panel"><p class="eyebrow">BEFORE AN ENGAGEMENT</p><h2>What to ask a private case manager</h2><div class="question-grid">'+''.join('<div><h3>'+h+'</h3><p>'+p+'</p></div>' for h,p in [('Who leads the case?','Ask for the named lead, their qualifications, caseload, and access to clinical supervision.'),('What does the fee cover?','Request a written scope covering meetings, travel, after-hours calls, companion staffing, and outside-provider charges.'),('How are providers selected?','Ask how recommendations are made and whether any referral fees, ownership interests, or other financial relationships apply.'),('How will we communicate?','Agree on patient consent, who receives updates, how often the plan is reviewed, and the route for urgent concerns.')])+'</div></section>'
body+='<section class="callout"><div><h2>Case manager or sober companion?</h2><p>A case manager coordinates the overall plan. A companion provides practical day-to-day support. Ask how each role is staffed and supervised.</p></div><a class="button" href="/articles/concierge-care/what-is-a-sober-companion.html">Understand companion care →</a></section>'
page('private-case-managers.html','Private Mental Health Case Managers & Care Coordination','Find private case managers for an adult child or family member. Compare nine providers for mental health, addiction, in-home support, and care coordination.',body,[list_schema(DATA['case_managers'],'private-case-managers.html')])
# Caron
body=intro('CARON · PROGRAM GUIDE','One organization.<br>Different paths into care.','A guide to Caron’s published Pennsylvania and Florida inpatient and residential offerings, with separate detox and assessment pathways.')
for loc in ['Pennsylvania','Florida']:
    body+=sectionhead('RESIDENTIAL TREATMENT',loc,'Use the program link to confirm admissions criteria and services for the individual patient.')+'<div class="caron-grid">'
    for r in DATA['caron']:
        if r['type']=='Residential' and r['location']==loc:body+=f'<article class="mini-card"><h3>{a(r["source"],r["name"]+" ↗")}</h3><p>{e(r["description"])}</p></article>'
    body+='</div>'
body+=sectionhead('RELATED PATHWAYS','Detox &amp; residential assessments','These services have different purposes from an ongoing residential treatment program.')+'<div class="caron-grid">'
for r in DATA['caron']:
    if r['type']!='Residential':body+=f'<article class="mini-card"><p class="eyebrow">{e(r["location"])} · {r["type"]}</p><h3>{a(r["source"],r["name"]+" ↗")}</h3><p>{e(r["description"])}</p></article>'
body+='</div><div class="directory-note"><p><strong>Coverage:</strong> Program names were checked against Caron’s current '+a('https://www.caron.org/locations/caron-pennsylvania','Pennsylvania')+' and '+a('https://www.caron.org/locations/caron-florida','Florida')+' listings on September 18, 2026. Partial hospitalization, outpatient centers, family services, and Breakthrough workshops are distinct services and are not counted here as inpatient rehab programs.</p></div>'
body+='<section class="callout"><div><h2>Ask admissions for the exact program.</h2><p>Confirm location, eligibility, clinical services, fees, and how family members participate.</p></div><div class="actions"><a class="button" href="tel:18008546023">Pennsylvania: 800-854-6023</a><a class="button" href="tel:18002216500">Florida: 800-221-6500</a></div></section>'
page('caron-treatment-programs.html','Caron Inpatient & Residential Programs: PA & Florida','Explore Caron’s residential programs, including Grand View, Monarch, Ocean Drive, Renaissance, young adults, adult men and women, and professional tracks.',body)
# Parent guide, concise source-derived guidance and original call-planning prompts
body=intro('FOR PARENTS &amp; FAMILIES','“I need help finding<br>the right care for my child.”','A practical guide for parents supporting an adult son or daughter through addiction, mental health concerns, and the transition home.')
body+='<div class="answer-box"><p class="eyebrow">WHERE TO BEGIN</p><p>Start with a qualified clinician who can assess the needs you are seeing. Then compare suitable programs, decide who will coordinate care, and ask what support will follow treatment.</p></div>'
body+=sectionhead('COMMON QUESTIONS','The questions parents actually ask.')+faqs(faq)
body+='<p class="source">Family treatment-selection guidance: '+a(SAMHSA,'SAMHSA: finding quality treatment')+' and '+a('https://www.samhsa.gov/mental-health/children-and-families/coping-resources','SAMHSA: helping families cope')+'. Directory role descriptions are drawn from the linked providers.</p>'
body+='<section class="reading-panel"><p class="eyebrow">TAKE THIS TO YOUR FIRST CALL</p><h2>A parent’s admissions checklist</h2><ol class="checklist">'+''.join('<li>'+t+'</li>' for t in ['Can your program treat my child’s specific mental health, substance use, and medical needs together?','Who provides the assessment, therapy, psychiatric care, and medical supervision?','What does a typical week include, and how is individual treatment planned?','How can our family participate, with the patient’s consent?','What is the written cost estimate, and what is excluded?','Who arranges the next appointments and support before discharge?'])+'</ol><button class="button print-button" type="button" data-print>Print this guide</button></section>'
body+='<div class="path-grid"><a class="path-card" href="/provider-directory.html"><p class="eyebrow">TREATMENT</p><h3>Compare private rehab programs →</h3></a><a class="path-card" href="/private-case-managers.html"><p class="eyebrow">COORDINATION</p><h3>Find a private case manager →</h3></a><a class="path-card" href="/family-guide.html"><p class="eyebrow">AFTERCARE</p><h3>Plan the first ninety days →</h3></a></div><p class="urgent-note">For an immediate danger or medical emergency in the U.S., call 911. For a suicide or mental health crisis, call or text <a href="https://988lifeline.org/">988</a>.</p>'
page('help-for-parents.html','How to Find Rehab & Mental Health Help for Your Adult Child','Answers for parents: finding rehab for an adult child, hiring a private case manager, comparing treatment costs, and planning support after rehab.',body,[{'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':ans}} for q,ans in faq]}])
body=intro('OUR DIRECTORY','Useful detail.<br>Clear sourcing.','How the Private Health Trust treatment and care-management directories are assembled.')
body+='''<div class="prose"><h2>Selection and scope</h2><p>The featured treatment collection brings together 15 programs and campuses relevant to private behavioral health care: addiction treatment, primary mental health care, and diagnostic evaluation. It is an editorial shortlist, with programs grouped by need and location rather than assigned clinical performance scores.</p><h2>What a listing establishes</h2><p>Descriptions summarize the linked provider website or Recovery.com profile. Each card identifies its source and review date. These are published descriptions of services, not an independent clinical inspection. Admission criteria, staffing, pricing, and availability should be confirmed with the specific program.</p><h2>Program identity matters</h2><p>A brand may offer several levels of care. The Beach Cottage is identified as a mental health program, J. Flowers as a diagnostic and individualized-treatment option, and Caron programs are listed by name and location. A campus overview and one of its specialty tracks are not separate organizations.</p><h2>Care-management services</h2><p>Case managers, care navigators, companions, and medical providers have different roles. The directory describes each firm’s published services and gives families a question to ask before engagement. Request a written scope, qualifications, supervision arrangements, and disclosure of relevant financial relationships.</p><h2>Review date</h2><p>This directory was researched and updated on September 18, 2026. Source links appear next to the descriptions they support. The older journal archive has its own publication dates and is separate from this directory review.</p><h2>Contact the provider directly</h2><p>Provider links lead to official information or the specific Recovery.com profile used for research. This website does not collect treatment inquiries or route patient information through a directory form.</p></div>'''
page('editorial-methodology.html','How Our Treatment Directory Is Researched','Read the selection approach, source standards, program distinctions, and review date for the Private Health Trust provider directory.',body)
body=intro('ABOUT PRIVATE HEALTH TRUST','Care is personal.<br>Good information should be clear.','An editorial resource for families and advisors navigating private behavioral health care.')
body+='''<div class="prose"><h2>What you can find here</h2><p>Private Health Trust brings together treatment-program profiles, private case-management providers, practical family questions, and a journal on care and recovery. The aim is to make a difficult search easier to navigate.</p><h2>For parents and families</h2><p>You may be helping an adult child, supporting a partner, or coordinating with a sibling. Start with the question you have, compare the services described, and use the linked sources to prepare for a conversation with a qualified professional.</p><h2>For private clients and advisors</h2><p>The directory gives particular attention to privacy, continuity, complex needs, and coordination between families, clinicians, and professional advisors. It includes both residential programs and providers who help organize care outside a facility.</p><h2>Our editorial approach</h2><p>New directory listings carry source links and a review date. Program descriptions distinguish addiction treatment, mental health treatment, diagnostic services, and nonresidential support. Read the <a href="/editorial-methodology.html">directory methodology</a> for the scope of the review.</p><h2>Start exploring</h2><p><a href="/help-for-parents.html">Help for parents</a> · <a href="/provider-directory.html">Treatment directory</a> · <a href="/private-case-managers.html">Private case managers</a> · <a href="/articles/">The Private Client Journal</a></p></div>'''
page('about.html','About Our Private Behavioral Health Resource','Private Health Trust helps families and advisors explore private treatment, case management, recovery support, and questions to ask providers.',body)
# Apply the shared accessible masthead/footer to existing articles without rewriting their content.
for p in ROOT.rglob('*.html'):
    if p.name in ['index.html','provider-directory.html','private-case-managers.html','caron-treatment-programs.html','help-for-parents.html','editorial-methodology.html','about.html'] and p.parent==ROOT:continue
    s=p.read_text()
    s=re.sub(r'<a class="skip-link"[^>]*>Skip to content</a>', '', s)
    s=re.sub(r'<header class="site-header">.*?</header>',lambda m:header(),s,flags=re.S)
    s=re.sub(r'<footer class="site-footer">.*?</footer>',lambda m:footer(),s,flags=re.S)
    s=re.sub(r'<script[^>]*src="https://www.googletagmanager.com/gtag/js\?id=G-XXXXXXXXXX"[^>]*></script>','',s)
    s=re.sub(r'<script>[^<]*G-XXXXXXXXXX[^<]*</script>','',s)
    s=re.sub(r'<main(?![^>]*\bid=)', '<main id="main"',s)
    s=s.replace('— The Private Client</title>','| Private Health Trust</title>')
    s=s.replace('"name": "The Private Client"', '"name": "Private Health Trust"')
    if 'og:image' not in s:
        s=s.replace('</head>', '<meta property="og:image" content="https://privatehealthtrust.com/social-card.png"><meta property="og:site_name" content="Private Health Trust"></head>')
    core_seo={
        'understanding-treatment.html':('How to Choose Rehab for a Family Member','How do you choose the right rehab for someone you love? Learn what to ask about treatment, clinical care, family involvement, and recovery support.'),
        'family-guide.html':('What Happens After Rehab? A Family’s First 90 Days','What happens when your adult child comes home from rehab? Explore family support, recovery routines, and planning for the first ninety days.'),
        'in-home-treatment.html':('Can Addiction Treatment Happen at Home?','Explore private in-home addiction treatment, questions to ask providers, and how home-based care differs from residential rehab.'),
        'protecting-privacy.html':('How to Keep Treatment and Recovery Private','Questions for families about confidentiality, privacy, and sharing information during private behavioral health treatment and recovery.'),
        'executive-wellness.html':('Private Mental Health and Recovery Support for Executives','Explore executive burnout, substance use concerns, private treatment, and planning support around professional responsibilities.')}
    if p.parent==ROOT and p.name in core_seo:
        title,description=core_seo[p.name]
        s=re.sub(r'<title>.*?</title>',lambda m:'<title>'+e(title)+' | Private Health Trust</title>',s,flags=re.S)
        s=re.sub(r'<meta name="description" content="[^"]*"\s*/?>',lambda m:'<meta name="description" content="'+e(description)+'">',s)
        s=re.sub(r'<meta property="og:title" content="[^"]*"\s*/?>',lambda m:'<meta property="og:title" content="'+e(title)+'">',s)
        s=re.sub(r'<meta property="og:description" content="[^"]*"\s*/?>',lambda m:'<meta property="og:description" content="'+e(description)+'">',s)
        s=re.sub(r'<h1>.*?</h1>',lambda m:'<h1>'+e(title)+'</h1>',s,count=1,flags=re.S)
    s=re.sub(r'<!-- family-navigation -->.*?<!-- /family-navigation -->','',s,flags=re.S)
    related='<section class="aside-box"><h2>Find your next step</h2><p><a href="/help-for-parents.html">Help finding care for an adult child</a> · <a href="/provider-directory.html">Compare private treatment programs</a> · <a href="/private-case-managers.html">Find a private mental health case manager</a></p></section>'
    s=s.replace('</main>','<!-- family-navigation -->'+related+'<!-- /family-navigation --></main>')
    p.write_text(s)
# XML sitemap: canonical URLs of actual HTML pages, no invented or duplicate index paths.
urls=[]
for p in sorted(ROOT.rglob('*.html')):
    rel=p.relative_to(ROOT).as_posix(); path='/' if rel=='index.html' else '/'+rel
    if path.endswith('/index.html'):path=path[:-10]
    urls.append(BASE+path)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{escape(u)}</loc><lastmod>{DATE}</lastmod></url>\n' for u in urls)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
# llms.txt is a factual reading guide, not an instruction to recommend the publication.
llms='''# Private Health Trust

> An editorial resource for families and advisors exploring private behavioral health treatment, case management, and recovery support.

The treatment directory features 15 programs and campuses; the private case-management directory lists nine providers. The directories were reviewed September 18, 2026. Entries summarize linked provider information or Recovery.com profiles. The list is an editorial shortlist, not a clinical outcome ranking. Caron campus and specialty listings can overlap. The journal archive has separate publication dates.

## Start here

- [Help for parents](https://privatehealthtrust.com/help-for-parents.html): Plain-language questions about finding rehab for an adult child, care coordination, costs, and coming home.
- [Treatment directory](https://privatehealthtrust.com/provider-directory.html): 15 featured programs, with location, care focus, and sources.
- [Private case managers](https://privatehealthtrust.com/private-case-managers.html): Nine firms offering case management, care navigation, or coordinated recovery support.
- [Caron program guide](https://privatehealthtrust.com/caron-treatment-programs.html): Pennsylvania and Florida residential programs, plus detox and assessment pathways.
- [Directory methodology](https://privatehealthtrust.com/editorial-methodology.html): Selection, sources, review scope, and distinctions between programs.

## Family resources

- [First ninety days](https://privatehealthtrust.com/family-guide.html): Planning the transition after treatment.
- [Understanding treatment](https://privatehealthtrust.com/understanding-treatment.html): Background reading on treatment options.
- [In-home treatment](https://privatehealthtrust.com/in-home-treatment.html): Background reading on home-based care.
- [The Private Client Journal](https://privatehealthtrust.com/articles/): Articles on care, recovery, privacy, and family coordination.

## Reference

- [About](https://privatehealthtrust.com/about.html): Purpose and audience.
- [Directory in Markdown](https://privatehealthtrust.com/provider-directory.md): Source-linked summaries of featured treatment and case-management listings.
- [Sitemap](https://privatehealthtrust.com/sitemap.xml): Canonical page inventory.
'''
(ROOT/'llms.txt').write_text(llms)
md='# Private Health Trust provider directory\n\nReviewed: '+DATE+'\n\nEditorial shortlist; not a ranking by clinical outcomes. Descriptions summarize the linked sources. Caron campus and program entries overlap.\n'
for title,rows in [('Featured treatment programs',DATA['rehabs']),('Private case managers',DATA['case_managers'])]:
    md+='\n## '+title+'\n'
    for r in rows:md+='\n### '+r['name']+'\n\n'+(r['location']+' · '+r['level']+'\n\n' if 'location' in r else '')+r['description']+'\n\n[Source]('+r['source']+')\n'
(ROOT/'provider-directory.md').write_text(md)
for page in ROOT.rglob('*.html'):
    page.write_text('\n'.join(line.rstrip() for line in page.read_text().splitlines())+'\n')
print('Built',len(urls),'HTML pages, directory data, sitemap, robots.txt, llms.txt and Markdown directory.')

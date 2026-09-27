# Lead Capture — Setup (15 minutes, one time)

Abhi site ke saare enquiry forms visitor ko WhatsApp pe bhej dete hain. Agar visitor
WhatsApp wala step chhod deta hai, **lead poori tarah gayab ho jaata hai** — naam,
number, kuch bhi record nahi bachta.

`js/lead-capture.js` ab har form submit pe lead ko **pehle save karta hai**, uske baad
WhatsApp khulta hai. Bas ek cheez baaki hai: lead kahan save ho, woh batana.

Neeche wala setup Google Sheet use karta hai — free hai, koi server nahi chahiye, aur
leads phone pe Google Sheets app mein turant dikh jaate hain.

---

## Step 1 — Google Sheet banayein

1. [sheets.new](https://sheets.new) kholiye
2. Naam dijiye: **CA Natasha — Website Leads**
3. Neeche tab ka naam `Sheet1` se badal kar **`Leads`** kar dijiye

## Step 2 — Script paste karein

Usi Sheet mein: **Extensions → Apps Script**

Jo bhi code dikhe use hata kar ye paste kar dijiye:

```javascript
/**
 * CA Natasha & Co. — website lead receiver.
 * Har website form submit yahan aata hai aur "Leads" sheet mein ek row ban jaati hai.
 */

var SHEET_NAME   = 'Leads';
var NOTIFY_EMAIL = '';   // e.g. 'info@canatasha.com' — khaali chhodenge to email nahi aayegi

var HEADERS = ['Received At', 'Form', 'Name', 'Phone', 'Email',
               'Service', 'Page', 'All Fields', 'Referrer'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (err) {
    return reply({ ok: false, error: 'busy' });
  }

  try {
    var data = JSON.parse(e.postData.contents);

    // Phone ya email dono na ho to row banane ka fayda nahi
    if (!data.phone && !data.email) return reply({ ok: false, error: 'no contact' });

    var sheet = getSheet();
    sheet.appendRow([
      new Date(),
      data.form    || '',
      data.name    || '',
      normalisePhone(data.phone),
      data.email   || '',
      data.service || '',
      data.page    || '',
      flatten(data.fields),
      data.referrer || ''
    ]);

    notify(data);
    return reply({ ok: true });

  } catch (err) {
    return reply({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/** Browser kabhi-kabhi GET bhejta hai — endpoint zinda hai ye confirm karne ke liye. */
function doGet() {
  return reply({ ok: true, service: 'CA Natasha lead receiver' });
}

function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

/** Sheet phone ko number bana kar leading zero/plus kha jaata hai — text rakhein. */
function normalisePhone(p) {
  if (!p) return '';
  return "'" + String(p).replace(/\s+/g, ' ').trim();
}

function flatten(fields) {
  if (!fields) return '';
  return Object.keys(fields).map(function (k) {
    return k + ': ' + fields[k];
  }).join(' | ');
}

function notify(data) {
  if (!NOTIFY_EMAIL) return;
  try {
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: 'New website lead — ' + (data.name || 'Unknown') + ' (' + (data.form || '') + ')',
      body: [
        'Name    : ' + (data.name || '-'),
        'Phone   : ' + (data.phone || '-'),
        'Email   : ' + (data.email || '-'),
        'Service : ' + (data.service || '-'),
        'Form    : ' + (data.form || '-'),
        'Page    : ' + (data.url || '-'),
        '',
        flatten(data.fields)
      ].join('\n')
    });
  } catch (err) {
    // Email fail ho to bhi row to ban hi chuki hai — chup rahein
  }
}

function reply(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Agar har lead pe email chahiye, to upar `NOTIFY_EMAIL` mein apna email daal dijiye.

## Step 3 — Deploy karein

1. Upar dayein **Deploy → New deployment**
2. **Select type** (gear icon) → **Web app**
3. Settings:
   - **Execute as** — `Me`
   - **Who has access** — **`Anyone`**  ← ye zaroori hai, warna website se request block ho jayegi
4. **Deploy** → Google permission maangega → **Authorize** → apna account chuniye
   - "Google hasn't verified this app" aaye to: **Advanced → Go to (project name)**
5. Jo **Web app URL** milega use copy kar lijiye. Aisa dikhega:
   `https://script.google.com/macros/s/AKfycbx...../exec`

## Step 4 — URL website mein daalein

`js/lead-capture.js` kholiye, line 21 ke aas-paas ye milega:

```javascript
var LEAD_ENDPOINT = '';
```

Usmein apna URL daal dijiye:

```javascript
var LEAD_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx...../exec';
```

Bas. Deploy kar dijiye.

---

## Test kaise karein

1. Site kholiye, koi bhi enquiry form bhariye, submit kar dijiye
2. WhatsApp khulega — **use band kar dijiye, message mat bhejiye**
3. Google Sheet dekhiye — **row phir bhi aani chahiye**

Yahi poore kaam ka maksad hai: lead ab tab bhi milta hai jab visitor WhatsApp chhod de.

Browser console mein bhi check kar sakte hain:

```javascript
caLeadCapture.configured()   // true hona chahiye
caLeadCapture.pending()      // 0 — koi lead atka hua nahi
```

---

## Kaam kaise karta hai

- Form submit hote hi lead capture ho jaata hai — **WhatsApp khulne se pehle**
- `navigator.sendBeacon` use hota hai, jo page chhodne ke baad bhi request poori karta hai
- Endpoint na chale ya net band ho, to lead browser mein queue ho jaata hai aur
  visitor ke agle page view pe apne aap dobara bhejne ki koshish hoti hai
- Ye script kabhi form ko rok nahi sakta. Kuch bhi fail ho, WhatsApp wala flow
  waisa hi chalta rahega jaisa abhi chalta hai

Kaunse forms capture hote hain (`data-lead` attribute se):

| `data-lead`          | Form                                  | Kitni pages |
|----------------------|---------------------------------------|-------------|
| `quick-callback`     | Homepage ka upar wala callback bar     | 1  |
| `slot-booking`       | Consultation slot booking modal        | 50 |
| `request-quote`      | Request a Quote modal                  | 50 |
| `consultation-modal` | Book Consultation modal                | 7  |
| `inquiry`            | Inquiry & Callback section             | 2  |
| `calc-income-tax`    | Income Tax Calculator ka lead gate     | 1  |
| `calc-hra`           | HRA Calculator ka lead gate            | 1  |
| `calc-emi`           | EMI Calculator ka lead gate            | 1  |

Aage koi naya form banayein to bas `data-lead="कोई-naam"` laga dijiye — apne aap capture hone lagega.

---

## Dhyaan dene layak baatein

**Endpoint public hai.** Kisi bhi client-side form ke saath yahi baat hoti hai — URL
website ke code mein dikhta hai, to koi spam bhej sakta hai. Isme kuch sensitive nahi
hai (sirf likh sakte hain, padh nahi sakte). Spam aane lage to Apps Script mein ek
shared token ya rate limit add kiya ja sakta hai — bataiye to laga dunga.

**Career page ka form abhi capture nahi hota.** Uske andar koi input field hai hi
nahi — woh sirf ek fixed WhatsApp message kholta hai. Usmein naam/phone/resume ke
fields add karne honge, tab capture hoga.

**Ye file deploy folder mein hai.** Isme koi secret nahi hai, par chahein to live
karne se pehle delete kar sakte hain.

let hraCurrentFreq = 'annual';

function handleHraFreqChange(freq) {
  if (hraCurrentFreq === freq) return;
  const basicInput = document.getElementById("stHraBasic");
  const receivedInput = document.getElementById("stHraReceived");
  const rentInput = document.getElementById("stHraRentPaid");

  const bVal = parseFloat(basicInput.value) || 0;
  const rVal = parseFloat(receivedInput.value) || 0;
  const rentVal = parseFloat(rentInput.value) || 0;

  if (freq === 'monthly') {
    basicInput.value = Math.round(bVal / 12);
    receivedInput.value = Math.round(rVal / 12);
    rentInput.value = Math.round(rentVal / 12);

    document.getElementById("lblHraBasic").innerHTML = 'Monthly Basic Salary + DA (&#8377;) *';
    document.getElementById("lblHraReceived").innerHTML = 'Monthly HRA Received from Employer (&#8377;) *';
    document.getElementById("lblHraRentPaid").innerHTML = 'Monthly Rent Paid to Landlord (&#8377;) *';
  } else {
    basicInput.value = Math.round(bVal * 12);
    receivedInput.value = Math.round(rVal * 12);
    rentInput.value = Math.round(rentVal * 12);

    document.getElementById("lblHraBasic").innerHTML = 'Annual Basic Salary + Dearness Allowance (DA) (&#8377;) *';
    document.getElementById("lblHraReceived").innerHTML = 'Annual HRA Received from Employer (&#8377;) *';
    document.getElementById("lblHraRentPaid").innerHTML = 'Total Annual Rent Paid to Landlord (&#8377;) *';
  }
  hraCurrentFreq = freq;
  calculateStandaloneHRA();
}

function calculateStandaloneHRA(e) {
  if (e && e.preventDefault) e.preventDefault();
  var rawBasic = parseFloat(document.getElementById("stHraBasic").value) || 0;
  var rawReceived = parseFloat(document.getElementById("stHraReceived").value) || 0;
  var rawRent = parseFloat(document.getElementById("stHraRentPaid").value) || 0;
  var city = document.getElementById("stHraCityType").value;

  var multiplier = (hraCurrentFreq === 'monthly') ? 12 : 1;
  var basicAnnual = rawBasic * multiplier;
  var receivedAnnual = rawReceived * multiplier;
  var rentAnnual = rawRent * multiplier;

  var cond1 = receivedAnnual;
  var cond2 = Math.max(0, rentAnnual - (0.10 * basicAnnual));
  var cond3Rate = (city === 'metro') ? 0.50 : 0.40;
  var cond3 = cond3Rate * basicAnnual;

  var exemptAnnual = Math.min(cond1, cond2, cond3);
  var taxableAnnual = Math.max(0, receivedAnnual - exemptAnnual);

  var exemptMonthly = Math.round(exemptAnnual / 12);
  var taxableMonthly = Math.round(taxableAnnual / 12);

  // Update summary cards
  document.getElementById("stHraExempt").innerText = "₹ " + Math.round(exemptAnnual).toLocaleString('en-IN');
  document.getElementById("stHraTaxable").innerText = "₹ " + Math.round(taxableAnnual).toLocaleString('en-IN');
  document.getElementById("stHraExemptMonthly").innerText = "₹ " + exemptMonthly.toLocaleString('en-IN') + " / month";
  document.getElementById("stHraTaxableMonthly").innerText = "₹ " + taxableMonthly.toLocaleString('en-IN') + " / month";

  // Update 3 Limbs Values
  document.getElementById("valLimb1").innerText = "₹ " + Math.round(cond1).toLocaleString('en-IN');
  document.getElementById("valLimb2").innerText = "₹ " + Math.round(cond2).toLocaleString('en-IN');
  document.getElementById("valLimb3").innerText = "₹ " + Math.round(cond3).toLocaleString('en-IN');
  document.getElementById("titleLimb3").innerText = (city === 'metro' ? "50%" : "40%") + " of Basic Salary:";
  document.getElementById("descLimb3").innerText = (city === 'metro' ? "Metro city statutory limit" : "Non-metro statutory limit");

  // Determine binding minimum limb
  var limbs = [
    { id: 1, val: cond1, card: document.getElementById("cardLimb1"), badge: document.getElementById("badgeLimb1") },
    { id: 2, val: cond2, card: document.getElementById("cardLimb2"), badge: document.getElementById("badgeLimb2") },
    { id: 3, val: cond3, card: document.getElementById("cardLimb3"), badge: document.getElementById("badgeLimb3") }
  ];

  var minVal = Math.min(cond1, cond2, cond3);
  var minFound = false;

  limbs.forEach(function(l) {
    if (!minFound && l.val === minVal) {
      minFound = true;
      l.card.className = "p-3 rounded-3 border border-2 border-success h-100 position-relative bg-success bg-opacity-10 shadow-sm";
      l.badge.innerHTML = '<span class="badge bg-success">Binding (Least Limb)</span>';
    } else {
      l.card.className = "p-3 rounded-3 border h-100 position-relative bg-white";
      l.badge.innerHTML = '<span class="badge bg-light text-muted border">Higher</span>';
    }
  });

  // Compliance Notice Alerts
  var alertsHtml = '';
  var rentPerMonth = rentAnnual / 12;

  if (rentAnnual > 100000) {
    alertsHtml += `
    <div class="alert alert-warning d-flex align-items-center mb-2" role="alert" style="background:#fff3cd; color:#664d03; border-color:#ffecb5; border-radius:8px; padding:12px 16px;">
      <span class="me-3 fs-4">📋</span>
      <div>
        <strong>Landlord PAN Mandatory (CBDT Circular 08/2013)</strong>: Since your rent exceeds ₹1,00,000 per annum (₹${Math.round(rentPerMonth).toLocaleString('en-IN')}/mo), you must obtain and furnish your Landlord's PAN to your employer to validate HRA exemption without employer TDS disallowance.
      </div>
    </div>`;
  }

  if (rentPerMonth > 50000) {
    alertsHtml += `
    <div class="alert alert-danger d-flex align-items-center mb-2" role="alert" style="background:#f8d7da; color:#842029; border-color:#f5c2c7; border-radius:8px; padding:12px 16px;">
      <span class="me-3 fs-4">⚠️</span>
      <div>
        <strong>Section 194-IB TDS Compliance Alert</strong>: Since rent paid exceeds ₹50,000 per month, the tenant is legally required to deduct 5% TDS under Section 194-IB from the rent and deposit it via Form 26QC challan to avoid penalty interest.
      </div>
    </div>`;
  }

  var alertsContainer = document.getElementById("hraComplianceAlerts");
  if (alertsContainer) {
    alertsContainer.innerHTML = alertsHtml;
  }
}

function handleHraLead(e) {
  e.preventDefault();
  var name = document.getElementById("hraLeadName").value.trim();
  var phone = document.getElementById("hraLeadPhone").value.trim();
  var rawBasic = parseFloat(document.getElementById("stHraBasic").value) || 0;
  var rawRent = parseFloat(document.getElementById("stHraRentPaid").value) || 0;
  var multiplier = (hraCurrentFreq === 'monthly') ? 12 : 1;
  var rentAnnual = rawRent * multiplier;
  var exempt = document.getElementById("stHraExempt").innerText;
  var taxable = document.getElementById("stHraTaxable").innerText;

  if (!name || !phone) return;
  var text = "🏠 *HRA EXEMPTION REPORT & RENT RECEIPT REQUEST* 🏠\n\n"
           + "*Client Name:* " + name + "\n"
           + "*Mobile:* " + phone + "\n"
           + "*Annual Rent Paid:* ₹ " + rentAnnual.toLocaleString('en-IN') + "\n"
           + "*Exempt HRA (Section 10(13A)):* " + exempt + "\n"
           + "*Taxable HRA:* " + taxable + "\n\n"
           + (rentAnnual > 100000 ? "• Note: Landlord PAN required (Rent > ₹1L/yr)\n" : "")
           + (rentAnnual > 600000 ? "• Note: Section 194-IB TDS applicable (Rent > ₹50k/mo)\n" : "")
           + "\n_Sent via canatasha.com HRA Calculator_";
  caWhatsApp(text);
  var submitBtn = e.target.querySelector('button[type="submit"]');
  if (submitBtn) {
    submitBtn.innerHTML = '<i class="fas fa-check-circle me-1"></i> Opening WhatsApp...';
    submitBtn.classList.remove('btn-warning');
    submitBtn.classList.add('btn', 'btn-success');
  }
}

function caWhatsApp(text) {
  var url = 'https://wa.me/919407000157?text=' + encodeURIComponent(text);
  window.open(url, '_blank');
}

function handleModalLeadSubmit(e) {
  e.preventDefault();
  var name = document.getElementById('modalLeadName').value.trim();
  var phone = document.getElementById('modalLeadPhone').value.trim();
  var service = document.getElementById('modalLeadService').value;
  var text = "📋 *NEW CA CONSULTATION REQUEST*\n\n"
           + "*Name:* " + name + "\n*Phone:* " + phone + "\n*Service:* " + service
           + "\n\n_Sent via canatasha.com CA Consultation Modal_";
  caWhatsApp(text);
  var modalEl = document.getElementById('consultationModal');
  if (modalEl && typeof bootstrap !== 'undefined') {
    var modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
  }
}

function handleSidebarLead(e) {
  e.preventDefault();
  var name = document.getElementById('sbLeadName').value.trim();
  var phone = document.getElementById('sbLeadPhone').value.trim();
  var service = document.getElementById('sbLeadService') ? document.getElementById('sbLeadService').value : 'CA Consultation';
  var notes = document.getElementById('sbLeadNotes') ? document.getElementById('sbLeadNotes').value.trim() : '';
  var text = "📋 *URGENT SERVICE ENQUIRY*\n\n"
           + "*Name:* " + name + "\n*Mobile:* " + phone + "\n*Service:* " + service
           + (notes ? ("\n*Notes:* " + notes) : "")
           + "\n\n_Sent from canatasha.com page sidebar_";
  caWhatsApp(text);
}

// Initial compute
document.addEventListener('DOMContentLoaded', calculateStandaloneHRA);

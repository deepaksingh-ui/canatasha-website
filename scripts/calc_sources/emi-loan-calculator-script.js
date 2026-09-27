let currentLoanPreset = 'home';

function setEmiPreset(preset, principal, rate, tenure, btn) {
  currentLoanPreset = preset;
  document.getElementById("stEmiPrincipal").value = principal;
  document.getElementById("stEmiRate").value = rate;
  document.getElementById("stEmiTenure").value = tenure;

  document.querySelectorAll('#emiPresetsGroup .btn').forEach(b => {
    b.classList.remove('btn-danger', 'active');
    b.classList.add('btn-outline-danger');
  });
  if (btn) {
    btn.classList.remove('btn-outline-danger');
    btn.classList.add('btn-danger', 'active');
  }
  calculateStandaloneEMI();
}

function calculateStandaloneEMI(e) {
  if (e && e.preventDefault) e.preventDefault();
  var p = parseFloat(document.getElementById("stEmiPrincipal").value) || 0;
  var rateAnnual = parseFloat(document.getElementById("stEmiRate").value) || 0;
  var tenureYears = parseFloat(document.getElementById("stEmiTenure").value) || 0;

  var r = rateAnnual / 12 / 100;
  var n = tenureYears * 12;

  if (p > 0 && r > 0 && n > 0) {
    var emi = (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    var totalPayment = emi * n;
    var totalInterest = totalPayment - p;

    document.getElementById("stEmiMonthly").innerText = "₹ " + Math.round(emi).toLocaleString('en-IN');
    document.getElementById("stEmiInterest").innerText = "₹ " + Math.round(totalInterest).toLocaleString('en-IN');
    document.getElementById("stEmiTotal").innerText = "₹ " + Math.round(totalPayment).toLocaleString('en-IN');

    // Visual Ratio Bar
    var principalPct = ((p / totalPayment) * 100).toFixed(1);
    var interestPct = ((totalInterest / totalPayment) * 100).toFixed(1);

    var splitEl = document.getElementById("emiSplitRatio");
    if (splitEl) splitEl.innerText = `Principal ${principalPct}% | Interest ${interestPct}%`;

    var barP = document.getElementById("barEmiPrincipal");
    var barI = document.getElementById("barEmiInterest");
    if (barP) barP.style.width = principalPct + '%';
    if (barI) barI.style.width = interestPct + '%';

    var legP = document.getElementById("legendEmiPrincipal");
    var legI = document.getElementById("legendEmiInterest");
    if (legP) legP.innerText = "₹ " + Math.round(p).toLocaleString('en-IN');
    if (legI) legI.innerText = "₹ " + Math.round(totalInterest).toLocaleString('en-IN');

    // Generate Year-by-Year Amortization Schedule Table
    var amortBody = document.getElementById("emiAmortBody");
    if (amortBody) {
      var rowsHtml = '';
      var balance = p;
      var totalYears = Math.min(Math.ceil(tenureYears), 40);

      for (var y = 1; y <= totalYears; y++) {
        var openingBal = balance;
        var yearlyInterest = 0;
        var yearlyPrincipal = 0;

        for (var m = 1; m <= 12; m++) {
          if (balance <= 0) break;
          var monthInterest = balance * r;
          var monthPrincipal = emi - monthInterest;
          if (monthPrincipal > balance) {
            monthPrincipal = balance;
            monthInterest = 0;
          }
          yearlyInterest += monthInterest;
          yearlyPrincipal += monthPrincipal;
          balance -= monthPrincipal;
        }

        var yearlyTotal = yearlyPrincipal + yearlyInterest;
        if (balance < 1) balance = 0;

        rowsHtml += `
        <tr>
          <td class="fw-bold">Year ${y}</td>
          <td>₹ ${Math.round(openingBal).toLocaleString('en-IN')}</td>
          <td class="text-success fw-semibold">₹ ${Math.round(yearlyPrincipal).toLocaleString('en-IN')}</td>
          <td class="text-danger">₹ ${Math.round(yearlyInterest).toLocaleString('en-IN')}</td>
          <td class="fw-bold text-dark">₹ ${Math.round(yearlyTotal).toLocaleString('en-IN')}</td>
          <td class="fw-semibold">₹ ${Math.round(balance).toLocaleString('en-IN')}</td>
        </tr>`;

        if (balance <= 0) break;
      }
      amortBody.innerHTML = rowsHtml;
    }

    var resBox = document.getElementById("standaloneEmiResult");
    if (resBox) resBox.style.display = "block";
  }
}

function handleEmiLead(e) {
  e.preventDefault();
  var name = document.getElementById("emiLeadName").value.trim();
  var phone = document.getElementById("emiLeadPhone").value.trim();
  var p = document.getElementById("stEmiPrincipal").value;
  var rate = document.getElementById("stEmiRate").value;
  var tenure = document.getElementById("stEmiTenure").value;
  var emi = document.getElementById("stEmiMonthly").innerText;
  var interest = document.getElementById("stEmiInterest").innerText;
  var total = document.getElementById("stEmiTotal").innerText;

  if (!name || !phone) return;
  var text = "💼 *BANK LOAN CMA DATA & CA PROJECT REPORT REQUEST* 💼\n\n"
           + "*Client Name:* " + name + "\n"
           + "*Mobile:* " + phone + "\n"
           + "*Loan Details:*\n"
           + "• Loan Amount: ₹ " + (parseFloat(p) || 0).toLocaleString('en-IN') + "\n"
           + "• Interest Rate: " + rate + "%\n"
           + "• Tenure: " + tenure + " Years\n"
           + "• Computed Monthly EMI: " + emi + "\n"
           + "• Total Interest Outflow: " + interest + "\n"
           + "• Total Repayment: " + total + "\n\n"
           + "_Sent via canatasha.com EMI Loan Calculator_";
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
document.addEventListener('DOMContentLoaded', calculateStandaloneEMI);

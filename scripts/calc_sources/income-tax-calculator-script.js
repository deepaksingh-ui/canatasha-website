/* ------------------------------------------------------------------
   FY 2025-26 / AY 2026-27  (Finance Act 2025)
   New regime slabs: 4L nil | 4-8L 5% | 8-12L 10% | 12-16L 15%
                     16-20L 20% | 20-24L 25% | 24L+ 30%
   87A rebate (new): full relief up to Rs.12,00,000 taxable, max Rs.60,000
   Section 87A Marginal relief: if excess > 0 && taxNew > excess, taxNew = excess (break-even: Rs.12,70,588)
   Surcharge Marginal Relief at Rs.50L, Rs.1Cr, Rs.2Cr (and Rs.5Cr in old)
   ------------------------------------------------------------------ */
var NEW_SLABS_FY2526 = [
  [400000, 0.00], [800000, 0.05], [1200000, 0.10], [1600000, 0.15],
  [2000000, 0.20], [2400000, 0.25], [Infinity, 0.30]
];

function slabTax(taxable, slabs) {
  var tax = 0, lower = 0;
  for (var i = 0; i < slabs.length; i++) {
    var upper = slabs[i][0], rate = slabs[i][1];
    if (taxable > lower) {
      tax += (Math.min(taxable, upper) - lower) * rate;
    }
    lower = upper;
    if (taxable <= upper) break;
  }
  return tax;
}

function oldSlabsFor(ageCategory) {
  var exempt = ageCategory === 'superSenior' ? 500000
             : ageCategory === 'senior'      ? 300000
             : 250000;
  var slabs = [[exempt, 0.00]];
  if (exempt < 500000) slabs.push([500000, 0.05]);
  slabs.push([1000000, 0.20]);
  slabs.push([Infinity, 0.30]);
  return slabs;
}

/* Surcharge rate based on taxable income */
function surchargeRate(totalIncome, regime) {
  if (totalIncome <= 5000000) return 0;
  if (totalIncome <= 10000000) return 0.10;
  if (totalIncome <= 20000000) return 0.15;
  if (regime === 'new') return 0.25;
  return totalIncome <= 50000000 ? 0.25 : 0.37;
}

/* Computes base tax, 87A rebate & marginal relief, surcharge with marginal relief, cess & final tax */
function computeRegimeTax(taxable, slabs, regime) {
  var baseTax = slabTax(taxable, slabs);
  var rebate = 0;
  var isMarginal87A = false;

  if (regime === 'new') {
    if (taxable <= 1200000) {
      rebate = Math.min(baseTax, 60000);
      baseTax = Math.max(0, baseTax - rebate);
    } else {
      // Statutory Section 87A Marginal Relief formula:
      // If excess > 0 && taxNew > excess, taxNew = excess; break-even is Rs. 12,70,588
      var excess = taxable - 1200000;
      if (excess > 0 && baseTax > excess) {
        rebate = baseTax - excess;
        baseTax = excess;
        isMarginal87A = true;
      }
    }
  } else {
    if (taxable <= 500000) {
      rebate = Math.min(baseTax, 12500);
      baseTax = Math.max(0, baseTax - rebate);
    }
  }

  // Surcharge with Marginal Relief
  var surRate = surchargeRate(taxable, regime);
  var surcharge = Math.round(baseTax * surRate);

  if (surRate > 0) {
    var thresholds = [5000000, 10000000, 20000000];
    if (regime === 'old') thresholds.push(50000000);

    var thresh = 0;
    for (var t = thresholds.length - 1; t >= 0; t--) {
      if (taxable > thresholds[t]) {
        thresh = thresholds[t];
        break;
      }
    }

    if (thresh > 0) {
      var taxAtThresh = slabTax(thresh, slabs);
      var surRateAtThresh = surchargeRate(thresh, regime);
      var surAtThresh = Math.round(taxAtThresh * surRateAtThresh);
      var maxTotalTax = (taxAtThresh + surAtThresh) + (taxable - thresh);

      if ((baseTax + surcharge) > maxTotalTax) {
        surcharge = Math.max(0, maxTotalTax - baseTax);
      }
    }
  }

  var cess = Math.round((baseTax + surcharge) * 0.04);
  var finalTax = Math.round(baseTax + surcharge + cess);

  return {
    taxable: taxable,
    baseTax: baseTax,
    rebate: rebate,
    isMarginal87A: isMarginal87A,
    surcharge: surcharge,
    cess: cess,
    finalTax: finalTax
  };
}

function inr(n) { return "\u20B9 " + Math.round(n).toLocaleString('en-IN'); }

function calculateStandaloneIncomeTax(e) {
  if (e && e.preventDefault) e.preventDefault();
  var gross = parseFloat(document.getElementById("stGrossIncome").value) || 0;
  var age = document.getElementById("stAgeCategory").value;
  var isSalaried = document.getElementById("stEmpSalaried") ? document.getElementById("stEmpSalaried").checked : true;
  var c80 = parseFloat(document.getElementById("st80C").value) || 0;
  var d80 = parseFloat(document.getElementById("st80D").value) || 0;
  var other = parseFloat(document.getElementById("stOtherDed").value) || 0;
  var totalDed = Math.min(150000, c80) + d80 + other;

  /* Standard deductions: only for salaried individuals */
  var stdDedNew = isSalaried ? 75000 : 0;
  var stdDedOld = isSalaried ? 50000 : 0;

  /* Update standard deduction displays and badge */
  var stdNewEl = document.getElementById("stNewStdDed");
  if (stdNewEl) stdNewEl.innerText = inr(stdDedNew);
  var badgeNewStd = document.getElementById("badgeNewStd");
  if (badgeNewStd) badgeNewStd.innerText = isSalaried ? "₹75,000 Std Ded" : "No Std Ded";

  var stdOldEl = document.getElementById("stOldStdDed");
  if (stdOldEl) stdOldEl.innerText = inr(stdDedOld);

  /* New regime */
  var taxableNew = Math.max(0, gross - stdDedNew);
  var resNew = computeRegimeTax(taxableNew, NEW_SLABS_FY2526, 'new');

  /* Old regime */
  var taxableOld = Math.max(0, gross - stdDedOld - totalDed);
  var resOld = computeRegimeTax(taxableOld, oldSlabsFor(age), 'old');

  /* Take-home calculations */
  var takeHomeNewAnnual = Math.max(0, gross - resNew.finalTax);
  var takeHomeNewMonthly = Math.round(takeHomeNewAnnual / 12);
  var takeHomeOldAnnual = Math.max(0, gross - resOld.finalTax);
  var takeHomeOldMonthly = Math.round(takeHomeOldAnnual / 12);

  /* Update DOM */
  document.getElementById("stNewTaxable").innerText = inr(taxableNew);
  var rebateText = "Not applicable above \u20B912.70L";
  if (taxableNew <= 1200000) {
    rebateText = inr(resNew.rebate) + " (Full 87A Relief)";
  } else if (resNew.isMarginal87A) {
    rebateText = inr(resNew.rebate) + " (87A Marginal Relief)";
  }
  document.getElementById("stNewRebate").innerText = rebateText;
  
  var surCessTotalNew = resNew.surcharge + resNew.cess;
  var newCessEl = document.getElementById("stNewCess");
  if (newCessEl) {
    newCessEl.innerText = resNew.surcharge > 0 
      ? inr(resNew.surcharge) + " (Sur.) + " + inr(resNew.cess) + " (Cess)"
      : inr(resNew.cess);
  }

  document.getElementById("stNewTaxPayable").innerText = inr(resNew.finalTax);
  var newMonthlyEl = document.getElementById("stNewMonthlyTakeHome");
  if (newMonthlyEl) newMonthlyEl.innerText = inr(takeHomeNewMonthly);

  document.getElementById("stOldTaxable").innerText = inr(taxableOld);
  document.getElementById("stOldTotalDed").innerText = inr(totalDed);

  var oldCessEl = document.getElementById("stOldCess");
  if (oldCessEl) {
    oldCessEl.innerText = resOld.surcharge > 0 
      ? inr(resOld.surcharge) + " (Sur.) + " + inr(resOld.cess) + " (Cess)"
      : inr(resOld.cess);
  }

  document.getElementById("stOldTaxPayable").innerText = inr(resOld.finalTax);
  var oldMonthlyEl = document.getElementById("stOldMonthlyTakeHome");
  if (oldMonthlyEl) oldMonthlyEl.innerText = inr(takeHomeOldMonthly);

  var rec = document.getElementById("stTaxRecommendation");
  if (resNew.finalTax < resOld.finalTax) {
    var diff = resOld.finalTax - resNew.finalTax;
    rec.innerText = "\uD83D\uDCA1 CA Recommendation: The New Tax Regime saves you " + inr(diff) + " annually (" + inr(Math.round(diff/12)) + "/month extra take-home).";
    rec.className = "mt-4 p-3 rounded bg-success bg-opacity-10 text-success border border-success text-center fw-bold fs-6";
  } else if (resOld.finalTax < resNew.finalTax) {
    var diff = resNew.finalTax - resOld.finalTax;
    rec.innerText = "\uD83D\uDCA1 CA Recommendation: The Old Tax Regime saves you " + inr(diff) + " annually due to your itemized deductions.";
    rec.className = "mt-4 p-3 rounded bg-primary bg-opacity-10 text-primary border border-primary text-center fw-bold fs-6";
  } else {
    rec.innerText = "\u2705 Both regimes yield identical tax liability for your income structure.";
    rec.className = "mt-4 p-3 rounded bg-warning bg-opacity-10 text-warning-emphasis border border-warning text-center fw-bold fs-6";
  }
}

function handleCalculatorLead(e, calcType) {
  e.preventDefault();
  var name = document.getElementById("calcLeadName").value.trim();
  var phone = document.getElementById("calcLeadPhone").value.trim();
  var gross = document.getElementById("stGrossIncome").value;
  var isSalaried = document.getElementById("stEmpSalaried") ? document.getElementById("stEmpSalaried").checked : true;
  var empType = isSalaried ? "Salaried Individual" : "Self-Employed / Business";
  var taxNew = document.getElementById("stNewTaxPayable").innerText;
  var taxOld = document.getElementById("stOldTaxPayable").innerText;
  var takeHomeNew = document.getElementById("stNewMonthlyTakeHome") ? document.getElementById("stNewMonthlyTakeHome").innerText : "";
  var recText = document.getElementById("stTaxRecommendation") ? document.getElementById("stTaxRecommendation").innerText : "";

  if (!name || !phone) return;
  var text = "📊 *PERSONALIZED CA TAX OPTIMIZATION REQUEST* 📊\n\n"
           + "*Client Name:* " + name + "\n"
           + "*Mobile:* " + phone + "\n"
           + "*Employment:* " + empType + "\n"
           + "*Annual Gross Income:* ₹ " + (parseFloat(gross) || 0).toLocaleString('en-IN') + "\n\n"
           + "*Tax Liability Summary:*\n"
           + "• New Regime Tax: " + taxNew + (takeHomeNew ? (" (Take-Home: " + takeHomeNew + "/mo)") : "") + "\n"
           + "• Old Regime Tax: " + taxOld + "\n"
           + "• Analysis: " + recText + "\n\n"
           + "_Sent via canatasha.com Income Tax Calculator_";
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

// Auto-calculate on initial page load
document.addEventListener('DOMContentLoaded', calculateStandaloneIncomeTax);

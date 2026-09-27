let currentGSTRate = 18;

const rateDescriptions = {
    0: '0% Nil Rated: Unbranded staples, fresh milk, vegetables, grains, seeds',
    0.25: '0.25% Special Rate: Cut & polished diamonds and rough precious stones',
    3: '3% Precious Metals: Gold, silver, jewellery, platinum coins',
    5: '5% Merit Goods: Packaged basic food, economy footwear, domestic LPG, medicines',
    12: '12% Standard Concessional: Processed foods, umbrella, apparel above threshold, business services',
    18: '18% Standard Main Rate: Capital goods, financial services, IT, majority of industrial products',
    28: '28% Peak / Luxury Rate: Automobiles, air conditioners, cement, aerated drinks, betting'
};

function syncAmountToSlider(val) {
    const num = parseFloat(val) || 0;
    const slider = document.getElementById('gstSlider');
    if (num <= 1000000 && num >= 1000) {
        slider.value = num;
    }
    calculateGST();
}

function syncSliderToAmount(val) {
    document.getElementById('gstAmount').value = val;
    calculateGST();
}

function setGSTRate(rate, btn) {
    currentGSTRate = rate;
    document.querySelectorAll('#gstRateGroup .btn').forEach(b => {
        b.classList.remove('btn-danger', 'active');
        b.classList.add('btn-outline-danger');
    });
    btn.classList.remove('btn-outline-danger');
    btn.classList.add('btn-danger', 'active');
    
    const descEl = document.getElementById('gstRateDesc');
    if (descEl && rateDescriptions[rate] !== undefined) {
        descEl.textContent = rateDescriptions[rate];
    }
    calculateGST();
}

function calculateGST() {
    const amount = parseFloat(document.getElementById('gstAmount').value) || 0;
    const isInclusive = document.getElementById('gstInclusive').checked;
    
    let baseAmount = 0;
    let gstAmount = 0;
    let totalAmount = 0;

    if (isInclusive) {
        baseAmount = (amount * 100) / (100 + currentGSTRate);
        gstAmount = amount - baseAmount;
        totalAmount = amount;
    } else {
        baseAmount = amount;
        gstAmount = (amount * currentGSTRate) / 100;
        totalAmount = amount + gstAmount;
    }

    const halfGst = gstAmount / 2;

    const resBase = document.getElementById('resBase');
    const resGST = document.getElementById('resGST');
    const resTotal = document.getElementById('resTotal');
    const resCgstSgst = document.getElementById('resCgstSgst');
    const resIgst = document.getElementById('resIgst');

    if (resBase) resBase.textContent = '₹ ' + Math.round(baseAmount).toLocaleString('en-IN');
    if (resGST) resGST.textContent = '₹ ' + Math.round(gstAmount).toLocaleString('en-IN');
    if (resTotal) resTotal.textContent = '₹ ' + Math.round(totalAmount).toLocaleString('en-IN');
    if (resCgstSgst) resCgstSgst.textContent = '₹ ' + Math.round(halfGst).toLocaleString('en-IN') + ' + ₹ ' + Math.round(halfGst).toLocaleString('en-IN');
    if (resIgst) resIgst.textContent = '₹ ' + Math.round(gstAmount).toLocaleString('en-IN');

    // Visual Segmented Bar
    const totalCalc = totalAmount > 0 ? totalAmount : 1;
    const basePct = ((baseAmount / totalCalc) * 100).toFixed(1);
    const halfGstPct = (((halfGst) / totalCalc) * 100).toFixed(1);
    const gstPct = ((gstAmount / totalCalc) * 100).toFixed(1);

    const splitEl = document.getElementById('gstSplitRatio');
    if (splitEl) splitEl.textContent = `Base ${basePct}% | GST ${gstPct}%`;

    const barBase = document.getElementById('barBase');
    const barCgst = document.getElementById('barCgst');
    const barSgst = document.getElementById('barSgst');
    if (barBase) barBase.style.width = basePct + '%';
    if (barCgst) barCgst.style.width = halfGstPct + '%';
    if (barSgst) barSgst.style.width = halfGstPct + '%';

    const legBase = document.getElementById('legendBase');
    const legCgst = document.getElementById('legendCgst');
    const legSgst = document.getElementById('legendSgst');
    if (legBase) legBase.textContent = '₹ ' + Math.round(baseAmount).toLocaleString('en-IN');
    if (legCgst) legCgst.textContent = '₹ ' + Math.round(halfGst).toLocaleString('en-IN');
    if (legSgst) legSgst.textContent = '₹ ' + Math.round(halfGst).toLocaleString('en-IN');

    // Side-by-side 4-Slab Comparison Table (5%, 12%, 18%, 28%)
    const compTableBody = document.getElementById('gstComparisonBody');
    if (compTableBody) {
        const slabs = [5, 12, 18, 28];
        let rowsHtml = '';
        slabs.forEach(slab => {
            let sBase = 0;
            let sGst = 0;
            let sTotal = 0;
            if (isInclusive) {
                sBase = (amount * 100) / (100 + slab);
                sGst = amount - sBase;
                sTotal = amount;
            } else {
                sBase = amount;
                sGst = (amount * slab) / 100;
                sTotal = amount + sGst;
            }
            const sHalf = sGst / 2;
            const isCurrent = (currentGSTRate === slab);
            const rowClass = isCurrent ? 'table-row-highlight fw-bold' : '';
            const activeBadge = isCurrent ? '<span class="badge bg-danger ms-1">Active</span>' : '';
            rowsHtml += `
            <tr class="${rowClass}">
                <td class="text-start ps-3"><span class="badge ${isCurrent ? 'bg-danger' : 'bg-secondary'} me-1">${slab}%</span>${activeBadge}</td>
                <td>₹ ${Math.round(sBase).toLocaleString('en-IN')}</td>
                <td>₹ ${Math.round(sHalf).toLocaleString('en-IN')} + ₹ ${Math.round(sHalf).toLocaleString('en-IN')}</td>
                <td class="fw-bold text-dark">₹ ${Math.round(sTotal).toLocaleString('en-IN')}</td>
            </tr>`;
        });
        compTableBody.innerHTML = rowsHtml;
    }
}

// Initial compute
document.addEventListener('DOMContentLoaded', calculateGST);

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
  var service = document.getElementById('sbLeadService') ? document.getElementById('sbLeadService').value : 'GST Consultation';
  var notes = document.getElementById('sbLeadNotes') ? document.getElementById('sbLeadNotes').value.trim() : '';
  var amt = document.getElementById('gstAmount') ? document.getElementById('gstAmount').value : '';
  var rate = currentGSTRate;
  var total = document.getElementById('resTotal') ? document.getElementById('resTotal').textContent : '';
  var gstVal = document.getElementById('resGST') ? document.getElementById('resGST').textContent : '';
  var mode = document.getElementById('gstInclusive').checked ? 'Inclusive' : 'Exclusive';

  var text = "📋 *GST CONSULTATION & ADVISORY REQUEST*\n\n"
           + "*Name:* " + name + "\n*Mobile:* " + phone + "\n*Service:* " + service + "\n"
           + "*Calculation Details:*\n"
           + "• Input Amount: ₹" + (parseFloat(amt) || 0).toLocaleString('en-IN') + " (" + mode + ")\n"
           + "• GST Rate: " + rate + "%\n"
           + "• GST Tax Value: " + gstVal + "\n"
           + "• Total Invoice Value: " + total + "\n"
           + (notes ? ("*Client Query:* " + notes + "\n") : "")
           + "\n_Sent via canatasha.com GST Calculator_";
  caWhatsApp(text);
  var submitBtn = e.target.querySelector('button[type="submit"]');
  if (submitBtn) {
    submitBtn.innerHTML = '<i class="fas fa-check-circle me-1"></i> Opening WhatsApp...';
    submitBtn.classList.remove('btn-submit-lead');
    submitBtn.classList.add('btn', 'btn-success', 'w-100');
  }
}

/**
 * CA Natasha & Company - Unified Reusable Header Web Component
 * Automatically highlights the active page link and handles responsive behaviors
 */
(function() {
  'use strict';

  function initHeaderComponent() {
    var path = window.location.pathname.toLowerCase();
    var pageName = path.substring(path.lastIndexOf('/') + 1) || 'index.html';

    var navItems = document.querySelectorAll('.main-nav > li, .mobile-nav-list > li');
    navItems.forEach(function(item) {
      var link = item.querySelector('a');
      if (!link) return;
      var href = link.getAttribute('href');
      if (!href) return;
      var cleanHref = href.split('#')[0].split('?')[0].toLowerCase();

      if (cleanHref === pageName || (pageName === 'index.html' && cleanHref === 'index.html')) {
        item.classList.add('active');
        link.classList.add('active');
      }
    });

    // Close offcanvas when clicking any navigation link
    var mobileLinks = document.querySelectorAll('#mobileMenu .mobile-nav-link');
    mobileLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        var offcanvasEl = document.getElementById('mobileMenu');
        if (offcanvasEl && typeof bootstrap !== 'undefined' && bootstrap.Offcanvas) {
          var bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvasEl);
          if (bsOffcanvas) bsOffcanvas.hide();
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeaderComponent);
  } else {
    initHeaderComponent();
  }
})();

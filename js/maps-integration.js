// Source: Google Maps Platform Code Assist
/**
 * CA Natasha & Co. — Google Maps Platform Integration
 * ---------------------------------------------------------------------------
 * Features:
 * 1. 1-Click "Get Directions" navigation helpers
 * 2. Modern Google Places Autocomplete (Places API New) on City/Location fields
 * 3. Graceful fallback for offline / restricted environments
 * ---------------------------------------------------------------------------
 */
(function () {
  'use strict';

  var API_KEY = 'AIzaSyDhgSsIVd-kuaXLxzcdU5IecA2E35AVWwQ';
  var SOLUTION_ID = 'gmp_git_agentskills_v1';

  /* ----------------------------------------------------------- Dynamic Loader */
  function loadGoogleMapsBootstrap() {
    return new Promise(function (resolve, reject) {
      if (window.google && window.google.maps && window.google.maps.importLibrary) {
        return resolve(window.google.maps);
      }
      if (document.getElementById('gmp-maps-js-sdk')) {
        var existing = document.getElementById('gmp-maps-js-sdk');
        existing.addEventListener('load', function () { resolve(window.google.maps); });
        existing.addEventListener('error', reject);
        return;
      }
      var script = document.createElement('script');
      script.id = 'gmp-maps-js-sdk';
      script.async = true;
      script.defer = true;
      script.src = 'https://maps.googleapis.com/maps/api/js?key=' + encodeURIComponent(API_KEY) +
                   '&libraries=places&v=weekly';
      script.onload = function () {
        if (window.google && window.google.maps) {
          resolve(window.google.maps);
        } else {
          reject(new Error('Google Maps SDK loaded but window.google.maps not available'));
        }
      };
      script.onerror = function (err) {
        console.warn('Google Maps Platform script load deferred or blocked:', err);
        reject(err);
      };
      document.head.appendChild(script);
    });
  }

  /* ----------------------------------------------- City / Location Autocomplete */
  function setupCityAutocomplete() {
    var cityInput = document.getElementById('f-city');
    if (!cityInput) return;

    // Create dropdown container
    var wrapper = document.createElement('div');
    wrapper.className = 'gmp-autocomplete-wrap';
    wrapper.style.position = 'relative';
    cityInput.parentNode.insertBefore(wrapper, cityInput);
    wrapper.appendChild(cityInput);

    var dropdown = document.createElement('div');
    dropdown.className = 'gmp-autocomplete-dropdown';
    dropdown.style.display = 'none';
    dropdown.style.position = 'absolute';
    dropdown.style.top = '100%';
    dropdown.style.left = '0';
    dropdown.style.right = '0';
    dropdown.style.zIndex = '999';
    dropdown.style.backgroundColor = '#ffffff';
    dropdown.style.border = '1px solid #dcdcdc';
    dropdown.style.borderRadius = '0 0 8px 8px';
    dropdown.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)';
    dropdown.style.maxHeight = '240px';
    dropdown.style.overflowY = 'auto';
    wrapper.appendChild(dropdown);

    loadGoogleMapsBootstrap().then(async function (maps) {
      try {
        var placesLib = await maps.importLibrary('places');
        var sessionToken = new placesLib.AutocompleteSessionToken();

        var debounceTimer = null;

        cityInput.addEventListener('input', function () {
          var query = cityInput.value.trim();
          clearTimeout(debounceTimer);
          if (query.length < 2) {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            return;
          }

          debounceTimer = setTimeout(async function () {
            try {
              if (placesLib.AutocompleteSuggestion && placesLib.AutocompleteSuggestion.fetchAutocompleteSuggestions) {
                var res = await placesLib.AutocompleteSuggestion.fetchAutocompleteSuggestions({
                  input: query,
                  sessionToken: sessionToken,
                  includedRegionCodes: ['in'],
                  includedPrimaryTypes: ['locality', 'administrative_area_level_2', 'postal_code']
                });

                renderSuggestions(res.suggestions || []);
              } else if (maps.places && maps.places.AutocompleteService) {
                // Compatibility fallback
                var service = new maps.places.AutocompleteService();
                service.getPlacePredictions({
                  input: query,
                  componentRestrictions: { country: 'in' },
                  types: ['(cities)']
                }, function (predictions) {
                  renderLegacyPredictions(predictions || []);
                });
              }
            } catch (err) {
              console.warn('Autocomplete fetch note:', err.message);
            }
          }, 250);
        });

        function renderSuggestions(suggestions) {
          dropdown.innerHTML = '';
          if (!suggestions || suggestions.length === 0) {
            dropdown.style.display = 'none';
            return;
          }

          suggestions.slice(0, 5).forEach(function (s) {
            var item = document.createElement('div');
            item.className = 'gmp-autocomplete-item';
            item.style.padding = '10px 14px';
            item.style.cursor = 'pointer';
            item.style.borderBottom = '1px solid #f0f0f0';
            item.style.fontSize = '0.92rem';
            item.style.color = '#1f2937';
            item.style.display = 'flex';
            item.style.alignItems = 'center';
            item.style.gap = '8px';

            var text = s.placePrediction ? s.placePrediction.text.toString() : (s.description || query);
            item.innerHTML = '<span style="color:#d97706">📍</span> <span>' + escapeHTML(text) + '</span>';

            item.addEventListener('mouseenter', function () {
              item.style.backgroundColor = '#f8fafc';
            });
            item.addEventListener('mouseleave', function () {
              item.style.backgroundColor = '#ffffff';
            });

            item.addEventListener('click', function () {
              cityInput.value = text;
              dropdown.style.display = 'none';
              dropdown.innerHTML = '';
              // Refresh session token after place selection
              sessionToken = new placesLib.AutocompleteSessionToken();
              cityInput.dispatchEvent(new Event('change', { bubbles: true }));
            });

            dropdown.appendChild(item);
          });

          dropdown.style.display = 'block';
        }

        function renderLegacyPredictions(predictions) {
          dropdown.innerHTML = '';
          if (!predictions || predictions.length === 0) {
            dropdown.style.display = 'none';
            return;
          }

          predictions.slice(0, 5).forEach(function (p) {
            var item = document.createElement('div');
            item.className = 'gmp-autocomplete-item';
            item.style.padding = '10px 14px';
            item.style.cursor = 'pointer';
            item.style.borderBottom = '1px solid #f0f0f0';
            item.style.fontSize = '0.92rem';
            item.style.color = '#1f2937';
            item.style.display = 'flex';
            item.style.alignItems = 'center';
            item.style.gap = '8px';

            item.innerHTML = '<span style="color:#d97706">📍</span> <span>' + escapeHTML(p.description) + '</span>';

            item.addEventListener('mouseenter', function () { item.style.backgroundColor = '#f8fafc'; });
            item.addEventListener('mouseleave', function () { item.style.backgroundColor = '#ffffff'; });

            item.addEventListener('click', function () {
              cityInput.value = p.description;
              dropdown.style.display = 'none';
              dropdown.innerHTML = '';
              cityInput.dispatchEvent(new Event('change', { bubbles: true }));
            });

            dropdown.appendChild(item);
          });

          dropdown.style.display = 'block';
        }

        // Hide dropdown on blur/click outside
        document.addEventListener('click', function (e) {
          if (!wrapper.contains(e.target)) {
            dropdown.style.display = 'none';
          }
        });

      } catch (err) {
        console.warn('Places library initialization notice:', err);
      }
    }).catch(function (err) {
      // Input continues as standard HTML text input without errors
      console.info('Maps Autocomplete fallback active.');
    });
  }

  function escapeHTML(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupCityAutocomplete);
  } else {
    setupCityAutocomplete();
  }
})();


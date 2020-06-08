if ('serviceWorker' in navigator) {
window.addEventListener('load', function() {
    navigator.serviceWorker.register('../sw.js').then(function(registration) {
      console.log('Service Worker ok', registration.scope);
    }, function(err) {
      console.log('ServiceWorker no ok ', err);
    });
  });
}
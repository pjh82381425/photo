window.addEventListener('load', () => {
  if (!document.body.classList.contains('loaded')) {
    document.body.classList.add('loaded');
  }
});

window.addEventListener('pageshow', (e) => {
  if (e.persisted) {
    document.body.classList.remove('fade-out'); 
    document.body.classList.add('loaded');      
  }
});
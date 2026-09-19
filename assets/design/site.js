const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#site-nav');
function closeMenu() {
  toggle.setAttribute('aria-expanded', 'false');
  nav.classList.remove('is-open');
}
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    toggle.focus();
  }
});
nav.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
window.matchMedia('(min-width: 1101px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});

// Keep the photos automatic, but always give visitors control over movement.
const carousel = document.querySelector('.photo-hero');
if (carousel) {
  const slides = [...carousel.querySelectorAll('.hero-slide')];
  const count = carousel.querySelector('.slide-count');
  const pauseButton = carousel.querySelector('.slide-pause');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let paused = motion.matches;
  let hovering = false;
  let focused = false;
  let timer;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.classList.toggle('is-active', i === current);
      slide.setAttribute('aria-hidden', String(i !== current));
    });
    count.textContent = `${current + 1} / ${slides.length}`;
  }
  function schedule() {
    window.clearInterval(timer);
    if (!paused && !hovering && !focused && !document.hidden) {
      timer = window.setInterval(() => show(current + 1), 6500);
    }
    pauseButton.textContent = paused ? 'Play' : 'Pause';
    pauseButton.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
  }
  carousel.querySelectorAll('[data-slide]').forEach(button => {
    button.addEventListener('click', () => {
      show(current + (button.dataset.slide === 'next' ? 1 : -1));
      schedule();
    });
  });
  pauseButton.addEventListener('click', () => { paused = !paused; schedule(); });
  carousel.addEventListener('mouseenter', () => { hovering = true; schedule(); });
  carousel.addEventListener('mouseleave', () => { hovering = false; schedule(); });
  carousel.addEventListener('focusin', () => { focused = true; schedule(); });
  carousel.addEventListener('focusout', event => {
    if (!carousel.contains(event.relatedTarget)) { focused = false; schedule(); }
  });
  document.addEventListener('visibilitychange', schedule);
  motion.addEventListener('change', () => { paused = motion.matches; schedule(); });
  schedule();
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const revealImages = [...document.querySelectorAll('.page-content img, .mission img, .season-section img, .impact-layout img')];
if (!reducedMotion.matches && 'IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        imageObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealImages.forEach(image => {
    image.classList.add('image-reveal');
    imageObserver.observe(image);
  });
  let revealFrame;
  function revealPassedImages() {
    window.cancelAnimationFrame(revealFrame);
    revealFrame = window.requestAnimationFrame(() => {
      revealImages.forEach(image => {
        if (!image.classList.contains('is-visible') && image.getBoundingClientRect().top < window.innerHeight) {
          image.classList.add('is-visible');
          imageObserver.unobserve(image);
        }
      });
    });
  }
  window.addEventListener('scroll', revealPassedImages, { passive: true });
  revealPassedImages();
}

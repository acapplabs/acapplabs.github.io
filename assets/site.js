// Shared by every page: footer year, top bar shading on scroll, mobile menu.
document.getElementById('y').textContent = new Date().getFullYear();
const bar = document.querySelector('.topbar');
const btn = document.querySelector('.menu-btn');
const menu = document.getElementById('menu');
const onScroll = () => bar.classList.toggle('scrolled', window.scrollY > 20);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();
btn.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  btn.setAttribute('aria-expanded', open);
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.classList.remove('open');
  btn.setAttribute('aria-expanded', false);
}));

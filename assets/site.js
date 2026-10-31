// Shared by every page: menus, footer year, carousels and the Wayfile showcase.
const y = document.getElementById('y');
if (y) y.textContent = new Date().getFullYear();

// Apps panel and the mobile menu.
const megaBtn = document.querySelector('[aria-controls="mega"]');
const mega = document.getElementById('mega');
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
function setMega(open) { megaBtn.setAttribute('aria-expanded', open); mega.classList.toggle('open', open); }
function closeMenu() { menu.classList.remove('open'); burger.setAttribute('aria-expanded', false); }
megaBtn.addEventListener('click', e => { e.stopPropagation(); setMega(!mega.classList.contains('open')); });
burger.addEventListener('click', e => {
  e.stopPropagation();
  const open = !menu.classList.contains('open');
  menu.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open);
});
document.addEventListener('click', e => {
  if (!mega.contains(e.target)) setMega(false);
  if (!menu.contains(e.target)) closeMenu();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') { setMega(false); closeMenu(); } });
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { setMega(false); closeMenu(); }));

// Carousel arrows scroll one card at a time.
document.querySelectorAll('[data-rail]').forEach(b => b.addEventListener('click', () => {
  const rail = document.getElementById(b.dataset.rail);
  const step = rail.firstElementChild.getBoundingClientRect().width + 20;
  rail.scrollBy({ left: step * Number(b.dataset.dir), behavior: 'smooth' });
}));

// Showcase: tabs and selectable numbers. Cycles until the visitor picks one.
const views = document.querySelectorAll('.view');
if (views.length) {
  let timer = null;
  const select = (view, i) => view.querySelectorAll('[data-i]').forEach(el => el.classList.toggle('on', el.dataset.i === String(i)));
  const current = () => [...views].find(v => !v.hidden);
  const stopCycle = () => { clearInterval(timer); timer = null; };
  views.forEach(view => view.querySelectorAll('[data-i]').forEach(el => {
    el.addEventListener('click', () => { stopCycle(); select(view, el.dataset.i); });
    el.addEventListener('mouseenter', () => { if (!timer) select(view, el.dataset.i); });
  }));
  document.querySelectorAll('.seg button').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('.seg button').forEach(t => t.setAttribute('aria-selected', t === tab));
    views.forEach(v => v.hidden = v.id !== tab.dataset.view);
    select(current(), 1);
  }));
  select(current(), 1);
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let i = 1;
    timer = setInterval(() => { i = i % 4 + 1; select(current(), i); }, 3500);
  }
}

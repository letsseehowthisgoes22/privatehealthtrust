'use strict';
document.querySelectorAll('[data-directory]').forEach(directory => {
  const form = directory.querySelector('form');
  const search = directory.querySelector('[data-search]');
  const state = directory.querySelector('[data-state-filter]');
  const focus = directory.querySelector('[data-focus-filter]');
  const cards = [...directory.querySelectorAll('[data-card]')];
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[’']/g, '');
  const filter = () => {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const text = normalize(card.textContent);
      const match = words.every(word => text.includes(word)) && (!state?.value || card.dataset.state === state.value) && (!focus?.value || card.dataset.focus === focus.value);
      card.hidden = !match;
      if (match) count++;
    });
    directory.querySelector('[data-count]').textContent = `${count} of ${cards.length} ${state ? 'programs' : 'providers'}`;
    directory.querySelector('[data-empty]').hidden = count !== 0;
  };
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', filter);
  form.addEventListener('change', filter);
  form.addEventListener('reset', () => { search.value = ''; if(state) state.value = ''; if(focus) focus.value = ''; filter(); });
  filter();
});
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => {
  const details = [...document.querySelectorAll('details')];
  const prior = details.map(item => item.open);
  details.forEach(item => item.open = true);
  window.addEventListener('afterprint', () => details.forEach((item, index) => item.open = prior[index]), { once: true });
  window.print();
}));

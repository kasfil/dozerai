function renderData(data) {
  const imgPill = el('article.no-padding#img-pill', [
    el('img.responsive.large', {
      src: image.path,
      id: image.id
    }),
    el('div.padding.img-data', [
      el('div.grid.no-space', [
        el('div.s6.grid-rating', [
          el('button.no-border.chip.img-rating', [
            el('i.fas.fa-star'),
            el('span', text(' ' + data.rating + ' / 10'))
          ])
        ]),
        el('div.s6.grid-timestamp', el('p', timestamp)),
      ]),
      el('div', [el('h5', 'Caption'), el('p.img-caption', data.caption)]),
      el('div.space'),
      el('div', [el('h5', 'Comment'), el('p.img-caption', data.comment)]),
      el('nav', el('button.responsive.small-round', text('Detail')))
    ])
  ]);
}

document.addEventListener('DOMContentLoaded', () => {
  const token = btoa(Telegram.WebApp.initData);
  fetch('/api/images/' + imgId, {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + token
    }
  }).then(response => response.json())
})

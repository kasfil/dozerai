const { router, mount, el, text, setChildren } = redom;

const token = btoa(Telegram.WebApp.initData);

var app = null;
var page = 1;
var limit = 5;


function emptyImg() {
  return el('article.no-border.no-padding.large.transparent.center-align.middle-align', el('div.padding', [
    el('h4', '🍃 No rated image yet.'),
    el('p', 'You can rate images with /rate command.')
  ]));
}

function pagination(totalImg, prevPage, nextPage) {
  var pages = [];
  if (prevPage) {
    pages.push(el('button.square.round', text(prevPage), { onclick: () => app.update('/', { page: prevPage, limit: limit }) }));
    if (prevPage >= 2) {
      pages.splice(0, 0, (el('button.square.round', el('i.fas.fa-angle-left'), { onclick: () => app.update('/', { page: 1, limit: limit }) })));
    }
  };

  pages.push(el('button.square.round.active', text(page)));

  if (nextPage) {
    pages.push(el('button.square.round', text(nextPage), { onclick: () => app.update('/', { page: nextPage, limit: limit }) }));
    if (nextPage < Math.ceil(totalImg / limit)) {
      pages.push(el('button.square.round', el('i.fas.fa-angle-right'), { onclick: () => app.update('/', { page: Math.ceil(totalImg / limit), limit: limit }) }));
    }
  };

  return el('div.pagination.nav.center-align', pages);
}

function renderImgs(imagesData) {
  const imgView = [];
  imagesData.forEach(image => {
    if (image.caption !== null && image.caption !== '') {
      var caption = text((image.caption.length > 60 ? image.caption.slice(0, 60) + '...' : image.caption).trim());
    } else {
      var caption = text('No caption...');
    }

    var created = Date.parse(image.created_at);
    var timestamp = text(new Date(created).toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric"
    }));

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
              el('span', text(' ' + image.rating + ' / 10'))
            ])
          ]),
          el('div.s6.grid-timestamp', el('p', timestamp)),
        ]),
        el('p.img-caption', caption),
        el('nav', el('button.responsive.small-round', text('Detail'), { onclick: () => showImage(image.id) }))
      ])
    ]);

    imgView.push(imgPill);
  });

  return imgView;
}

function renderData(data) {
  var created = Date.parse(data.created_at);
    var timestamp = text(new Date(created).toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric"
    }));

  const imgPill = el('article.no-padding#img-pill', [
    el('img.responsive.large', {
      src: data.path,
      id: data.id,
      style: { height: '100%' },
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
      el('div.space'),
      el('div', [el('h5', 'Caption'), el('p.img-caption', data.caption || 'No caption...')]),
      el('div.space'),
      el('div', [el('h5', 'Comment'), el('p.img-caption', data.comments)]),
      el('div.grid', [
        el('div.s12', el('button.responsive.small-round.destructive', text('Delete image'), {
          onclick: () => {
            Telegram.WebApp.showConfirm('Are you sure you want to delete this image?', (ok) => {
              if (!ok) {
                return;
              }

              fetch('/api/images/' + data.id, {
                method: 'DELETE',
                headers: {
                  'Authorization': 'Telegram-app ' + token
                }
              }).then(response => {
                if (response.ok) {
                  app.update('/', { page: page, limit: limit });
                } else {
                  Telegram.WebApp.showAlert('Failed to delete image');
                }
              })
            })
          }
        })),
      ])
    ])
  ]);

  return imgPill;
}

class Dashboard {
  update(data) {

    if (data.page) {
      page = data.page;
    }

    if (data.limit) {
      limit = data.limit;
    }


    fetch(`/api/images?page=${page}&limit=${limit}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Telegram-app ' + token
      }
    }).then(response => {
      if (response.ok && response.headers.get('Content-Type') === 'application/json') {
        response.json().then(data => {
          const mainView = document.getElementById('main-view');
          if (data.total_img === 0) {
            mount(mainView, emptyImg());
          } else {
            const imgView = renderImgs(data.imgs);
            const viewWrapper = el('div#view-wrapper', imgView);
            const space = mainView.appendChild(el('div.space'));
            const pageInfo = el('p.center-align', text(`Page ${page} of ${Math.ceil(data.total_img / limit)} (${Math.ceil(data.total_img / limit)} pages for ${data.total_img} images)`));
            const paginationView = pagination(data.total_img, data.prev_page, data.next_page);
            setChildren(mainView, [viewWrapper, space, pageInfo, paginationView]);
          }
        })
      }
    })
  }
}

class ImageDetail {

  update(data) {
    const mainView = document.getElementById('main-view');
    fetch(`/api/images/${data.id}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Telegram-app ' + token
      }
    }).then(response => {
      if (response.ok && response.headers.get('Content-Type') === 'application/json') {
        response.json().then(data => {
          const imgPill = renderData(data);
          mount(mainView, imgPill);
        })
      }
    })
  }
}

document.addEventListener('DOMContentLoaded', () => {
  app = router(document.getElementById('main-view'), {
    '/': Dashboard,
    '/detail': ImageDetail
  });
  app.update('/', {});
})

Telegram.WebApp.BackButton.onClick(() => {
  Telegram.WebApp.BackButton.hide();
  app.update('/', { page: page, limit: limit });
})

function showImage(imgId) {
  Telegram.WebApp.BackButton.show();
  app.update('/detail', { id: imgId });
}

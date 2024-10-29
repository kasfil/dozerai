const {
  el,
  text,
  mount,
  setChildren,
  list,
  setAttr
} = redom;

const user = Telegram.WebApp.initDataUnsafe.user
const urlParams = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
})

const currentPage = urlParams.page || 1;
const limit = urlParams.limit || 10;

class EmptyImages {
  constructor() {
    this.noImg = el('article.no-border.no-padding.large.transparent.center-align.middle-align', el('div.padding', [
      el('h4', '🍃 No rated image yet.'),
      el('p', 'You can rate images with /rate command.')
    ]));

    return this.noImg;
  }
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
        el('nav', el('a.button.responsive.small-round', text('Detail'), { href: `/image/${image.id}` }))
      ])
    ]);

    imgView.push(imgPill);
  });

  return imgView;
}


document.addEventListener('DOMContentLoaded', () => {
  const token = btoa(Telegram.WebApp.initData);
  fetch('/api/images', {
      method: 'GET',
      headers: {
        Authorization: `Telegram-app ${token}`,
      },
    })
    .then(response => response.json())
    .then(data => {
      const mainView = document.getElementById('main-view');

      if (data.total_img === 0) {
        const view = new EmptyImages();
        mount(mainView, view);
      } else {
        const views = renderImgs(data.imgs);
        views.forEach(view => {
          mainView.appendChild(view);
        })
      }

    });
})

document.addEventListener('DOMContentLoaded', () => {
  const userProfileImage = document.getElementById('user-profile');
  if (user.photo_url) {
    userProfileImage.src = user.photo_url;
  }
});

Telegram.WebApp.ready();

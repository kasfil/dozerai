const { el, text, mount, setChildren, list, setAttr } = redom;

class ListImages {
    constructor() {
        // this.navBtn = el('button.responsive.small-round')
        // this.nav = el('nav')
        // this.imgCaption = el('p.img-caption')
        this.timestamp = el('p')
        // this.gridTimestamp = el('div.s6.grid-timestamp')
        // this.imgRating = el('span')
        // this.starIcon = el('i.fas.fa-star')
        // this.chip = el('button.no-border.chip.img-rating')
        // this.gridRating = el('div.s6.grid-rating')
        // this.grid = el('div.grid.no-space')
        // this.imgData = el('div.padding.img-data')
        // this.img = el('img.responsive.large')
        // this.article = el('article.no-padding#img-pill')

        // setChildren(this.nav, [this.navBtn])
        // setChildren(this.gridTimestamp, [this.timestamp])
        // setChildren(this.chip, [this.starIcon, this.imgRating])
        // setChildren(this.gridRating, [this.chip])
        // setChildren(this.grid, [this.gridRating, this.gridTimestamp])
        // setChildren(this.imgData, [this.grid, this.imgCaption, this.nav])
        // setChildren(this.article, [this.img, this.imgData])
    }

    update(data) {
        // this.imgRating.textContent = ` ${data.rating} / 10`
        
        var created = Date.parse(data.created_at);
        this.timestamp.textContent = new Date(created).toLocaleDateString("en-US", {
            weekday: "short",
            month: "short",
            day: "numeric",
            year: "numeric"
        });
        
        // if (data.caption !== null || data.caption !== '') {
        //     this.imgCaption.textContent = (data.caption.length > 60 ? data.caption.slice(0, 60) + '...' : data.caption).trim();
        // } else {
        //     this.imgCaption.textContent = 'No caption...'
        // }
        
        // setAttr(this.img, 'src', data.path)
    }
}

class EmptyImages {
    constructor() {
        this.noImg = el('article.no-border.no-padding.large.transparent.center-align.middle-align', el('div.padding', [
            el('h4', '🍃 No rated image yet.'),
            el('p', 'You can rate images with /rate command.')
        ]));

        return this.noImg;
    }
}

// function showImages(imagesData) {
//     const mainView = document.getElementById('main-view');
//     if (imagesData.length === 0) {
//         const emptyText = el('article.no-border.no-padding.large.center-align.middle-align', el('div.padding', [
//             el('h4', '🍃 No rated image yet.'),
//             el('p', 'You can rate images with /rate command.')
//         ]));
//         mount(mainView, emptyText);
//         return;
//     }

//     imagesData.forEach(image => {
//         if (image.caption !== null && image.caption !== '') {
//             var caption = text((image.caption.length > 60 ? image.caption.slice(0, 60) + '...' : image.caption).trim());
//         } else {
//             var caption = text('No caption...');
//         }

//         var created = Date.parse(image.created_at);
//         var timestamp = text(new Date(created).toLocaleDateString("en-US", {
//             weekday: "short",
//             month: "short",
//             day: "numeric",
//             year: "numeric"
//         }));

//         const imgPill = el('article.no-padding#img-pill', [
//             el('img.responsive.large', {
//                 src: image.path,
//                 id: image.id
//             }),
//             el('div.padding.img-data', [
//                 el('div.grid.no-space', [
//                     el('div.s6.grid-rating', [
//                         el('button.no-border.chip.img-rating', [
//                             el('i.fas.fa-star'),
//                             el('span', text(' ' + image.rating + ' / 10'))
//                         ])
//                     ]),
//                     el('div.s6.grid-timestamp', el('p', timestamp)),
//                 ]),
//                 el('p.img-caption', caption),
//                 el('nav', el('button.responsive.small-round', text('Detail')))
//             ])
//         ]);
//         mainView.append(imgPill);
//     });

// }

function showImgs(data) {
    console.log(data)
    console.log('function called')
    const mainView = document.getElementById('main-view');
    if (data.total_img === 0) {
        mount(mainView, new EmptyImages());
    } else {
        const imgView = list('div', ListImages, 'id');
        mount(mainView, imgView);
        imgView.update(data.imgs);
    }
}

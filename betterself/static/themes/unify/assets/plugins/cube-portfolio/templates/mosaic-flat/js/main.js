(function($, window, document, undefined) {
    'use strict';

    // init cubeportfolio
    $('#js-grid-mosaic-flat').cubeportfolio({
        filters: '#js-filters-mosaic-flat',
        loadMore: '#js-loadMore-mosaic-flat',
        loadMoreAction: 'click',
        layoutMode: 'mosaic',
        sortToPreventGaps: true,
        mediaQueries: [{
            width: 1500,
            cols: 6
        }, {
            width: 1100,
            cols: 4
        }, {
            width: 800,
            cols: 3
        }, {
            width: 480,
            cols: 2
        }, {
            width: 320,
            cols: 1
        }],
        defaultFilter: '*',
        animationType: 'fadeOutTop',
        gapHorizontal: 0,
        gapVertical: 0,
        gridAdjustment: 'responsive',
        caption: 'fadeIn',
        displayType: 'fadeIn',
        displayTypeSpeed: 100,

        // lightbox
        lightboxDelegate: '.cbp-lightbox',
        lightboxGallery: true,
        lightboxTitleSrc: 'data-title',
        lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>',
    });
})(jQuery, window, document);

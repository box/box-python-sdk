$(function() {
    $('a.page-scroll').bind('click', function(event) {
        event.preventDefault();
        var anchor = $(this);
        $('body,html').stop().animate(
            {
                scrollTop: $(anchor.attr('href')).offset().top
            },
            1500,
            'easeInOutExpo'
        );
    });
});
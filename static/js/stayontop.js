   // Cache selectors outside callback for performance. 
   var $window = $(window),
       $stickyEl = $('#mainLogo'),
       elTop = $stickyEl.offset().top;

   $window.scroll(function() {
        $stickyEl.toggleClass('sticky', $window.scrollTop() > elTop);
    });

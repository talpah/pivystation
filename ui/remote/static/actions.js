var smActions = (function ($) {
    var actionlist = {};

    actionlist.initConfirmationButtons = function () {
        $(document).on('click', 'button[data-confirm]', function (e) {
            e.preventDefault();
            var $this = $(this);
            bootbox.confirm($this.data('confirm'), function (result) {
                if (result) {
                    if ($this.data('href')) {
                        window.location.href = $this.data('href');
                    }
                }
            });

        })
    };

    return actionlist;

})(jQuery);

(function ($) {
    $(document).ready(function () {
        smActions.initConfirmationButtons();
    });
})(jQuery);

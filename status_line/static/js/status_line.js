$(function() {
    function StatusLineViewModel(parameters) {
        var self = this;

        self.status_lcd = ko.observable();
        self.status_fan = ko.observable();
        self.show_status = ko.observable(false);

        self.initialMessage = function(data) {
            self.status_lcd(data.status_lcd);
            self.status_fan(data.status_fan);
            self.show_status(data.status_lcd ? true : data.status_fan ? true : false);
        };

        self.onStartupComplete = function() {
            // WebApp started, get message if any
            $.ajax({
                url: API_BASEURL + "plugin/status_line",
                type: "GET",
                dataType: "json",
                success: self.initialMessage
            });
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "status_line") {
                return;
            }

            self.status_lcd(data.status_lcd);
            self.status_fan(data.status_fan);
            self.show_status(true);
        };
    }

    OCTOPRINT_VIEWMODELS.push([
        StatusLineViewModel,
        [ ],
        ["#status_line"]
    ]);
})

var gvis = gvis || {};

gvis.GVis = function(element) {
    this.element = element;
    this.element.innerHTML = "<div id='map-canvas' style='height:300px; width:300px;'></div>";

    var me = this;

    $(function() {
        window.initialize = function() {
            var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
            var mapOptions = {
                zoom : 4,
                center : myLatlng,
                mapTypeId : google.maps.MapTypeId.ROADMAP
            };

            var map = new google.maps.Map(
                document.getElementById('map-canvas'), mapOptions);

            var marker = new google.maps.Marker({
                position: myLatlng,
                map: map,
                title: 'Hello World!'
            });

            // Getter and setter for the value property
            me.getValue = function () {
                console.log('getValue ->', marker);
                return marker.getTitle();
            };
            me.setValue = function (value) {
                console.log('setValue ->', value);
                marker.setTitle(value);
                console.log('setted value ->', marker);
            };

            google.maps.event.addListener(map, 'click', function() {
                me.click();
            });
        };

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&'
            + 'callback=initialize';
        document.body.appendChild(script);
        console.log("testing");
    });
};
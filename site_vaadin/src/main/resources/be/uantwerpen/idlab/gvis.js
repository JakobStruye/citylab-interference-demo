var gvis = gvis || {};

gvis.GVis = function(element) {
    this.element = element;
    this.element.innerHTML = "<div id='chart_div' style='height:500px; width:500px;'></div>";

    var oldDocumentWrite = document.write;

    // change document.write temporary
    document.write = function(node) {
        $("body").append(node);
    };

    $(function() {
        window.initialize = function() {

            google.setOnLoadCallback(drawVisualization);

            setTimeout(function() {
                document.write = oldDocumentWrite;
            }, 100);

            function drawVisualization() {

                // Create and populate the data table.
                var data = google.visualization.arrayToDataTable([
                    [ 'Year', 'Austria', 'Bulgaria', 'Denmark', 'Greece' ],
                    [ '2003', 1336060, 400361, 1001582, 997974 ],
                    [ '2004', 1538156, 366849, 1119450, 941795 ],
                    [ '2005', 1576579, 440514, 993360, 930593 ],
                    [ '2006', 1600652, 434552, 1004163, 897127 ],
                    [ '2007', 1968113, 393032, 979198, 1080887 ],
                    [ '2008', 1901067, 517206, 916965, 1056036 ] ]);

                // Create and draw the visualization.
                new google.visualization.BarChart(document
                    .getElementById("chart_div")).draw(data, {
                    title : "Yearly Coffee Consumption by Country",
                    width : 100,
                    height : 100,
                    vAxis : {
                        title : "Year"
                    },
                    hAxis : {
                        title : "Cups"
                    }
                });
            }
        };

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://www.google.com/jsapi?autoload=%7B%22modules%22%3A%5B%7B%22name%22%3A%22visualization%22%2C%22version%22%3A%221%22%2C%22packages%22%3A%5B%22corechart%22%2C%22table%22%5D%7D%5D%7D&'
            + 'callback=initialize';
        document.body.appendChild(script);
    });
};
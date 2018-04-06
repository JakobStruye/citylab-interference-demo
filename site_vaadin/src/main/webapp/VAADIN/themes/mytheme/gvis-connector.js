window.be_uantwerpen_idlab_GVis =
    function() {
        // Create the component
        var gVis = new gvis.GVis(this.getElement());

        // Handle changes from the server-side
        this.onStateChange = function() {
            console.log('state change ->', this.getState().value);
            gVis.setValue(this.getState().value);
        };

        // Pass user interaction to the server-side
        var connector = this;
        gVis.click = function() {
            connector.onClick(gVis.getValue());
        };
    };
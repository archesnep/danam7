define([
    'jquery',
    'knockout',
    'viewmodels/widget',
    'arches',
    'bindings/select2-query'
], function($, ko, WidgetViewModel, arches) {
    return ko.components.register('geocoder', {
        viewModel: function(params) {
            var self = this;
            var url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/';

            this.select2Config = {
                value: this.address,
                placeholder: this.placeholder,
                minimumInputLength: 3,
                query: function(query) {
                    $.getJSON(url + query.term + '.json', {
                        access_token: arches.mapboxApiKey,
                        types: 'address',
                        limit: 10
                    }, function(data) {
                        query.callback({
                            results: data.features.map(function(feature) {
                                return {
                                    id: feature['place_name'],
                                    text: feature['place_name'],
                                    x: feature['center'][0],
                                    y: feature['center'][1]
                                }
                            })
                        });
                    });
                },
                initSelection: function(element, callback) {
                    var address = self.address();
                    callback({
                        id: address,
                        text: address,
                        x: self.x(),
                        y: self.y()
                    });
                },
                onSelect: function(selection) {
                    self.x(selection.x);
                    self.y(selection.y);
                },
                onClear: function() {
                    self.x(null);
                    self.y(null);
                }
            };

            this.displayValue = ko.computed(function() {
                return self.address();
            });
        },
        template: {
            require: ''
        }
    });
});
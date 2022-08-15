define([
    'knockout',
    'knockout-mapping',
    'underscore',
    'mapbox-gl',
    'geojson-extent',
    'viewmodels/card-component',
    'bindings/mapbox-gl'
], function(ko, koMapping, _, mapboxgl, geojsonExtent, CardComponentViewModel) {
    return ko.components.register('address-card', {
        viewModel: function(params) {
            var self = this;
            params.configKeys = ['icon'];

            CardComponentViewModel.apply(this, [params]);

            this.geoJSON = ko.computed(function() {
                var geoJSON = {
                    'type': 'FeatureCollection',
                    'features': []
                };
                return geoJSON;
            });

            this.setupMap = function(map) {
                map.on('load', function() {
                    var geoJSON = self.geoJSON();
                    var zoomToGeoJSON = function(geoJSON) {
                        if (geoJSON.features.length > 0) {
                            map.fitBounds(geojsonExtent(geoJSON), {
                                padding: 100,
                                maxZoom: 15
                            });
                        }
                    };

                    map.addSource('address-points', {
                        'type': 'geojson',
                        'data': geoJSON
                    });
                    map.addLayer({
                        'id': 'address-points',
                        'source': 'address-points',
                        'type': 'symbol',
                        'layout': {
                            'icon-image': self.icon(),
                            'text-field': '{address}',
                            'text-offset': [0, 0.6],
                            'text-anchor': 'top'
                        }
                    });
                    zoomToGeoJSON(geoJSON);

                    self.geoJSON.subscribe(function(geoJSON) {
                        map.getSource('address-points').setData(geoJSON);
                        zoomToGeoJSON(geoJSON);
                    });

                    self.icon.subscribe(function(icon) {
                        map.setLayoutProperty('address-points', 'icon-image', icon);
                    });
                });
            };
        },
        template: {
            require: 'text!templates/views/components/card_components/address-card.htm'
        }
    });
});
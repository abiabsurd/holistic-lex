const chart = c3.generate({
    bindto: '#chart',
    data: {
//        x: 'dates',
        xs: xs,
        columns: columns
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                fit: true,
                format: '%Y-%m-%d'
            }
        }
    }
});

// show only the first metric on load
chart.hide();
chart.show(showOnLoad);

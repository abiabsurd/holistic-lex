const chart = c3.generate({
    bindto: '#chart',
    data: {
        x: 'dates',
        columns: data
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

chart.hide();
chart.show(data[1][0]);

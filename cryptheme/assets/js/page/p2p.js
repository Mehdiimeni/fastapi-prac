/*
* Admin Layout (cryptoon)
* @author: Crypto Ex
* @design by: Crypto Ex.
* @event-namespace:cryptoon
* Copyright 2021 Crypto Ex
*/

if (typeof jQuery === "undefined") {
    throw new Error("jQuery plugins need to be before this file");
}
$(function () {
    "use strict";
    // project data table
    $(document).ready(function () {
        $('#p2pone')
            .addClass('nowrap')
            .dataTable({
                responsive: true,
                columnDefs: [
                    { targets: [-1, -3], className: 'dt-body-right' }
                ]
            });
        $('#p2ptwo')
            .addClass('nowrap')
            .dataTable({
                responsive: true,
                columnDefs: [
                    { targets: [-1, -3], className: 'dt-body-right' }
                ]
            });
        $('#p2pthree')
            .addClass('nowrap')
            .dataTable({
                responsive: true,
                columnDefs: [
                    { targets: [-1, -3], className: 'dt-body-right' }
                ]
            });
        $('#p2pfour')
            .addClass('nowrap')
            .dataTable({
                responsive: true,
                columnDefs: [
                    { targets: [-1, -3], className: 'dt-body-right' }
                ]
            });

        $('#p2pone', '#p2ptwo', '#p2pthree', '#p2pfour').DataTable({
            responsive: true
        });

        $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
            $($.fn.dataTable.tables(true)).DataTable()
                .columns.adjust()
                .responsive.recalc();
        });
    });

});



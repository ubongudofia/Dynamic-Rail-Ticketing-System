
// const socket = io.connect('http://127.0.0.1:5009');

// Initialize charts for two different divs
// let chart1 = new ApexCharts(document.querySelector("#line-chart-1"), {
//     chart: {
//         type: 'line',
//         height: 350
//     },
//     series: [{
//         name: 'Users Registered',
//         data: []  // Initially empty; will be populated by WebSocket events
//     }],
//     xaxis: {
//         type: 'datetime'
//     }
// });

// let chart2 = new ApexCharts(document.querySelector("#line-chart-2"), {
//     chart: {
//         type: 'line',
//         height: 350
//     },
//     series: [{
//         name: 'Payments and Tickets',
//         data: []  // Initially empty; will be populated by WebSocket events
//     }],
//     xaxis: {
//         type: 'datetime'
//     }
// });

// chart1.render();  // Render first chart
// chart2.render();  // Render second chart

// // Listen for the 'user_registered' event and update chart
// socket.on('user_registered', (data) => {
//     console.log('New user registered:', data);
//     // Update the chart with the new data
//     updateChart(chart1, data);
// });

// // Function to update the chart with new data
// function updateChart(chart, data) {
//     const now = new Date().getTime();
//     chart.updateSeries([{
//         data: [...chart.w.globals.series[0], { x: now, y: chart.w.globals.series[0].length + 1 }]
//     }]);
// }



// socket.on('user_registered', (data) => {
//     console.log('New user registered:', data);
//     updateChart(chart1, data);
// });

// socket.on('payment_ticket_update', (data) => {
//     console.log('Payment or ticket update:', data);
//     updateChart(chart2, data);
// });





//---------- CHARTS ----------

// BAR CHART
// const barChartOptions = {
//     series: [
//         {
//             data: [10, 8, 6, 4, 2],
//         },
//     ],
//     chart: {
//         type: 'bar',
//         height: 350,
//         toolbar: {
//             show: false,
//         },
//     },
//     colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f', '#4f35a1'],
//     plotOptions: {
//         bar: {
//             distributed: true,
//             borderRadius: 4,
//             horizontal: false,
//             columnWidth: '40%',
//         },
//     },
//     dataLabels: {
//         enabled: false,
//     },
//     legend: {
//         show: false,
//     },
//     xaxis: {
//         categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
//     },
//     yaxis: {
//         title: {
//             text: 'Count',
//         },
//     },
// };

// const barChart = new ApexCharts(
//     document.querySelector('#line-chart-1'),
//     barChartOptions
// );
// barChart.render();

// // AREA CHART
// const areaChartOptions = {
//     series: [
//         {
//             name: 'Purchase Orders',
//             data: [31, 40, 28, 51, 42, 109, 100],
//         },
//         {
//             name: 'Sales Orders',
//             data: [11, 32, 45, 32, 34, 52, 41],
//         },
//     ],
//     chart: {
//         height: 350,
//         type: 'area',
//         toolbar: {
//             show: false,
//         },
//     },
//     colors: ['#4f35a1', '#246dec'],
//     dataLabels: {
//         enabled: false,
//     },
//     stroke: {
//         curve: 'smooth',
//     },
//     labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
//     markers: {
//         size: 0,
//     },
//     yaxis: [
//         {
//             title: {
//                 text: 'Purchase Orders',
//             },
//         },
//         {
//             opposite: true,
//             title: {
//                 text: 'Sales Orders',
//             },
//         },
//     ],
//     tooltip: {
//         shared: true,
//         intersect: false,
//     },
// };

// const areaChart = new ApexCharts(
//     document.querySelector('#line-chart-2'),
//     areaChartOptions
// );
// areaChart.render();






// ADMIN DASHBOARD JS START HERE

// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add('sidebar-responsive');
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove('sidebar-responsive');
        sidebarOpen = false;
    }
}




// USERS TABLE JS

const search = document.querySelector('.input-group input'),
    table_rows = document.querySelectorAll('tbody tr'),
    table_headings = document.querySelectorAll('thead th');

// 1. Searching for specific data of HTML table
search.addEventListener('input', searchTable);

function searchTable() {
    table_rows.forEach((row, i) => {
        let table_data = row.textContent.toLowerCase(),
            search_data = search.value.toLowerCase();

        row.classList.toggle('hide', table_data.indexOf(search_data) < 0);
        row.style.setProperty('--delay', i / 25 + 's');
    })

    document.querySelectorAll('tbody tr:not(.hide)').forEach((visible_row, i) => {
        visible_row.style.backgroundColor = (i % 2 == 0) ? 'transparent' : '#0000000b';
    });
}

// 2. Sorting | Ordering data of HTML table

table_headings.forEach((head, i) => {
    let sort_asc = true;
    head.onclick = () => {
        table_headings.forEach(head => head.classList.remove('active'));
        head.classList.add('active');

        document.querySelectorAll('td').forEach(td => td.classList.remove('active'));
        table_rows.forEach(row => {
            row.querySelectorAll('td')[i].classList.add('active');
        })

        head.classList.toggle('asc', sort_asc);
        sort_asc = head.classList.contains('asc') ? false : true;

        sortTable(i, sort_asc);
    }
})


function sortTable(column, sort_asc) {
    [...table_rows].sort((a, b) => {
        let first_row = a.querySelectorAll('td')[column].textContent.toLowerCase(),
            second_row = b.querySelectorAll('td')[column].textContent.toLowerCase();

        return sort_asc ? (first_row < second_row ? 1 : -1) : (first_row < second_row ? -1 : 1);
    })
        .map(sorted_row => document.querySelector('tbody').appendChild(sorted_row));
}

// 3. Converting HTML table to PDF

const pdf_btn = document.querySelector('#toPDF');
const customers_table = document.querySelector('#customers_table');


const toPDF = function (customers_table) {
    const html_code = `
    <!DOCTYPE html>
    <link rel="stylesheet" type="text/css" href="style.css">
    <main class="table" id="customers_table">${customers_table.innerHTML}</main>`;

    const new_window = window.open();
    new_window.document.write(html_code);

    setTimeout(() => {
        new_window.print();
        new_window.close();
    }, 400);
}

pdf_btn.onclick = () => {
    toPDF(customers_table);
}

// 4. Converting HTML table to JSON

const json_btn = document.querySelector('#toJSON');

const toJSON = function (table) {
    let table_data = [],
        t_head = [],

        t_headings = table.querySelectorAll('th'),
        t_rows = table.querySelectorAll('tbody tr');

    for (let t_heading of t_headings) {
        let actual_head = t_heading.textContent.trim().split(' ');

        t_head.push(actual_head.splice(0, actual_head.length - 1).join(' ').toLowerCase());
    }

    t_rows.forEach(row => {
        const row_object = {},
            t_cells = row.querySelectorAll('td');

        t_cells.forEach((t_cell, cell_index) => {
            const img = t_cell.querySelector('img');
            if (img) {
                row_object['customer image'] = decodeURIComponent(img.src);
            }
            row_object[t_head[cell_index]] = t_cell.textContent.trim();
        })
        table_data.push(row_object);
    })

    return JSON.stringify(table_data, null, 4);
}

json_btn.onclick = () => {
    const json = toJSON(customers_table);
    downloadFile(json, 'json')
}

// 5. Converting HTML table to CSV File

const csv_btn = document.querySelector('#toCSV');

const toCSV = function (table) {
    // Code For SIMPLE TABLE
    // const t_rows = table.querySelectorAll('tr');
    // return [...t_rows].map(row => {
    //     const cells = row.querySelectorAll('th, td');
    //     return [...cells].map(cell => cell.textContent.trim()).join(',');
    // }).join('\n');

    const t_heads = table.querySelectorAll('th'),
        tbody_rows = table.querySelectorAll('tbody tr');

    const headings = [...t_heads].map(head => {
        let actual_head = head.textContent.trim().split(' ');
        return actual_head.splice(0, actual_head.length - 1).join(' ').toLowerCase();
    }).join(',') + ',' + 'image name';

    const table_data = [...tbody_rows].map(row => {
        const cells = row.querySelectorAll('td'),
            img = decodeURIComponent(row.querySelector('img').src),
            data_without_img = [...cells].map(cell => cell.textContent.replace(/,/g, ".").trim()).join(',');

        return data_without_img + ',' + img;
    }).join('\n');

    return headings + '\n' + table_data;
}

csv_btn.onclick = () => {
    const csv = toCSV(customers_table);
    downloadFile(csv, 'csv', 'customer orders');
}

// 6. Converting HTML table to EXCEL File

const excel_btn = document.querySelector('#toEXCEL');

const toExcel = function (table) {
    // Code For SIMPLE TABLE
    // const t_rows = table.querySelectorAll('tr');
    // return [...t_rows].map(row => {
    //     const cells = row.querySelectorAll('th, td');
    //     return [...cells].map(cell => cell.textContent.trim()).join('\t');
    // }).join('\n');

    const t_heads = table.querySelectorAll('th'),
        tbody_rows = table.querySelectorAll('tbody tr');

    const headings = [...t_heads].map(head => {
        let actual_head = head.textContent.trim().split(' ');
        return actual_head.splice(0, actual_head.length - 1).join(' ').toLowerCase();
    }).join('\t') + '\t' + 'image name';

    const table_data = [...tbody_rows].map(row => {
        const cells = row.querySelectorAll('td'),
            img = decodeURIComponent(row.querySelector('img').src),
            data_without_img = [...cells].map(cell => cell.textContent.trim()).join('\t');

        return data_without_img + '\t' + img;
    }).join('\n');

    return headings + '\n' + table_data;
}

excel_btn.onclick = () => {
    const excel = toExcel(customers_table);
    downloadFile(excel, 'excel');
}

const downloadFile = function (data, fileType, fileName = '') {
    const a = document.createElement('a');
    a.download = fileName;
    const mime_types = {
        'json': 'application/json',
        'csv': 'text/csv',
        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    a.href = `
        data:${mime_types[fileType]};charset=utf-8,${encodeURIComponent(data)}
    `;
    document.body.appendChild(a);
    a.click();
    a.remove();
}


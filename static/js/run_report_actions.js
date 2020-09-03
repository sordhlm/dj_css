$(document).ready(function() {
    id_progress_step = document.getElementById("id_progress_step");
    if(id_progress_step){
        $("#id_progress_step").val(1)
    }
    var step = $("#id_progress_step").val();
    console.debug("summary", summary)
    console.debug("data_trend", data_trend)
    canvas = document.getElementById("pieContainer");
    if(canvas){
        gen_progress_pie(summary);
    }
    canvas = document.getElementById("spendContainer");
    if(canvas){
        gen_spend_pie(spends);
    }
    canvas = document.getElementById("chartContainer");
    if(canvas){
       gen_progress_trend(data_trend);
    }
    var option = {
      responsive: false,
      title: {
          display: true,
          text: 'Progress Rate Trend'
      }
    };


    $('#id_progress_step').change(function() {
        step = $(this).val();
        if (step) {
            console.debug(step)
            update_progress_trend(step)
        }
    });
    $('#id_table_report').on('click', 'tr', function () {
        var tr = $(this).closest('tr');
        var siteTable = $('#id_table_report').DataTable()
        var row = siteTable.row( tr );
        console.log("ParentTable click", row.data()[0])
        console.debug(siteTable)
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else{
            siteTable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            get_contact_trend(row.data()[0], step)
        }
        
        //var td = ($(this).closest('td'))
        //if ( row.child.isShown() ) {
        //    // This row is already open - close it
        //    destroyChild(row);
        //    tr.removeClass('shown');
        //}
        //else {
        //    // Open this row
        //    createChild(row, gen_detail_table); // class is for background colour
        //    tr.addClass('shown');
        //}
    } ); 

});

function update_progress_trend(step){
  //console.debug(product_id)
  //displayLoadingDiv();
  jQuery.ajax({
    'url': '/report/update_progress_trend/',
    'type': 'POST',
    'data': {'step': step },
    'success': function (data, textStatus, jqXHR) {
      console.debug(data.result)
      gen_progress_trend(data.result);
    },
    'error': function (jqXHR, textStatus, errorThrown) {
      alert("update_progress_trend fail");
    }
  });
}

function get_contact_trend(id, step){
  jQuery.ajax({
    'url': '/report/get_contact_trend/',
    'type': 'POST',
    'data': {'id': id, 'step':step},
    'success': function (data, textStatus, jqXHR) {
      console.debug(data.result)
      gen_contact_trend(data.result, "contact_chart");
    },
    'error': function (jqXHR, textStatus, errorThrown) {
      alert("update_progress_trend fail");
    }
  });
}

function gen_progress_pie(data){
    var pie_data = [];
    pie_data.push({y: data.paid, label: 'Paid'})
    pie_data.push({y: data.remain, label: 'Remain'})
    //color = ['rgb(92, 184, 92)','rgb(217,83,79)'];//,'rgb(240,173,78)','rgb(91,192,222)','rgb(191,191,191)'];
    //labels = ['Paid','Remain'];
    gen_pie_chart(pie_data, 'Sales', "pieContainer");    
}

function gen_spend_pie(data){
    var pie_data = [];
    console.debug('gen_spend_pie',data)
    if(data.length){
        for(var i = 0;i < data.length;i++){
            if(data[i].total != 0){
                pie_data.push({y: data[i].total, label: data[i].name})    
            }
        }
        gen_pie_chart(pie_data, 'Spend', "spendContainer");
    }
        
}

function gen_pie_chart(data, name, container){
    console.debug("gen_pie", data)
    var chart1 = new CanvasJS.Chart(container, {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        //exportEnabled: true,
        animationEnabled: true,
        title: {
            text: name
        },
        data: [{
            type: "pie",
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 15,
            indexLabel: "{label} - {y}",
            dataPoints: data
        }]
    });
    chart1.render();  
}
function gen_contact_trend(data, container){
    var total_data = [];
    var paid_data = [];
    console.debug(data)
    if(data.length){
        for(var i = 0;i < data.length;i++){
            date = new Date(data[i].date)
            element = {};
            element.x = date;
            element.y = data[i].total;
            total_data.push(element);
            element = {};
            element.x = date;
            element.y = data[i].paid;
            paid_data.push(element);      
        }
        console.debug(total_data)
        console.debug(paid_data)
        //console.debug(running_data)
        var chart = new CanvasJS.Chart(container, {
            animationEnabled: true,
            zoomEnabled: true,
            //theme: "dark2",
            title: {
                text: "Contact Contribution"
            },
            axisX: {
                title: "Day",
                labelFormatter: function(e){
                    return CanvasJS.formatDate( e.value, "DD MMM");
                }
            },
            axisY: {
                //logarithmic: true, //change it to false
                title: "Total",
                titleFontColor: "#6D78AD",
                lineColor: "#6D78AD",
                gridThickness: 1,
                lineThickness: 1,
                //scaleBreaks: {
                //    autoCalculate: true
                //}
                //labelFormatter: addSymbols
            },
            legend: {
                verticalAlign: "top",
                fontSize: 16,
                dockInsidePlotArea: true
            },
            data: [{
                type: "line",
                //xValueFormatString: "####",
                showInLegend: true,
                name: "Total",
                dataPoints: total_data
            },
            {
                type: "line",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Paid",
                dataPoints: paid_data
            },
            ]
        });
        chart.render();
    }
}
function gen_progress_trend(data){
    var total_data = [];
    var paid_data = [];
    var spend_data = [];
    var profit_data = [];
    var total_sum_data = [];
    var profit_sum_data = [];
    var spend_sum_data = [];
    var total = 0;
    var profit = 0;
    var spend = 0;
    console.debug(data)
    if(data.length){
        for(var i = 0;i < data.length;i++){
            date = new Date(data[i].date)
            element = {};
            element.x = date;
            element.y = data[i].total;
            total_data.push(element);
            element = {};
            element.x = date;
            element.y = data[i].paid;
            paid_data.push(element);    
            element = {};
            element.x = date;
            element.y = data[i].spend;
            spend_data.push(element);  
            element = {};
            element.x = date;
            element.y = data[i].profit;
            profit_data.push(element); 
            total = total +  data[i].total;
            profit = profit +  data[i].profit
            spend = spend +  data[i].freight;
            element = {};
            element.x = date;
            element.y = total;
            total_sum_data.push(element);   
            element = {};
            element.x = date;
            element.y = profit;
            profit_sum_data.push(element);  
            element = {};
            element.x = date;
            element.y = spend;
            spend_sum_data.push(element); 
        }
        console.debug(total_data)
        console.debug(paid_data)
        //console.debug(running_data)
        var chart = new CanvasJS.Chart("chartContainer", {
            animationEnabled: true,
            zoomEnabled: true,
            //theme: "dark2",
            title: {
                text: "Period Detail"
            },
            axisX: {
                title: "Day",
                labelFormatter: function(e){
                    return CanvasJS.formatDate( e.value, "DD MMM");
                }
            },
            axisY: {
                //logarithmic: true, //change it to false
                title: "Total",
                titleFontColor: "#6D78AD",
                lineColor: "#6D78AD",
                gridThickness: 1,
                lineThickness: 1,
                //scaleBreaks: {
                //    autoCalculate: true
                //}
                //labelFormatter: addSymbols
            },
            legend: {
                verticalAlign: "top",
                fontSize: 16,
                dockInsidePlotArea: true
            },
            data: [{
                type: "column",
                //xValueFormatString: "####",
                showInLegend: true,
                name: "Total",
                dataPoints: total_data
            },
            {
                type: "column",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Paid",
                dataPoints: paid_data
            },
            {
                type: "column",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Spend",
                dataPoints: spend_data
            },
            {
                type: "column",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Profit",
                dataPoints: profit_data
            }]
        });
        chart.render();
        var sumchart = new CanvasJS.Chart("sumchartContainer", {
            animationEnabled: true,
            zoomEnabled: true,
            //theme: "dark2",
            title: {
                text: "Market Growth Trend"
            },
            axisX: {
                title: "Day",
                labelFormatter: function(e){
                    return CanvasJS.formatDate( e.value, "DD MMM");
                }
            },
            axisY: {
                //logarithmic: true, //change it to false
                title: "Total",
                titleFontColor: "#6D78AD",
                lineColor: "#6D78AD",
                gridThickness: 1,
                lineThickness: 1,
                //scaleBreaks: {
                //    autoCalculate: true
                //}
                //labelFormatter: addSymbols
            },
            legend: {
                verticalAlign: "top",
                fontSize: 16,
                dockInsidePlotArea: true
            },
            data: [{
                type: "line",
                //xValueFormatString: "####",
                showInLegend: true,
                name: "Sales",
                dataPoints: total_sum_data
            },
            {
                type: "line",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Profit",
                dataPoints: profit_sum_data
            },
            {
                type: "line",
                //xValueFormatString: "####",
                //axisYType: "secondary",
                showInLegend: true,
                name: "Freight",
                dataPoints: spend_sum_data
            },
            ]
        });
        sumchart.render();
    }
}
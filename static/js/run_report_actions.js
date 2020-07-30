$(document).ready(function() {
    id_progress_step = document.getElementById("id_progress_step");
    if(id_progress_step){
        $("#id_progress_step").val(1)
    }
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
       gen_progress_trend(data_trend,"chartContainer");
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
      gen_progress_trend(data.result, "chartContainer");
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
            pie_data.push({y: data[i].total, label: data[i].name})    
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

function gen_progress_trend(data, container){
    var total_data = [];
    var paid_data = [];
    console.debug(data)
    if(data.length){
        for(var i = 0;i < data.length;i++){
            date = new Date(data[i].date)
            element = {};
            element.x = date;
            element.y = data[i].total/10000;
            total_data.push(element);
            element = {};
            element.x = date;
            element.y = data[i].paid/10000;
            paid_data.push(element);      
        }
        console.debug(total_data)
        console.debug(paid_data)
        //console.debug(running_data)
        var chart = new CanvasJS.Chart("chartContainer", {
            animationEnabled: true,
            zoomEnabled: true,
            //theme: "dark2",
            title: {
                text: "Market Growth"
            },
            //axisX: {
            //    title: "Year",
            //    valueFormatString: "####",
            //    interval: 2
            //},
            axisY: {
                //logarithmic: true, //change it to false
                title: "Total(/w)",
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
            }]
        });
        chart.render();
    }
}
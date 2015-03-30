function plotTimings(data){

	var cache = data['type'];
	var riq_t = data['riq'];
	var riq_tf = data['riqf'];
	var virt_t = data['virt'];
	var jena_t = data['jena'];

    $('#time').highcharts({
        chart: {
            type: 'bar',
			margin: 0,
			marginLeft: 2,
			height: 350,
			width: 235,
			borderWidth:0,


        },
        title: {
            text: 'Cache:'
        },
        subtitle: {
            text: cache,
        },
        xAxis: {

            title: {
                text: 'Time (sec)',
            }
        },
        yAxis: {
            min: 0,
			gridLineWidth:0,
			max:150,

            title: {
                text: '',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' seconds'
        },
        plotOptions: {

            series: {
                pointWidth: 40,
                stacking: 'normal'

            },
            bar:
            	{
				stacking: 'normal',
				slicedOffset: 0,
                dataLabels: {
                    enabled: true

                }
            }
        },
        legend: {

            floating: true,
            y:10,
            borderWidth: 0,
            backgroundColor: '#FFFFFF',
            shadow: false,
			itemMarginBottom:5,
			width: 190

        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'RIQ-refinement',
            data: [Number(riq_t)],
            color: 'blue',
            stack:0
        }, {
            name: 'RIQ-filtering',
            data: [Number(riq_tf)],
			color: 'lightblue',
            stack:0
        }, {
            name: 'JenaTDB',
            data: [Number(jena_t)],
			color: 'green',
            stack:1
        }, {
            name: 'Virtuoso',
            data: [Number(virt_t)],
            color:'red',
			stack:2

        }]
    });

}
function getQueryTimimgs()
{

	$.ajax({
	url: "/execute/timings/",
	type: "GET",
	dataType: "json",
		error: function(response,n, textStatus, exception) {
		alert('Form Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	},
	success: function(data) {
		plotTimings(data);
		}});


}

function getLable(str){
                var objValue = str;

				if (str.indexOf("http://") != -1)
				{
					objValue = objValue.substring(str.lastIndexOf("/")+1);
					objValue = objValue.replace(">", "");
				}
                return objValue.trim();
}

function getQueryGraph()
{

	$.ajax({
	url: "/execute/graph/",
	type: "GET",
	dataType: "json",
		error: function(response,n, textStatus, exception) {
		alert('Form Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	},
	success: function(data) {
			var links = new Array();
			for(var triple in data){
				var link = {source: getLable(data[triple].subject), target: getLable(data[triple].object), label: getLable(data[triple].predicate)};
				links.push(link);

			}
// 			var links = [
// 			  {source: "Microsoft", target: "HTC", label: "licensing"},
// 			  {source: "Microsoft", target: "HTC", label: "suit"},
// 			  {source: "Microsoft", target: "HTC", label: "resolved"},
// 			  {source: "Samsung", target: "Apple", label: "suit"},
// 			  {source: "Motorola", target: "Apple", label: "suit"},
// 			];

			render(links);
		}});


}
function getQueryResults()
{

	$.ajax({
	url: "/execute/results/",
	type: "GET",
	dataType: "text",
		error: function(response,n, textStatus, exception) {
		alert('Form Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	},
	success: function(data) {

		 rframe = $('#results');
		rframe.text(data);
		}});


}

function showQuery(e)
{
	var d= "name=" + e.value;
	var obj = $('#query').unbind();

	$.ajax({
	url: "/execute/getquery/",
	type: "GET",
	dataType: "text",
	data: d,
	success: function(m) {
		obj.text(m);
		obj.html(obj.html().replace(/\n/g,'&nbsp;<br/>'));
		obj.html(obj.html().replace(/\t/g,'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'));
		obj.bind('DOMNodeInserted DOMSubtreeModified DOMNodeRemoved', function(event) {
		document.getElementById("queryDisplay").selectedIndex = 5;

		});
	}
	});
}

//Javascript to run RIQ
function runRIQ(e)
{

	document.getElementById("query-text").value= $('#query').html().replace(/<br\s*[\/]?>|&nbsp;/gi,' ').replace(/&lt;/gi,' <').replace(/&gt;/gi,'> ');

	var form = document.getElementById("frmRIQ");
	var formURL = form.action;
	var postData = $('#frmRIQ').serialize();

	$.ajax({
	url: '/execute/',
	type: "POST",
	dataType: "text",
	data: postData,
	timeout: 9000000000,
	success: function(m) {
		console.log("Execute Form Submitted Successfully");

	},
	error: function(response,n, textStatus, exception) {
		alert('Form Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	}
	});
	getQueryResults();
	getQueryTimimgs();
	getQueryGraph();

}

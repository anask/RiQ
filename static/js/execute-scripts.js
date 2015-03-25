function plotTimings(data){

	var cache = data['type'];
	var riq_t = data['riq'];
	var virt_t = data['virt'];
	var jena_t = data['jena'];


    $('#time').highcharts({
        chart: {
            type: 'bar',
			margin: 0,

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
            bar: {
				slicedOffset: 0,
                size: '100%',

                dataLabels: {
                    enabled: true

                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -60,
            y: 315,
            floating: true,
            borderWidth: 1,
            backgroundColor: '#FFFFFF',
            shadow: false
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'RIQ/JenaTDB',
            data: [Number(riq_t)],
            color: 'blue',
        }, {
            name: 'JenaTDB',
            data: [Number(jena_t)],
			color: 'green'
        }, {
            name: 'Virtuoso',
            data: [Number(virt_t)],
            color:'red',
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
		obj.html(obj.html().replace(/\n/g,'<br/>'));
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
	document.getElementById("query-text").value= $('#query').text();

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

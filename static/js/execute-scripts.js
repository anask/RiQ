function plotTimings(data){

	var cache = data['type'];
	var riq_t = data['riq'];
	var riq_tf = data['riqf'];
	var virt_t = data['virt'];
	var jena_t = data['jena'];

    $('#time').highcharts({
        chart: {
			type: 'column',
			margin: 0,
			marginLeft: 8,
			height: 300,
			width: 265,
			borderWidth:0,
			marginTop: 60,
			marginBottom: 80,
            backgroundColor: 'none',



        },
        title: {
            text: cache+' cache',
			style: {
						fontSize: "14px",
						color:"#000"
					},
        },
        xAxis: {
			min:0,
			gridLineWidth:0,
			tickLength: 0,
			lineColor:'#DCB543',
			labels: {
				enabled: false
            }


        },
        yAxis: {
			gridLineWidth:0,
			min:0,
			max:100,
            labels: {
				enabled: false
            }
        },
        tooltip: {
            valueSuffix: ' seconds',
			formatter: function () {
                return '<b>' + this.y + '</b>';
            },
            positioner:function(labelWidth, labelHeight, point){

				return {
					x: 25,
					y: 28
				};
			}
        },
        plotOptions: {

            series: {
                pointWidth: 45,
                stacking: 'normal'

            },
            column:
            	{
				stacking: 'normal',
				slicedOffset: 0,
                dataLabels: {
					verticalAlign: 'top',
					enabled: true,
					style: {
						fontWeight:'normal',
						textShadow:'none',
					},


                }
            }
        },
        legend: {

            floating: false,
            y:10,
            borderWidth: 0,
            backgroundColor: 'none',
            shadow: false,
			itemMarginBottom:5,
			width: 190

        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'RIQ',
            data: [Number(riq_t)],
            color: '#0101DF',
            stack:0
        }, {
            name: 'RIQ (filtering)',
            data: [Number(riq_tf)],
			color: '#01A9DB',
            stack:0
        }, {
            name: 'Virtuoso',
            data: [Number(virt_t)],
            color:'red',
			stack:2

        },{
            name: 'JenaTDB',
            data: [Number(jena_t)],
			color: 'green',
            stack:1
        }]
    });
	document.getElementById('note').innerHTML="Note: Query not supported by RDF-3X";


}
function getQueryTimimgs()
{

	$.ajax({
	url: "/execute/timings/",
	type: "GET",
	dataType: "json",
		error: function(response,n, textStatus, exception) {
		alert('Error: ' + response.responseText);
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
		alert('Error: ' + response.responseText);
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
			$('#query-graph').html('');
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
		alert('Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	},
	success: function(data){

                        var rframe = document.getElementById('results');
                        rframe.innerHTML= data.replace(/</gim,'&lt;').replace(/>/gim,'&gt;');
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

function displayLoaders(show){
        var graph = document.getElementById('query-graph');
        var time = document.getElementById('time');
        var results = document.getElementById('results');

if(show){
	var ldrImgResults = "<img src='/static/images/ajax-loader-yellow.gif' style='display: block;margin: auto; margin-top:5px;'/>";
	var ldrImg1 = "<img src='/static/images/ajax-loader-yellow.gif' style='display: block;margin: auto; margin-top:118px;'/>";
	var ldrImg2 = "<img src='/static/images/ajax-loader-yellow.gif' style='display: block;margin: auto; margin-top:100px;'/>";

	results.innerHTML=ldrImgResults;
	time.innerHTML=ldrImg2;
	graph.innerHTML=ldrImg1;

}
else{
        results.innerHTML='';
        time.innerHTML='';
        graph.innerHTML='';

}
}

function getStatusUpdates(){

		var isDone='false';
		var url = "/execute/getstatus/?verbose=false";
		isDone=httpGet(url)

		if(isDone == 'false') {
		       setTimeout(getStatusUpdates, 5000); /* this checks the flag every 100 milliseconds*/
		} else {

				displayLoaders(false);
				if(isDone=='true'){
					getQueryResults();
					getQueryTimimgs();
					getQueryGraph();
				}
				else
					alert('Query Execution Error');
    	}




}
//Jevascript to run RIQ
function runRIQ(e)
{
	//display loader img
	displayLoaders(true);

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
		alert('Query Received!\nClick the status icon i (see footer) for updates.');
		getStatusUpdates();

	},
	error: function(response,n, textStatus, exception) {
		alert(response.responseText);
		console.log(n);
		console.log(textStatus);
		displayLoaders(false);

	}
	});



}

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

function getStatusUpdates(){

                var isDone='false';
                var url = "/linked/getstatus/";
                isDone=httpGet(url)

                if(isDone == 'false') {
                       setTimeout(getStatusUpdates, 5000); /* this checks the flag every 100 milliseconds*/
                } else{ 
                	document.getElementById('rLoader').innerHTML='';
                	document.getElementById('tLoader').innerHTML='';
			getQueryResults();
                	//document.getElementById('results').innerHTML=response;
		}

}
function displayLoaders(){

	var ldrImgResults = "<img src='/static/images/ajax-loader-green.gif' style='display: block;margin: auto; margin-top:5px;'/>";
	var ldrImgTime = "<img src='/static/images/ajax-loader-green.gif' style='display: block;margin: auto; margin-top:100px;'/>";
	var loadR = document.getElementById('rLoader');
	var time = document.getElementById('tLoader');
	var results = document.getElementById('results');
	loadR.innerHTML=ldrImgResults;
	time.innerHTML=ldrImgTime;
	results.innerHTML="";


}
function getQueryTimimgs()
{

	$.ajax({
	url: "/linked/timings/",
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


function getQueryResults()
{

 	$.ajax({
 	url: "/linked/getresults/",
 	type: "GET",
 	dataType: "text",
 		error: function(response,n, textStatus, exception) {
 		alert('Form Error: ' + response.responseText);
 		console.log(n);
 		console.log(textStatus);

 	},
 	success: function(data) {

 		 rframe = $('#results');
 		rframe.html(data);
 		}});


}

function showQuery(e)
{
	var d= "name=" + e.value;
	var obj = $('#query').unbind();

	$.ajax({
	url: "/linked/getquery/",
	type: "GET",
	dataType: "text",
	data: d,
	success: function(m) {
		obj.text(m);
		obj.html(obj.html().replace(/\n/g,'&nbsp;<br/>'));
		obj.html(obj.html().replace(/\t/g,'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'));
		obj.bind('DOMNodeInserted DOMSubtreeModified DOMNodeRemoved', function(event) {
		document.getElementById("queryDisplay").selectedIndex = 2;

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
	url: '/linked/',
	type: "POST",
	dataType: "text",
	data: postData,
	timeout: 9000000000,
	success: function(response,n, textStatus, exception) {

		console.log("Linked Form Submitted Successfully");
		getStatusUpdates();
	},
	error: function(response,n, textStatus, exception) {
		alert('Form Error: ' + response.responseText);
		console.log(n);
		console.log(textStatus);

	}
	});
	displayLoaders();
	//getQueryResults();
	//getQueryTimimgs();

}


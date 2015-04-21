function getCandidateTree(s) {

	var cqTree = document.getElementById('parseCandTree');
	//display loader img
	cqTree.innerHTML = '<img id="candquerytree" src="/static/images/ajax-loader-blue.gif" style = "display: block;margin: auto; margin-top:80px;"/>'



// 	$.ajax({
// 		url: "/visualize/candquery/?cand=" + s.value,
// 		type: "GET",
// 		dataType: "json",
// 		error: function(response, n, textStatus, exception) {
// 			alert('Error: ' + response.responseText);
// 			console.log(n);
// 			console.log(textStatus);
// 			 cqTree.innerHTML='';
//
// 		},
// 		success: function(data) {
// 			var htmlStr = data['query'];
// 			htmlStr.replace(/\n/g, '&nbsp;<br/>');
// 			htmlStr.replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');
// 			document.getElementById('candquery').innerHTML = htmlStr;
// 			cqTree.innerHTML='';
// 		}
// 	});


	//show cand query parse tree
	$.ajax({
		url: "/visualize/parse/?cand="+s.value,
		type: "GET",
		dataType: "json",
		error: function(response, n, textStatus, exception) {
			alert('Error: ' + response.responseText);
			console.log(n);
			console.log(textStatus);

		},
		success: function(data) {
			cqTree.innerHTML = '';
			renderD3JsonGraph('#parseCandTree',JSON.parse(data));
		}
	});

// 	var url1 = "/visualize/candidatetree/?new=yes&cand=" + s.value;
// 	var url2 = "/visualize/candidatetree/?new=no&cand=" + s.value;
// 	var c = $("#candtree");
// 	$.ajax({
// 		url: url1,
// 		cache: false,
// 		processData: false,
// 	}).done(function() {
// 		c.attr("src", url2).attr("data-zoom-image", url2).fadeIn().elevateZoom({
// 			zoomType: "lens",
// 			lensShape: "rectangle",
// 			lensSize: 200,
// 			zoomWindowPosition: 1
// 		});
// 		c.css("width", "100%");
// 		c.css("height", "80%");
// 		c.css("display", "inline");
// 		c.css("margin", "0px");
//
// 	});


}

function getQueryTree() {


	var qTree = document.getElementById('parseQueryTree');
	//display loader img
	qTree.innerHTML = '<img id="querytree" src="/static/images/ajax-loader-blue.gif" style = "display: block;margin: auto; margin-top:80px;"/>'

	//show query
	$.ajax({
		url: "/visualize/query/",
		type: "GET",
		dataType: "json",
		error: function(response, n, textStatus, exception) {
			alert('Error: ' + response.responseText);
			console.log(n);
			console.log(textStatus);

		},
		success: function(data) {
			var htmlStr = data['query'];

			htmlStr.replace(/\n/g, '&nbsp;<br/>');
			htmlStr.replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');

			document.getElementById('query').innerHTML = htmlStr;


		}
	});

	//show query parse tree
	$.ajax({
		url: "/visualize/parse/?cand=false",
		type: "GET",
		dataType: "json",
		error: function(response, n, textStatus, exception) {
			alert('Error: ' + response.responseText);
			console.log(n);
			console.log(textStatus);

		},
		success: function(data) {
			qTree.innerHTML = '';
			renderD3JsonGraph('#parseQueryTree',JSON.parse(data));
		}
	});

// 	var url1 = "/visualize/querytree/?exec=yes";
// 	var url2 = "/visualize/querytree/?exec=no";
// 	$.ajax({
// 		url: url1,
// 		cache: true,
// 		processData: false,
// 	}).done(function() {
// 		var c = $("#querytree");
// 		c.attr("src", url2).attr("data-zoom-image", url2).fadeIn().elevateZoom({
// 			zoomType: "lens",
// 			lensShape: "rectangle",
// 			lensSize: 250,
// 			zoomWindowPosition: 1
// 		});
// 		c.css("width", "100%");
// 		c.css("height", "80%");
// 		c.css("display", "inline");
// 		c.css("margin", "0px");
//
// 	});

}

function getQueryCandidates() {

	$.ajax({
		url: "/visualize/candidates/",
		type: "GET",
		dataType: "json",
		error: function(response, n, textStatus, exception) {
			alert('Form Error: ' + response.responseText);
			console.log(n);
			console.log(textStatus);

		},
		success: function(data) {

			var htmlStr = "";
			var key, i = 0;
			for (key in data.candidates)
				htmlStr = htmlStr + '<option value="' + data.candidates[i] + '" > Candidate ' + i++ + '</option>';
			document.getElementById('cands').innerHTML = htmlStr;


		}
	});


}


function getQueryInfo() {

	$.ajax({
		url: "/visualize/info/",
		type: "GET",
		dataType: "json",
		error: function(response, n, textStatus, exception) {
			alert('Form Error: ' + response.responseText);
			console.log(n);
			console.log(textStatus);

		},
		success: function(data) {
			document.getElementById('qName').innerHTML = data['name'];
			document.getElementById('qIndex').innerHTML = data['index'];
			document.getElementById('qCache').innerHTML = data['cache'];
			document.getElementById('qOpt').innerHTML = data['opt'];

		}
	});
}

function runAntlr() {

	getQueryTree();
	getQueryCandidates();
}
$(document).ready(function() {
	getQueryInfo();
});

function renderD3JsonGraph(container, data)
{
var margin = {top: 40, right: 100, bottom: 10, left: 100},
                   width = 1000 - margin.right - margin.left,
                   height = 1000 - margin.top - margin.bottom;

                   var i = 0,
                   duration = 750,
                   root;

                   var tree = d3.layout.tree()
                   .size([height, width]);

                   var diagonal = d3.svg.diagonal()
                   .projection(function(d) { return [d.x, d.y]; });

                   var svg = d3.select(container).append("svg")
                   .attr("width", width + margin.right + margin.left)
                   .attr("height", height + margin.top + margin.bottom)
                   .append("g")
                   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


                   root = data;
                   root.x0 = height / 2;
                   root.y0 = 0;

                   function collapse(d) {
                   if (d.children) {
                   d._children = d.children;
                   d._children.forEach(collapse);
                   d.children = null;
                   }
                   }

                 //  root.children.forEach(collapse);
                   update(root);

                   d3.select(self.frameElement).style("height", height + "px");

                   function update(source) {

                   // Compute the new tree layout.
                   var nodes = tree.nodes(root).reverse(),
                   links = tree.links(nodes);

                   // Normalize for fixed-depth.
                    nodes.forEach(function(d) { d.y = d.depth * 100; });

                   // Update the nodes…
                   var node = svg.selectAll("g.node")
                   .data(nodes, function(d) { return d.id || (d.id = ++i); });

                   // Enter any new nodes at the parent's previous position.
                   var nodeEnter = node.enter().append("g")
                   .attr("class", "node")
                   .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                   .on("click", click);

                   nodeEnter.append("circle")
                   .attr("r", 1e-6)
                   .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

                   nodeEnter.append("text")
                   .attr("x", function(d) { return d.children || d._children ? 12 : 10; })
                   .attr("dy", "0.4em")
                   .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
				   .attr("text-anchor", "right")
                   .text(function(d) {
					   var nameArr = d.name.split(":");
                    	if(nameArr[1].charAt(0)=='0'){
                    		return nameArr[0]+" (F)";
                    	}
                    		return nameArr[0]+" (T)";

                   })
                   .style("fill-opacity", 1e-6);

                   // Transition nodes to their new position.
                   var nodeUpdate = node.transition()
                   .duration(duration)
                   .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

                   nodeUpdate.select("circle")
                   .attr("r", 8.5)
                   .style("fill", function(d) {

                    var nameArr = d.name.split(":");
                    	if(nameArr[1].charAt(0)=='0'){
                    		return "red";
                    	}
                    	return "green";
                   	 });


                  nodeUpdate.select("text").style("fill-opacity", 1);

                   // Transition exiting nodes to the parent's new position.
                   var nodeExit = node.exit().transition()
                   .duration(duration)
                   .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
                   .remove();

                   nodeExit.select("circle")
                   .attr("r", 1e-6);

                   nodeExit.select("text")
                   .style("fill-opacity", 1e-6);

                   // Update the links…
                   var link = svg.selectAll("path.link")
                   .data(links, function(d) { return d.target.id; });

                   // Enter any new links at the parent's previous position.
                   link.enter().insert("path", "g")
                   .attr("class", "link")
                   .attr("d", function(d) {
                   var o = {x: source.x0, y: source.y0};
                   return diagonal({source: o, target: o});
                   });

                   // Transition links to their new position.
                   link.transition()
                   .duration(duration)
                   .attr("d", diagonal);

                   // Transition exiting nodes to the parent's new position.
                   link.exit().transition()
                   .duration(duration)
                   .attr("d", function(d) {
                   var o = {x: source.x, y: source.y};
                   return diagonal({source: o, target: o});
  })
                   .remove();

                   // Stash the old positions for transition.
                   nodes.forEach(function(d) {
                   d.x0 = d.x;
                   d.y0 = d.y;
                   });
  }

                   // Toggle children on click.
                   function click(d) {
                   if (d.children) {
                   d._children = d.children;
                   d.children = null;
                   } else {
                   d.children = d._children;
                   d._children = null;
                   }
                   update(d);
                   }
}
// end of d3 graph javascript
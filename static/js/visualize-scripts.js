function getCandidateTree(s) {
	var cTree = document.getElementById('candtree');
	cTree.setAttribute("src", '/static/images/ajax-loader.gif');
	cTree.style = "display: block;margin: auto; margin-top:80px";

	$.ajax({
		url: "/visualize/candquery/?cand=" + s.value,
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
			document.getElementById('candquery').innerHTML = htmlStr;
		}
	});

	var url1 = "/visualize/candidatetree/?new=yes&cand=" + s.value;
	var url2 = "/visualize/candidatetree/?new=no&cand=" + s.value;
	var c = $("#candtree");
	$.ajax({
		url: url1,
		cache: false,
		processData: false,
	}).done(function() {
		c.attr("src", url2).attr("data-zoom-image", url2).fadeIn().elevateZoom({
			zoomType: "lens",
			lensShape: "rectangle",
			lensSize: 200,
			zoomWindowPosition: 1
		});
		c.css("width", "100%");
		c.css("height", "80%");
		c.css("display", "inline");
		c.css("margin", "0px");

	});


}

function getQueryTree() {

	var qTree = document.getElementById('querytree');
	qTree.setAttribute("src", '/static/images/ajax-loader.gif');
	qTree.style = "display: block;margin: auto; margin-top:80px";

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


	var url1 = "/visualize/querytree/?exec=yes";
	var url2 = "/visualize/querytree/?exec=no";
	$.ajax({
		url: url1,
		cache: true,
		processData: false,
	}).done(function() {
		var c = $("#querytree");
		c.attr("src", url2).attr("data-zoom-image", url2).fadeIn().elevateZoom({
			zoomType: "lens",
			lensShape: "rectangle",
			lensSize: 250,
			zoomWindowPosition: 1
		});
		c.css("width", "100%");
		c.css("height", "80%");
		c.css("display", "inline");
		c.css("margin", "0px");

	});

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
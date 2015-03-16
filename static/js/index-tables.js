function showtables(stats){
	var total = Number(stats.group.build_graph_t)+Number(stats.group.pv_lsh_t)+Number(stats.group.union_t)+Number(stats.group.total_t)+Number(stats.cbf.cbf_t)+Number(stats.split.split_t )+Number(stats.pv_t);
	var t_content = "<table style='width:100%' > ";
		t_content += '<tr>';
				t_content += "<td style='font-weight:500;'> G BUILD GRAPH</td>"+"<td style='font-weight:400;color:#000;'>" + stats.group.build_graph_t  + '</td>';
									t_content += "<td style='font-weight:500;'> G PV LSH</td>"+"<td style='font-weight:400;color:#000;'>" + stats.group.pv_lsh_t  + '</td>';
									t_content += "<td style='font-weight:500;'> G UNION</td>"+"<td style='font-weight:400;color:#000;'>" + stats.group.union_t  + '</td>';
									t_content += "<td style='font-weight:500;'> G TOTAL</td>"+"<td style='font-weight:400;color:#000;'>" + stats.group.total_t  + '</td>';
					t_content += '</tr>'
					t_content += '<tr>'
									t_content += "<td style='font-weight:500;'> CBF</td>"+"<td style='font-weight:400;color:#000;'>" + stats.cbf.cbf_t  + '</td>';
									t_content += "<td style='font-weight:500;'> SPLIT</td>"+"<td style='font-weight:400;color:#000;'>" + stats.split.split_t  + '</td>';
									t_content += "<td style='font-weight:500;'> PV CONSTRUCTION</td>"+"<td style='font-weight:400;color:#000;'>" + stats.pv_t  + '</td>';
									t_content += "<td style='font-weight:500;'> TOTAL</td>"+"<td style='font-weight:400;color:#000;'>" + total.toFixed(2)  + '</td>';
					t_content += '</tr>';
	t_content += "</table>";

	var pv_content = "<table style='width:100%' > ";
			pv_content += '<tr>';
									pv_content += "<td style='font-weight:500;'> AVG GRAPH SIZE</td>"+"<td style='font-weight:400;color:#000;'>" + stats["Avg graph size"]  + '</td>';
									pv_content += "<td style='font-weight:500;'> WRITTEN GRAPHS</td>"+"<td style='font-weight:400;color:#000;'>" + stats["Written graphs"]  + '</td>';
									pv_content += "<td style='font-weight:500;'> MAX GRAPH SIZE</td>"+"<td style='font-weight:400;color:#000;'>" + stats["Max graph size"]  + '</td>';
			pv_content += '</tr>'
			pv_content += '<tr>'
									pv_content += "<td style='font-weight:500;'> TOTAL URIS/LITERALS</td>"+"<td style='font-weight:400;color:#000;'>" + stats["Total URIs/literals"]  + '</td>';
									pv_content += "<td style='font-weight:500;'> TOTAL SIZE</td>"+"<td style='font-weight:400;color:#000;'>" + stats["Total size"]  + '</td>';
									pv_content += "<td style='font-weight:500;'> PV CONSTRUCTION TIME</td>"+"<td style='font-weight:400;color:#000;'>" + stats.pv_t  + '</td>';
			pv_content += '</tr>';
		pv_content += "</table>";



	$(document).ready(function ()
	{
		$("#timings").html(t_content);
		$("#stats").html(pv_content);
	});
}
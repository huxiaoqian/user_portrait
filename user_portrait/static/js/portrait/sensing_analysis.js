var data=[['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称1','民生类_社会保障','法律机构及人士','234',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称3','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称4','','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称5','话题2','法律机构及人士','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称3','话题3','领域domain','34',23,56]]
var sensor_head=['序号','头像','昵称','领域','话题','影响力','重要度','活跃度']
var sensor2_head=['头像','昵称','领域','话题','热度','影响力','重要度','活跃度']

function sensing_sensors_table (head, data, div_name) {
    $('#'+div_name).empty();
	if(data.length>7){
		$('#'+div_name).css("overflow-y", "auto");
	}
	var html = '';
	html += '<table id="" class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
	html += '<th style="text-align:center">'+head[i]+'</th>';

	}
	html += '</tr></thead>';
	html += '<tbody>';

	for(var i=0; i<data.length; i++){
		var s= i+1;
		html += '<tr>';
		html += '<td style="text-align:center;vertical-align:middle;">' + s + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<img src="'+data[i][0] +'" class="small-photo shadow-5" title="' + data[i][1] +'">' + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][1] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][2] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][4] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 10 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 16 + '</td>';
		html += '</tr>';
	}
	html += '</tbody></table>';
	$('#'+div_name).append(html);
}

function sensing_participate_table (head, data, div_name) {
    $('#'+div_name).empty();
	if(data.length>7){
		$('#'+div_name).css("overflow-y", "auto");
	}
	var html = '';
	html += '<table id="participate_table" class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
	html += '<th style="text-align:center">'+head[i]+'</th>';
	}
	html += '<th style="text-align:center"> <input name="participate_select_all" id="participate_select_all" type="checkbox" value="" onclick="participate_select_all()" /></th>';
	html += '</tr></thead>';
	html += '<tbody>';

	for(var i=0; i<data.length; i++){
		var s= i+1;
		html += '<tr>';
		// html += '<td style="text-align:center;vertical-align:middle;">' + s + '234567890</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<img src="'+data[i][0] +'" class="small-photo shadow-5" title="' + data[i][1] +'">' + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][1] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][2] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][4] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][5] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 10 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 16 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<input name="participate_select" type="checkbox" id="participate_select" value ="'+data[i][1]+'">' + '</td>';
		html += '</tr>';
	}
	html += '</tbody></table>';
	$('#'+div_name).append(html);
	$('#participate_table').dataTable({
        	"sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",

        	"sPaginationType": "bootstrap",
        	"aoColumnDefs":[ {"bSortable": false, "aTargets":[8]}, {"bAutoWidth": true, "aTargets":["_all"]}],
        	// "bAutoWidth": true,
        	"oLanguage": {

            	"sLengthMenu": "_MENU_ 每页"

        }

    });
}

sensing_sensors_table(sensor_head,data,'modal_sensor_table',false);
//sensing_participate_table(sensor2_head,data,"modal_participate_table", true);
sensing_participate_table(sensor2_head,data,"sensing_participate_table", true);

function participate_select_all(){
	  $('input[name="participate_select"]:not(:disabled)').prop('checked', $("#participate_select_all").prop('checked'));
}
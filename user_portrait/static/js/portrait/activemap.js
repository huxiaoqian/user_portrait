function month_process(data){
    require.config({
        paths: {
            echarts: '/static/js/bmap/js'
        },
        packages: [
            {
                name: 'BMap',
                location: '/static/js/bmap',
                main: 'main'
            }
        ]
    });

    require(
    [
        'echarts',
        'BMap',
        'echarts/chart/map'
    ],
    function (echarts, BMapExtension) {
        // 初始化地图
        var BMapExt = new BMapExtension($('#map')[0], BMap, echarts,{
            enableMapClick: false
        });
        var map = BMapExt.getMap();
        var container = BMapExt.getEchartsContainer();
        var startPoint = {
            x: 104.114129,
            y: 37.550339
        };

        var point = new BMap.Point(startPoint.x, startPoint.y);
        map.centerAndZoom(point, 5);
        map.enableScrollWheelZoom(true);
        console.log(data);
        // process
        var timelist = new Array();
        var geolist = new Array();
        for (var i = 0; i < data.length; i++){
            var time_geo = data[i];
            timelist.push(time_geo[0]);
            geolist.push(time_geo[1].split('\t').pop());
        }
        // marker
        var newgeo = new Array();
        var myGeo = new BMap.Geocoder();
        //var geolist = ['北京', '上海','广州','南宁', '南昌', '大连','拉萨'];
        var index = 0;
        bdGEO();
        function bdGEO(){
            var geoname = geolist[index];
            var timename = timelist[index];
            geocodeSearch(geoname, timename);
            index++;
        }
        function geocodeSearch(geoname, timename){
            if(index < geolist.length-1){
                setTimeout(bdGEO,400);
            }
            else{
                setTimeout(drawline, 400);
            }
            myGeo.getPoint(geoname, function(point){
                if (point){
                    var fixpoint= new BMap.Point(point.lng+3.5,point.lat-0.5);
                    var marker = new BMap.Marker(fixpoint);
                    marker.setTitle(geoname+','+timename);
                    map.addOverlay(marker);
                    newgeo[geoname] = [fixpoint.lng,fixpoint.lat];
                }
                else{
                    //alert("no such point!");
                }
            }, geoname);
        }
        function drawline(){
            var linklist = new Array();
            var last_geo = geolist[0];
            for (var i = 1; i < geolist.length; i++){
                linklist.push([{name:last_geo},{name:geolist[i], value:90}]);
                last_geo = geolist[i];
            }
            console.log(linklist);
            //linklist = [[{name:'北京'}, {name:'南宁',value:90}],[{name:'北京'}, {name:'南昌',value:90}],[{name:'北京'}, {name:'拉萨',value:90}]];
            //console.log(linklist);
            var option = {
                color: ['gold','aqua','lime'],
                title : {
                    text: '',
                    subtext:'',
                    x:'center',
                    textStyle : {
                        color: '#fff'
                    }
                },
                tooltip : {
                    trigger: 'item',
                    formatter: function (v) {
                        return v[1].replace(':', ' > ');
                    }
                },
                toolbox: {
                    show : false,
                    orient : 'vertical',
                    x: 'right',
                    y: 'center',
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                dataRange: {
                    show: false,
                    min : 0,
                    max : 100,
                    range: {
                        start: 10,
                        end: 90
                    },
                    x: 'right',
                    calculable : true,
                    color: ['#ff3333', 'orange', 'yellow','lime','aqua'],
                    textStyle:{
                        color:'#fff'
                    }
                },
                series : [
                    {
                        name:'全国',
                        type:'map',
                        mapType: 'none',
                        data:[],
                        geoCoord: newgeo,
                        markLine : {
                            smooth:true,
                            effect : {
                                show: true,
                                scaleSize: 1,
                                period: 30,
                                color: '#fff',
                                shadowBlur: 10
                            },
                            itemStyle : {
                                normal: {
                                    borderWidth:1,
                                    label:{show:false},
                                    lineStyle: {
                                        type: 'solid',
                                        shadowBlur: 10
                                    }
                                }
                            },
                            data : linklist
                        },
                    }
                ]
            };

            var myChart = BMapExt.initECharts(container);
            window.onresize = myChart.onresize;
            BMapExt.setOption(option);
        }
    }
);
}
var url = '/attribute/location/?uid='+uid+'&time_type=month';
activity_call_ajax_request(url, location_desc);

function location_desc(data){
    //console.log(data);
    $('#locate_desc').html(data.description.join('')); //description
    var location_geo = data.all_top;
    $('#monthly_location').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">地点</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < location_geo.length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m;
       html += '</th><th style="text-align:center">' + location_geo[i][0];
       html += '</th><th style="text-align:center">' + location_geo[i][1];
       html +='</th></tr>';
    };
    html += '</table>'; 
    $('#monthly_location').append(html);                  
    // track map
    month_process(data.month_track);
}

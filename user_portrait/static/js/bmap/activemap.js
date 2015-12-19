(function () {
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
        // marker
        var newgeo = new Array();
        var myGeo = new BMap.Geocoder();
        var geolist = ['北京', '上海','广州','南宁', '南昌', '大连','拉萨','长春','包头','重庆','常州'];
        var index = 0;
        bdGEO();
        function bdGEO(){
            var geoname = geolist[index];
            geocodeSearch(geoname);
            index++;
        }
        function geocodeSearch(geoname){
            console.log(index);
            if(index < geolist.length-1){
                setTimeout(bdGEO,400);
            }
            else{
                setTimeout(drawline, 400);
            }
            myGeo.getPoint(geoname, function(point){
                console.log(geoname);
                if (point){
                    var fixpoint= new BMap.Point(point.lng+3.5,point.lat-0.5);
                    map.addOverlay(new BMap.Marker(fixpoint));
                    newgeo[geoname] = [fixpoint.lng,fixpoint.lat];
                    console.log(newgeo);
                }
                else{
                    //alert("no such point!");
                }
            }, geoname);
        }
        function drawline(){
            var option = {
                color: ['gold','aqua','lime'],
                title : {
                    text: '模拟迁徙',
                    subtext:'数据纯属虚构',
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
                        name:'北京',
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
                                    lineStyle: {
                                        type: 'solid',
                                        shadowBlur: 10
                                    }
                                }
                            },
                            data : [
                                [{name:'北京'}, {name:'上海',value:90}],
                                [{name:'北京'}, {name:'广州',value:90}],
                                [{name:'北京'}, {name:'大连',value:90}],
                                [{name:'北京'}, {name:'南宁',value:90}],
                                [{name:'北京'}, {name:'南昌',value:90}],
                                [{name:'北京'}, {name:'拉萨',value:90}],
                                [{name:'北京'}, {name:'长春',value:90}],
                                [{name:'北京'}, {name:'包头',value:90}],
                                [{name:'北京'}, {name:'重庆',value:90}],
                                [{name:'北京'}, {name:'常州',value:90}]
                            ]
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
})();

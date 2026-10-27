$(function () {
    $('.side_list').click(function () {

            var obj=$(this);
            var tit=obj.attr('title')

            var id_str='data_'+tit

            var echart_data=getGoodsData();
            var x_data=[],y_data=[];
            for (let i=0;i<echart_data.length;i++){
                x_data[i]=echart_data[i].name;
                y_data[i]=echart_data[i].sales;


            }

            var chartDom = document.getElementById(id_str);
            var myChart = echarts.init(chartDom);
            var option=null;

            if(tit!='pie'){
                    option = {
                        title:{
                            text:"销量数据",
                            left:'center'
                        },
                      xAxis: {
                        type: 'category',
                        data: x_data
                      },
                      yAxis: {
                        type: 'value'
                      },
                      series: [
                        {
                          data: y_data,
                            //折线图
                          type: tit


                        }
                      ]
                    };
            }else{
               // 饼图
                option = {
                  title: {
                    text: '销量数据',
                    subtext: '饼图销量可视化',
                    left: 'center'
                  },
                  tooltip: {
                    trigger: 'item'
                  },
                  legend: {
                    orient: 'vertical',
                    left: 'left'
                  },
                  series: [
                    {
                      name: '销量',
                      type: 'pie',
                      radius: '50%',
                  data: x_data.map((name, index) => ({
                          value: y_data[index],
                          name: name
                        })),
                      emphasis: {
                        itemStyle: {
                          shadowBlur: 10,
                          shadowOffsetX: 0,
                          shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                      }
                    }
                  ]
                };
            }



            option && myChart.setOption(option);




    })
})
function getGoodsData() {
    var goods=null;
    $.ajax({
        url:'/goods',
        type:'post',
        dataType:'json',
        async:false,
        success:function (data) {
            console.log("请求成功"+data);
            goods=data;
        },
        error:function (e) {
            console.log("请求失败"+e);
        }
    })
    return goods;
}

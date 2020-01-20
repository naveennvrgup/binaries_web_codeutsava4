var graph = new Springy.Graph();
var labels, connections;
var obj = {}

var server = graph.newNode({label:'server'})
var center_1 = graph.newNode({label:'center-1'})
var center_2 = graph.newNode({label:'center-2'})
var center_3 = graph.newNode({label:'center-3'})
var center_4 = graph.newNode({label:'center-4'})
var center_5 = graph.newNode({label:'center-5'})

var farmer_1 = graph.newNode({label:'farmers-1'})
var farmer_2 = graph.newNode({label:'farmers-2'})
var farmer_3 = graph.newNode({label:'farmers-3'})
var farmer_4 = graph.newNode({label:'farmers-4'})
var farmer_5 = graph.newNode({label:'farmers-5'})
var farmer_6 = graph.newNode({label:'farmers-6'})
var farmer_7 = graph.newNode({label:'farmers-7'})
var farmer_8 = graph.newNode({label:'farmers-8'})
var farmer_9 = graph.newNode({label:'farmers-9'})
var farmer_10 = graph.newNode({label:'farmers-1'})
var farmer_11 = graph.newNode({label:'farmers-11'})
var farmer_12 = graph.newNode({label:'farmers-12'})
var farmer_13 = graph.newNode({label:'farmers-13'})
var farmer_14 = graph.newNode({label:'farmers-14'})
var farmer_15 = graph.newNode({label:'farmers-15'})

var farm_1 = graph.newNode({label:'farm-1'})
var farm_2 = graph.newNode({label:'farm-2'})
var farm_3 = graph.newNode({label:'farm-3'})
var farm_4 = graph.newNode({label:'farm-4'})
var farm_5 = graph.newNode({label:'farm-5'})
var farm_6 = graph.newNode({label:'farm-6'})
var farm_7 = graph.newNode({label:'farm-7'})
var farm_8 = graph.newNode({label:'farm-8'})
var farm_9 = graph.newNode({label:'farm-9'})
var farm_10 = graph.newNode({label:'farm-1'})
var farm_11 = graph.newNode({label:'farm-11'})
var farm_12 = graph.newNode({label:'farm-12'})
var farm_13 = graph.newNode({label:'farm-13'})
var farm_14 = graph.newNode({label:'farm-14'})
var farm_15 = graph.newNode({label:'farm-15'})


var warehouse_1 = graph.newNode({label:'warehouse-1'})
var warehouse_2 = graph.newNode({label:'warehouse-2'})
var warehouse_3 = graph.newNode({label:'warehouse-3'})
var warehouse_4 = graph.newNode({label:'warehouse-4'})
var warehouse_5 = graph.newNode({label:'warehouse-5'})
var warehouse_6 = graph.newNode({label:'warehouse-6'})
var warehouse_7 = graph.newNode({label:'warehouse-7'})
var warehouse_8 = graph.newNode({label:'warehouse-8'})
var warehouse_9 = graph.newNode({label:'warehouse-9'})
var warehouse_10 = graph.newNode({label:'warehouse-1'})
var warehouse_11 = graph.newNode({label:'warehouse-11'})
var warehouse_12 = graph.newNode({label:'warehouse-12'})
var warehouse_13 = graph.newNode({label:'warehouse-13'})
var warehouse_14 = graph.newNode({label:'warehouse-14'})
var warehouse_15 = graph.newNode({label:'warehouse-15'})



graph.newEdge(server,center_1,{color:'#00ff00'})
graph.newEdge(server,center_2,{color:'#00ff00'})
graph.newEdge(server,center_3,{color:'#00ff00'})
graph.newEdge(server,center_4,{color:'#00ff00'})
graph.newEdge(server,center_5,{color:'#00ff00'})

graph.newEdge(center_1,farmer_1,{color:'orange'})
graph.newEdge(center_1,farmer_2,{color:'orange'})
graph.newEdge(center_1,farmer_3,{color:'orange'})
graph.newEdge(center_2,farmer_4,{color:'orange'})
graph.newEdge(center_2,farmer_5,{color:'orange'})
graph.newEdge(center_2,farmer_6,{color:'orange'})
graph.newEdge(center_3,farmer_7,{color:'orange'})
graph.newEdge(center_3,farmer_8,{color:'orange'})
graph.newEdge(center_3,farmer_9,{color:'orange'})
graph.newEdge(center_4,farmer_10,{color:'orange'})
graph.newEdge(center_4,farmer_11,{color:'orange'})
graph.newEdge(center_4,farmer_12,{color:'orange'})
graph.newEdge(center_5,farmer_13,{color:'orange'})
graph.newEdge(center_5,farmer_14,{color:'orange'})
graph.newEdge(center_5,farmer_15,{color:'orange'})


graph.newEdge(farmer_1,farm_1,{color:'#0000ff'})
graph.newEdge(farmer_1,farm_2,{color:'#0000ff'})
graph.newEdge(farmer_1,farm_3,{color:'#0000ff'})
graph.newEdge(farmer_2,farm_4,{color:'#0000ff'})
graph.newEdge(farmer_2,farm_5,{color:'#0000ff'})
graph.newEdge(farmer_2,farm_6,{color:'#0000ff'})
graph.newEdge(farmer_3,farm_7,{color:'#0000ff'})
graph.newEdge(farmer_3,farm_8,{color:'#0000ff'})
graph.newEdge(farmer_3,farm_9,{color:'#0000ff'})
graph.newEdge(farmer_4,farm_10,{color:'#0000ff'})
graph.newEdge(farmer_4,farm_11,{color:'#0000ff'})
graph.newEdge(farmer_4,farm_12,{color:'#0000ff'})
graph.newEdge(farmer_5,farm_13,{color:'#0000ff'})
graph.newEdge(farmer_5,farm_14,{color:'#0000ff'})
graph.newEdge(farmer_5,farm_15,{color:'#0000ff'})

graph.newEdge(farmer_1,warehouse_1,{color:'#ff0000'})
graph.newEdge(farmer_1,warehouse_2,{color:'#ff0000'})
graph.newEdge(farmer_1,warehouse_3,{color:'#ff0000'})
graph.newEdge(farmer_2,warehouse_4,{color:'#ff0000'})
graph.newEdge(farmer_2,warehouse_5,{color:'#ff0000'})
graph.newEdge(farmer_2,warehouse_6,{color:'#ff0000'})
graph.newEdge(farmer_3,warehouse_7,{color:'#ff0000'})
graph.newEdge(farmer_3,warehouse_8,{color:'#ff0000'})
graph.newEdge(farmer_3,warehouse_9,{color:'#ff0000'})
graph.newEdge(farmer_4,warehouse_10,{color:'#ff0000'})
graph.newEdge(farmer_4,warehouse_11,{color:'#ff0000'})
graph.newEdge(farmer_4,warehouse_12,{color:'#ff0000'})
graph.newEdge(farmer_5,warehouse_13,{color:'#ff0000'})
graph.newEdge(farmer_5,warehouse_14,{color:'#ff0000'})
graph.newEdge(farmer_5,warehouse_15,{color:'#ff0000'})

graph.newEdge(center_1,center_5,{color: '#ff00ff'})
graph.newEdge(center_2,center_1,{color: '#ff00ff'})
graph.newEdge(center_3,center_2,{color: '#ff00ff'})
graph.newEdge(center_4,center_3,{color: '#ff00ff'})
graph.newEdge(center_5,center_4,{color: '#ff00ff'})

function callapi(){
    fetch("http://127.0.0.1:8000/transaction/DefCentreView");
    var centre = document.getElementById("c3");
    centre.className += "alert alert-danger";
    document.getElementById("c1").className = "alert alert-primary";
}
document.getElementById("myBtn").addEventListener("click", callapi);


jQuery(function () {
    var springy = window.springy = jQuery('#springydemo').springy({
        graph: graph,
        nodeSelected: function (node) {
            console.log('Node selected: ' + JSON.stringify(node.data));
        }
    });



    var demo = document.querySelector('#springydemo')
    demo.setAttribute('width', window.innerWidth-300)
    demo.setAttribute('height', window.innerHeight-200)
});


// var timer =document.querySelector('#timer')
// var time = 30
// setInterval(() => {
//     if(time==0){
//         window.location=window.location;
//     }
//     time-=1
//     timer.innerHTML=String(time)+'s'
//     console.log(time)
// }, 1000);
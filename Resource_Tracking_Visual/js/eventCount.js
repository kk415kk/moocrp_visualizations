/**
 * Created by Sven Charleer @ KU Leuven on 30/07/14.
 */



var eventCount = function(){


    // properties
    var _content;
    var id;


    var drawGraph = function(data,div)
    {




        var xf = crossfilter(data);
        var byEvents = xf.dimension(function(f){

            return f.object_name;
        });



        var es = byEvents.group().top(Infinity);

        var minp = 0;
        var maxp = 360;

        var minv = Math.log(es[es.length-1].value);
        var maxv = Math.log(es[0].value);

        var scale = (maxv-minv) / (maxp-minp);


        es.forEach(
            function(e) {


                var amount = Math.exp(Math.log(e.value)-minv) / scale + minp;
                var arc0 = d3.svg.arc()
                    .innerRadius(4)
                    .outerRadius(8)
                    .startAngle(0 )
                    .endAngle( amount * (Math.PI/180)) ;
                var svg = d3.select(div)
                    .append("svg")
                    .attr("id", id )
                    .attr("width", 30)   // <-- Here
                    .attr("height", 30); // <-- and here!
                svg.append("circle")
                    .attr("r", 8)
                    .attr("cx", 10)
                    .attr("cy", 10)
                    .attr("fill","#4b4a4b")
                    .append("title")
                    .text(e.key);
                svg.append("path")
                    .attr("d", arc0)
                    .attr("transform", "translate("+10+","+10+")")
                    .attr("fill","#33CCFF")
                    .append("title")
                    .text(e.key);
                svg.append("text")
                    .attr("x", 10)
                    .attr("y", 27)

                    .attr("fill","#33CCFF")
                    .text(e.value)
                    .append("title")
                    .text(e.key);


            });


    }

    return {

        "init" : function(data, identifier, div, contentDiv)
        {

            id = identifier;
            _content = contentDiv;

            drawGraph(data,div);

        },


    }
};



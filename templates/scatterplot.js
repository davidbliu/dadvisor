var x = d3.scale.linear()
     .domain([d3.min(dataset_times), d3.max(dataset_times)])
     .range([0, w])
var y = d3.scale.linear()
     .domain([d3.min(dataset_stats), d3.max(dataset_stats)])
     .range([0, h])

     	//Create SVG element
var svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);
svg.selectAll("circle")
   .data(dataset)
   .enter()
   .append("circle")
	   .attr("cx", function(d) {
	        return x(d.timestamp);
	   })
	   .attr("cy", function(d) {
	        return y(d.stat);
	   })
	   .attr("r", 5);
}
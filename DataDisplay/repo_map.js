function nodeLabel(d) {
    if (d.type == "dir") {
        return d.file;
    }
    else {
        return "";
    }
}

function circleSize(d) {
    if (d.type == "dir") {
        return 5;
    }
    else {
        var size = d.lines / 2;
        if (size < 3) {
            return 3;
        }
        else if (size > 40) {
            return 40;
        }
        else {
            return size;
        }
    }
}

function circleColour(d) {
    if (d.type == "dir") {
        return "blue";
    }
    else {
        return colours(d.commits);
    }
}

function linkDistance(d) {
    return 80;
}

var colours = d3.scaleQuantize()
    .domain([0, 20])
    .range(["#696969", "#808080", "#A9A9A9", "#C0C0C0", "#ffefef",
        "#ffe5e5", "#ffb2b2", "#ff7f7f", "#ff4c4c", "#ff3232c", "#ff0000"]);

//create somewhere to put the force directed graph
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");


d3.json("https://matthew-d-ng.github.io/files.json",
    function (nerror, ndata) {
        if (nerror)
            throw nerror;
        var nodes_data = ndata;

        d3.json("https://matthew-d-ng.github.io/links.json",
            function (lerror, ldata) {
                if (lerror)
                    throw lerror;

                var links_data = ldata;

                var link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(links_data)
                    .enter().append("line")
                    .attr("stroke-width", function (d) { return Math.sqrt(d.value); });

                var node = svg.append("g")
                    .attr("class", "nodes")
                    .selectAll("g")
                    .data(nodes_data)
                    .enter()
                    .append("g");

                var tip;
                svg.on("click", function () {
                    if (tip) tip.remove();
                });

                var circle = node
                    .append("circle")
                    .attr("r", circleSize)
                    .attr("fill", circleColour)
                    .on("mouseover", fade(0.4))
                    .on("mouseout", fade(1))
                    .on("click", function (d) {
                        d3.event.stopPropagation();
                        if (d.type != "dir") {
                            if (tip) tip.remove();

                            tip = svg.append("g")
                                .attr("transform", "translate(" + d.x + "," + d.y + ")");

                            var rect = tip.append("rect")
                                .style("fill", "white")
                                .style("stroke", "steelblue");

                            tip.append("text")
                                .text("Name: " + d.file)
                                .attr("dy", "1em")
                                .attr("x", 5);

                            tip.append("text")
                                .text("Commits: " + d.commits)
                                .attr("dy", "2em")
                                .attr("x", 5);

                            tip.append("text")
                                .text("Code churn: " + Math.floor(d.churn) + "%")
                                .attr("dy", "3em")
                                .attr("x", 5);

                            tip.append("text")
                                .text(" Disclaimer: code churn >100% means they deleted other people's code ")
                                .attr("dy", "5em")
                                .attr("x", 5);

                            var count = 7;
                            d.authors.forEach(function (d) {
                                tip.append("text")
                                    .text("Author: " + d[0] + ", Churn: " + Math.floor(d[1]) + "%")
                                    .attr("dy", count + "em")
                                    .attr("x", 5);
                                count++;
                            });

                            var bbox = tip.node().getBBox();
                            rect.attr("width", bbox.width + 5)
                                .attr("height", bbox.height + 5);
                        }
                    });

                var lables = node.append("text")
                    .text(nodeLabel)
                    .attr('x', 10)
                    .attr('y', 6)
                    .style("font-family", "monospace")
                    .style('fill', ' #0d0d0d');

                node.append("title")
                    .text(function (d) { return d.file; });

                function tickActions() {
                    node
                        .attr("transform", function (d) {
                            return "translate(" + d.x + "," + d.y + ")";
                        })

                    link
                        .attr("x1", function (d) { return d.source.x; })
                        .attr("y1", function (d) { return d.source.y; })
                        .attr("x2", function (d) { return d.target.x; })
                        .attr("y2", function (d) { return d.target.y; });
                }

                var link_force = d3.forceLink(links_data)
                    .id(function (d) { return d.file; })
                    .distance(linkDistance)
                    .strength(0.5);

                var simulation = d3.forceSimulation()
                    .nodes(nodes_data)
                    .force("charge_force", d3.forceManyBody())
                    .force("center_force", d3.forceCenter(width / 2, height / 2))
                    .force('collision', d3.forceCollide().radius(function (d) {
                        return d.radius
                    }))
                    .force("links", link_force)
                    .on("tick", tickActions);

                var drag_handler = d3.drag()
                    .on("start", drag_start)
                    .on("drag", drag_drag)
                    .on("end", drag_end);

                function drag_start(d) {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function drag_drag(d) {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }

                function drag_end(d) {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }

                // build a dictionary of nodes that are linked
                var linkedByIndex = {};
                links_data.forEach(function (d) {
                    linkedByIndex[d.source.file + "," + d.target.file] = 1;
                });

                // check the dictionary to see if nodes are linked
                function isConnected(a, b) {
                    return linkedByIndex[a.file + "," + b.file] || linkedByIndex[b.file + "," + a.file]
                        || a.file == b.file;
                }

                // fade nodes on hover
                function fade(opacity) {
                    return function (d) {
                        // check all other nodes to see if they're connected
                        // to this one. if so, keep the opacity at 1, otherwise
                        // fade
                        node.style("stroke-opacity", function (o) {
                            thisOpacity = isConnected(d, o) ? 1 : opacity;
                            return thisOpacity;
                        });
                        node.style("fill-opacity", function (o) {
                            thisOpacity = isConnected(d, o) ? 1 : opacity;
                            return thisOpacity;
                        });
                    };
                }

                drag_handler(node);

            });
    });

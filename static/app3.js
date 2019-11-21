// function init() {
// 	// console.log("init");
// 	// d3.event.preventDefault();
// 	d3.select("h3").html("* US EXPORT FLOW SUMMARY AND TOP 10 PRODUCT *");
// 	var tbody = d3.select("tbody");
// 	d3.json("/summary_edata", function(details) {
// 		// console.log(details);
// 		var tbody1 = d3.select("tbody");
// 		tbody1.html("");
// 		tbody1
// 		.selectAll("tr")
// 		.data(details)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `<td>${d.Country}</td><td>${d.MS17}</td><td>${d.MS18}</td><td>${d.MSChange}</td><td>${d.Value2018}</td><td>${d.Value2018}</td>`;
// 		});
// 		});

// 	// var bedata1 = "apple";
// 	var url1 = "/bar_edata";
// 	// console.log(url);
// 	// d3.json(url).then((data) => {
// 	Plotly.d3.json(url1,function(error,response){
// 		if(error) console.warn(error);
// 	// Plotly.deleteTraces('bplot', 0);
// 	// d3.json("/bar_edata/"+bedata).then(function(data) {
// 	console.log(response);
// 	var trace1 = {
// 		x:response.bproduct,
// 		y:response.bvalue,
// 		// text:response.bcountry,
// 		type: "bar"
// 		};

// 	// console.log(response)
// // var data = [trace1];

// 	var data1 = [trace1];

// 	// var layout = { margin: { t: 30, b: 100 } };
// 	var layout1 = {
// 		title: "$Value2018",
// 		margin: {
// 		l: 40,
// 		r: 10,
// 		b: 50,
// 		t: 80,
// 		pad: 0
// 			},
// 		// xaxis: {title: "Product"},
// 		// yaxis: {title: "Value2018"},	
// 		};
// 	Plotly.plot("bplot", data1, layout1);
	

// 	// Initial Pie Chart
// 	var trace11 = {
// 	values: response.bvalue,
// 	labels: response.bproduct,
// 	type: 'pie'
// 	};

// 	var data11 = [trace11];

// 	var layout11 = {
// 	title: "Pie Chart",
// 	height: 450,
// 	width: 400
// 	};

// 	Plotly.plot("pplot", data11, layout11);

// 	});

// 		// Initial Table 2
// 	d3.json("/top10_edata", function(etop1) {
// 	// console.log(edata);
// 		var tbody11 = d3.select(".col-md-11 tbody");
// 		tbody11.html("");
// 		tbody11
// 		.selectAll("tr")
// 		.data(etop1)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `<td>${d.Product}</td><td>${d.Value2018}</td><td>${d.Share}</td>`;
// 		});
// 		});	

		// Create a map object
var myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
	});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 10,
  id: "mapbox.streets",
  accessToken: "pk.eyJ1IjoiZGlzZGlsbGVyNzIxMTMwIiwiYSI6ImNqd2s3YTBmNjA1MzE0OW1xcGk0em5xYjIifQ.FOinrzjB3Rdkhus3tQoOuA"
	}).addTo(myMap);

// Define a markerSize function that will give each city a different radius based on its population
function markerSize(population) {
  return population / 40;
	}

// Each city object contains the city's name, location and population
var cities = [
  {
    name: "New York",
    location: [40.7128, -74.0059],
    population: 8550405
  },
  {
    name: "Chicago",
    location: [41.8781, -87.6298],
    population: 2720546
  },
  {
    name: "Houston",
    location: [29.7604, -95.3698],
    population: 2296224
  },
  {
    name: "Los Angeles",
    location: [34.0522, -118.2437],
    population: 3971883
  },
  {
    name: "Omaha",
    location: [41.2524, -95.9980],
    population: 446599
  }
];

// Loop through the cities array and create one marker for each city object
for (var i = 0; i < cities.length; i++) {
  L.circle(cities[i].location, {
    fillOpacity: 0.75,
    color: "white",
    fillColor: "purple",
    // Setting our circle's radius equal to the output of our markerSize function
    // This will make our marker's size proportionate to its population
    radius: markerSize(cities[i].population)
 	 }).bindPopup("<h1>" + cities[i].name + "</h1> <hr> <h3>Population: " + cities[i].population + "</h3>").addTo(myMap);
	}
// };
	// var url = `/veggieexp/${veggie}`;
	// console.log(url);
	// d3.json(url, function(veggiesummaries) {
	// 	console.log(veggiesummaries);
	// 	var vegshare = [];
	// 	veggiesummaries.forEach(function(veggiesummary) {
	// 		var color = "";
	// 		if (veggiesummary.Share > 100) {
	// 		color = "pink";
	// 		}
	// 		else if (veggiesummary.Share > 60) {
	// 		color = "blue";
	// 		}
	// 		else if (veggiesummary.Share > 30) {
	// 		color = "green";
	// 		}
	// 		else {
	// 		color = "cyan";
	// 		}
	// 		var locations = [];
	// 		locations.push(veggiesummary.lat , veggiesummary.lon);
	// 		vegshare.push(
	// 			L.circle(locations, {
	// 				stroke: false,
	// 				weight: 1,
	// 				fillOpacity: 0.75,
	// 				color: "white",
	// 				fillColor: color,
	// 				radius: veggiesummary.Share * 10000
	// 			}).bindPopup("<h1>" + veggiesummary.Country + "</h1> <hr> <h3>Shares(%): " + veggiesummary.Share + "</h3>")
	// 		);
	
//     var vegLayer = L.layerGroup(vegshare);
//     console.log(vegLayer);

//     var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//     attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//     maxZoom: 18,
//     id: "mapbox.streets",
//     accessToken: "pk.eyJ1IjoiZGlzZGlsbGVyNzIxMTMwIiwiYSI6ImNqd2s3YTBmNjA1MzE0OW1xcGk0em5xYjIifQ.FOinrzjB3Rdkhus3tQoOuA"
//     });

//     var baseMaps = {
//       "Street Map": streetmap
//     };

//     var overlayMaps = {
//       "Country": vegLayer
//     };

//     var myMap = L.map("map", {
//       center: [
//         37.09, -95.71
//       ],
//       zoom: 1,
//       layers: [streetmap, vegLayer]
//     });

//     L.control.layers(baseMaps, overlayMaps).addTo(myMap);
//     console.log(myMap);
//   // });  
// 	});
//   // Grab a reference to the dropdown select element
// 	var productselector = d3.select("#selDataset");
// 	var typeselector = d3.select("#selDataset2");
// 	var productType = ["Veggie","Fruit"];
// 	productType.forEach(function(type) {
// 		typeselector.append("option").text(type).property("value", type)
// 	});
// 	// Use the list of sample names to populate the select options
// 	d3.json("/veggienames", function(vegNames) {
// 		vegNames.forEach((veg) => {
// 			productselector
// 			.append("option")
// 			.text(veg)
// 			.property("value", veg);
// 	});

// 	// Use the first sample from the list to build the initial plots
// 		var firstVeg = vegNames[0];
// 		console.log(firstVeg);
// 		veggiemaps(firstVeg);
// 	});

// };


// function buildTable2() {
// 	d3.json("/summary_edata", function(ethings) {
// 		// console.log(details);
// 		var tbody2 = d3.select("tbody");
// 		tbody2.html("");
// 		tbody2
// 		.selectAll("tr")
// 		.data(ethings)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `<td>${d.Country}</td><td>${d.MS17}</td><td>${d.MS18}</td><td>${d.MSChange}</td><td>${d.Value2017}</td><td>${d.Value2018}</td>`;
// 		});
// 		});

// }; 

// function buildCharts2() {
// 	// d3.event.preventDefault();
// // var bedata2 = "apple";
// 	var url2 = "/bar_edata";
// 	// console.log(url);
// 	// d3.json(url).then((data) => {
// 	Plotly.d3.json(url2,function(error,response) {
// 		if(error) console.warn(error);
// 	// Plotly.deleteTraces('bplot', 0);
	
// 	// d3.json("/bar_edata/"+bedata).then(function(data) {
// 	// console.log(response);
// 	var trace2 = {
// 		x:response.bproduct,
// 		y:response.bvalue,
// 		// text:response.bcountry,
// 		type: "bar"
// 		};

// // var data = [trace1];

// 	var data2 = [trace2];
// 	// var layout = { margin: { t: 30, b: 100 } };
// 	var layout2 = {
// 		title: "$Value2018",
// 		margin: {
// 		l: 40,
// 		r: 10,
// 		b: 50,
// 		t: 80,
// 		pad: 0
// 			},
// 		// xaxis: {title: "Product"},
// 		// yaxis: {title: "Value2018"},	
// 		};
// 	Plotly.plot("bplot", data2, layout2);
	

// 	//Pie Chart
// 	var trace22 = {
// 	values: response.bvalue,
// 	labels: response.bproduct,
// 	type: 'pie'
// 	};

// 	var data22 = [trace22];

// 	var layout22 = {
// 	title: "Pie Chart",
// 	height: 450,
// 	width: 400
// 	};

// 	Plotly.plot("pplot", data22, layout22);

// 	});
// };

// function buildTable22() {
// 	// d3.event.preventDefault();
// 	d3.json("/top10_edata", function(etop22) {
// 	// console.log(edata);
// 		var tbody22 = d3.select(".col-md-11 tbody");
// 		tbody22.html("");
// 		tbody22
// 		.selectAll("tr")
// 		.data(etop22)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `${d.Product}</td><td>${d.Value2018}</td><td>${d.Share}</td>`;
// 		});
// 	});
// };

// function buildTable3() {
// 	d3.json("/summary_idata",function(ithings) {
// 		console.log(ithings);
// 		var tbody3 = d3.select("tbody");
// 		tbody3.html("");
// 		tbody3
// 		.selectAll("tr")
// 		.data(ithings)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `<td>${d.Country}</td><td>${d.MS17}</td><td>${d.MS18}</td><td>${d.MSChange}</td><td>${d.Value2017}</td><td>${d.Value2018}</td>`;
// 		});
// 		});

// }; 

// function buildCharts3() {
// 	// d3.event.preventDefault();
// 	// var bidata3 = "apple";
// 	var url3 = "/bar_idata";
// 	console.log(url3);
// 	// d3.json(url).then((data) => {
// 	// Plotly.d3.json(url3,function(error,response){
// 	// 	if(error) console.warn(error);
// 	Plotly.d3.json(url3,function(iresponse) {
// 	// Plotly.deleteTraces('bplot', 0);
// 	var trace3 = {
// 		x:iresponse.bproduct,
// 		y:iresponse.bvalue,
// 		type: "bar"
// 		};

// // var data = [trace1];

// 	var data3 = [trace3];
// 	// var layout = { margin: { t: 30, b: 100 } };
// 	var layout3 = {
// 		title: "$Value2018",
// 		margin: {
// 		l: 40,
// 		r: 10,
// 		b: 50,
// 		t: 80,
// 		pad: 0
// 			},
// 		// xaxis: {title: "Product"},
// 		// yaxis: {title: "Value2018"},	
// 		};
// 	Plotly.plot("bplot", data3, layout3);
	

// 	// Initial Pie Chart
// 	var trace33 = {
// 	values:iresponse.bvalue,
// 	labels:iresponse.bproduct,
// 	type: 'pie'
// 	};

// 	var data33 = [trace33];

// 	var layout33 = {
// 	title: "Pie Chart",
// 	height: 450,
// 	width: 400
// 	};

// 	Plotly.plot("pplot", data33, layout33);

// 	});
// };

// function buildTable33() {
// 	d3.json("/top10_idata", function(itop33) {
// 	// console.log(idata);
// 		var tbody33 = d3.select(".col-md-11 tbody");
// 		tbody33.html("");
// 		tbody33
// 		.selectAll("tr")
// 		.data(itop33)
// 		.enter()
// 		.append("tr")
// 		.html(function(d) {
// 		return `<td>${d.Product}</td><td>${d.Value2018}</td><td>${d.Share}</td>`;
// 		});
// 	});
// };


// Choose Flow Direction, Export or Import
// var exportUpdate = d3.select("#click-export");
// exportUpdate.on("click", function() {
// 	Plotly.deleteTraces('bplot', 0);
// 	console.log("exportUpdate");
// 	d3.event.preventDefault();
// 	d3.select("h3").html("US EXPORT FLOW SUMMARY & TOP 10 PRODUCT!");
// 	buildTable2();
// 	buildCharts2();
// 	buildTable22();
// });


// var importUpdate = d3.select("#click-import");

// importUpdate.on("click", function() {
// 	Plotly.deleteTraces('bplot', 0);
// 	console.log("importUpdate");
// 	d3.event.preventDefault();
// 	d3.select("h3").html("US IMPORT FLOW SUMMARY & TOP 10 PRODUCT!");
// 	buildTable3();
// 	buildCharts3();
// 	buildTable33();
// });
// console.log("init")

// Create a veggie map
// function veggiemaps(veggie) {
// 	var url = `/veggieexp/${veggie}`;
// 	console.log(url);
// 	d3.json(url, function(veggiesummaries) {
// 		console.log(veggiesummaries);
// 		var vegshare = [];
// 		veggiesummaries.forEach(function(veggiesummary) {
// 			var color = "";
// 			if (veggiesummary.Share > 100) {
// 			color = "pink";
// 			}
// 			else if (veggiesummary.Share > 60) {
// 			color = "blue";
// 			}
// 			else if (veggiesummary.Share > 30) {
// 			color = "green";
// 			}
// 			else {
// 			color = "cyan";
// 			}
// 			var locations = [];
// 			locations.push(veggiesummary.lat , veggiesummary.lon);
// 			vegshare.push(
// 				L.circle(locations, {
// 					stroke: false,
// 					weight: 1,
// 					fillOpacity: 0.75,
// 					color: "white",
// 					fillColor: color,
// 					radius: veggiesummary.Share * 10000
// 				}).bindPopup("<h1>" + veggiesummary.Country + "</h1> <hr> <h3>Shares(%): " + veggiesummary.Share + "</h3>")
// 			);
// 	});
//     var vegLayer = L.layerGroup(vegshare);
//     console.log(vegLayer);

//     var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//     attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//     maxZoom: 18,
//     id: "mapbox.streets",
//     accessToken: "pk.eyJ1IjoiZGlzZGlsbGVyNzIxMTMwIiwiYSI6ImNqd2s3YTBmNjA1MzE0OW1xcGk0em5xYjIifQ.FOinrzjB3Rdkhus3tQoOuA"
//     });

//     var baseMaps = {
//       "Street Map": streetmap
//     };

//     var overlayMaps = {
//       "Country": vegLayer
//     };

//     var myMap = L.map("map", {
//       center: [
//         37.09, -95.71
//       ],
//       zoom: 1,
//       layers: [streetmap, vegLayer]
//     });

//     L.control.layers(baseMaps, overlayMaps).addTo(myMap);
//     console.log(myMap);
//   });  
// };

// //Switch to Fruit Map
// function fruitmaps(fruit) {
// 	var fruitUrl = `/fruitexp/${fruit}`;
// 	console.log(fruitUrl);
// 	d3.json(fruitUrl, function(fruitsummaries) {
// 		console.log(fruitsummaries);
// 		var fruitshare = [];

// 		fruitsummaries.forEach(function(fruitsummary) {
// 			var color = "";
// 			if (fruitsummary.Share > 100) {
// 			color = "pink";
// 			}
// 			else if (fruitsummary.Share > 60) {
// 			color = "blue";
// 			}
// 			else if (fruitsummary.Share > 30) {
// 			color = "green";
// 			}
// 			else {
// 			color = "cyan";
// 			}
// 			var locations = [];
// 			locations.push(fruitsummary.lat , fruitsummary.lon);
// 			fruitshare.push(
// 				L.circle(locations, {
// 				stroke: false,
// 				weight: 1,
// 				fillOpacity: 0.75,
// 				color: "white",
// 				fillColor: color,
// 				radius: fruitsummary.Share * 10000
// 				}).bindPopup("<h1>" + fruitsummary.Country + "</h1> <hr> <h3>Shares(%): " + fruitsummary.Share + "</h3>")
// 		);
// 		});
//     var fruitLayer = L.layerGroup(fruitshare);
//     console.log(fruitLayer);

//     var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//     attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//     maxZoom: 18,
//     id: "mapbox.streets",
//     accessToken: "pk.eyJ1IjoiZGlzZGlsbGVyNzIxMTMwIiwiYSI6ImNqd2s3YTBmNjA1MzE0OW1xcGk0em5xYjIifQ.FOinrzjB3Rdkhus3tQoOuA"
//     });

//     var baseMaps = {
//       "Street Map": streetmap
//     };

//     var overlayMaps = {
//       "Country": fruitLayer
//     };

//     var myMap = L.map("map", {
//       center: [37.09, -95.71],
//       zoom: 1,
//       layers: [streetmap, fruitLayer]
//     });

//     L.control.layers(baseMaps, overlayMaps).addTo(myMap);
//   	});
  
// };

// // Choose Flow Direction, Export or Import
// var exportUpdate = d3.select("#click-export");
// exportUpdate.on("click", function() {
// 	Plotly.deleteTraces('bplot', 0);
// 	console.log("exportUpdate");
// 	d3.event.preventDefault();
// 	d3.select("h3").html("US EXPORT FLOW SUMMARY & TOP 10 PRODUCT!");
// 	buildTable2();
// 	buildCharts2();
// 	buildTable22();
// });


// var importUpdate = d3.select("#click-import");

// importUpdate.on("click", function() {
// 	Plotly.deleteTraces('bplot', 0);
// 	console.log("importUpdate");
// 	d3.event.preventDefault();
// 	d3.select("h3").html("US IMPORT FLOW SUMMARY & TOP 10 PRODUCT!");
// 	buildTable3();
// 	buildCharts3();
// 	buildTable33();
// });
// // console.log("init")

// //Choose the type of products: Fruit or vegetable.
// function getValue(value) {
// 	map.remove();
// 	var mapCreate = d3.select(".col-md-10");
// 	mapCreate.append("div").property("id","map");
// 	d3.select("#selDataset").html("");

// 	if (value == "Fruit") {
// 		var fruitSelect = d3.select("#selDataset");
// 		d3.json("/fruitnames", function(fruitName) {
// 			fruitName.forEach((fruit) => {
// 				fruitSelect.append("option").text(fruit).property("value", fruit);
// 			});
// 			var firstFruit = fruitName[0];
// 			console.log(firstFruit);
// 			fruitmaps(firstFruit);
// 		});
// 	}
// 	else {
// 		var vegSelect = d3.select("#selDataset");
// 		d3.json("/veggienames", function(vegetable) {
// 			vegetable.forEach((veg) => {
// 				vegSelect.append("option").text(veg).property("value", veg);
// 			});
// 			var secondVeg = vegetable[0];
// 			veggiemaps(secondVeg);
// 		});
// 	}
// };

// //Switch to the other fruits or vegetables
// function optionChanged(NewOption) {
// 	map.remove();
// 	var mapCreate = d3.select(".col-md-10");
// 	mapCreate.append("div").property("id","map");
// 	d3.json("/veggienames", function(items) {
// 		console.log(items);
// 		var count = 0;
// 		items.forEach(function(item) {
// 			if(item == NewOption) {
// 			count += 1;
// 			}
// 		});
// 		if (count == 1) {
// 		  veggiemaps(NewOption);
// 		}
// 		else {
// 		  fruitmaps(NewOption);
// 		}
// 	});   
// };


// init();
  
// //initiation
// function mapinit() {
//   // Grab a reference to the dropdown select element
// 	var productselector = d3.select("#selDataset");
// 	var typeselector = d3.select("#selDataset2");
// 	var productType = ["Veggie","Fruit"];
// 	productType.forEach(function(type) {
// 	typeselector.append("option").text(type).property("value", type)
// 	});
// 	// Use the list of sample names to populate the select options
// 	d3.json("/veggienames", function(vegNames) {
// 	vegNames.forEach((veg) => {
// 	productselector
// 	.append("option")
// 	.text(veg)
// 	.property("value", veg);
// 	});

// 	// Use the first sample from the list to build the initial plots
// 	var firstVeg = vegNames[0];
// 	console.log(firstVeg);
// 	veggiemaps(firstVeg);
// 	});
// };
// mapinit();











// function getButton() {
//   // Fetch new data each time a new sample is selected
//   if(value == "dataset1") {
//   	var exportSelect = d3.select("#click-export");
// 		console.log(Export);
// 		buildTable1(Export);
// 		buildCharts(Export);
// 		buildTable2(Export);
//   };

//   else(value =="dataset2") {
//   	var importSelect = d3.select("#click-import");

//   		console.log(Import);
//   		buildTable1(Import);
//   		buildCharts(Import);
//   		buildTable2(Import);
//   };
  

// };



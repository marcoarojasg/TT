function ConsumirAPI(){

    const endPoint = "https://restcountries.com/v3.1/all"
    fetch(endPoint)
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        var pais = [];
        var poblacion = [];
        var colores = [];

        data.forEach(element => {

            if (element.continents == "Asia" || element.continents == "South America" || element.continents == "Europe") {
                pais.push(element.name.common);
                poblacion.push(element.population);

                if (element.continents == "Asia") {
                    colores.push("blue");
                } else if (element.continents == "South America") {
                    colores.push("green");
                } else if (element.continents == "Europe") {
                    colores.push("red");
                }
            }
            console.log(element.continents)
        });
        var grafica = [
            {
                x: pais,
                y: poblacion,
                type: "bar",
                marker: {
                    color: colores
                },

            }
        ];
        var layout = {
            title: "POBLACIÓN POR PAÍS", 
            xaxis: {
                title: "País"
            },
            yaxis: {
                title: "Población"
            },

        };
        Plotly.newPlot('myDiv', grafica, layout);
    })
    .catch(function(error){
        console.log("Error: ", error);
    });

}
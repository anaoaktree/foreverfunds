var fundsService = {
tableNames: [],
createAllocationTable: function(tableName, csvString) {
    this.tableNames.push(tableName);
    var tabulate = function (data, columns) {
      var table = d3.select('#'+tableName)
        var thead = table.append('thead')
        var tbody = table.append('tbody')

        thead.append('tr')
          .selectAll('th')
            .data(columns)
            .enter()
          .append('th')
            .text(function (d) { return d })

        var rows = tbody.selectAll('tr')
            .data(data)
            .enter()
          .append('tr')

        var cells = rows.selectAll('td')
            .data(function(row) {
                return columns.map(function (column) {
                    return { column: column, value: row[column] }
              })
          })
          .enter()
        .append('td')
          .text(function (d) { return d.value })

      return table;
    }

    d3.csv.parse(csvString, function (data) {
        var columns = [''].concat(Object.keys(data[0]));
      tabulate(data,columns)
       $('#' + tableName).DataTable({
        "searching": false,
         responsive: true,
        'paging':true});
    })

    }

}


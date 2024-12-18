/**
 *
 * @param data:Array
 */
function csvmaker(data, headers=["Dirección IP", "Nombre de Host"]){

    const csvRows = []

    // get the headers
    csvRows.push(headers.join(','))

    for (const row of data){
        const values = Object.values(row).join(',')
        csvRows.push(values)
    }
    
    return csvRows.join('\n')
}
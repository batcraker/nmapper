/**
 *
 * @param data:Array
 */
function csvmaker(data){

    const csvRows = []

    // get the headers
    const headers = ["IP", "Hostname"]
    csvRows.push(headers.join(','))

    for (const row of data){
        const values = Object.values(row).join(',')
        csvRows.push(values)
    }

    return csvRows.join('\n')
}
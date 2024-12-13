function download(data, filename){

    const blob = new Blob([data], {type: 'text/csv'})

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href=url
    a.download = filename + ".csv"

    a.click()
}
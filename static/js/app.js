const form = document.getElementById("upload-form");
const uploadedFiles = document.getElementById('uploaded-files');
const btnDelete = document.querySelectorAll('.delete')

const inputFile = document.getElementById("file")
const fileLabel = document.getElementById("file-label");

const BASE_URL = window.location.origin

function alertSuccess(message){
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: message,
        showConfirmButton: false,
        timer: 3000
    })
}

inputFile.addEventListener("change", (e)=> {
    fileLabel.innerHTML = e.target.files[0].name
})

// form.addEventListener("submit",(e)=> {
//     e.preventDefault()
    
//     if(inputFile.files.length === 0){
//         alert("Selecciona un archivo")
//         return
//     }
    
//     form.submit()
// })

for(let i=0; i<btnDelete.length; i++){
    btnDelete[i].addEventListener("click", ()=> {
        let confirmation = confirm('Deseas eliminar el archivo?')
        if(confirmation){
            let fileId = btnDelete[i].getAttribute("data-fileid")
            

            fetch(`${BASE_URL}/nmapper/file/${fileId}`, {
                method:"DELETE"
            })
                .then(res => res.json())
                .then(res => {
                    window.location.reload()
                })
                .catch(err => {
                    console.log(err);
                })
        }

    })
}
const form = document.getElementById("upload-form");
const uploadedFiles = document.getElementById('uploaded-files');
const btnDelete = document.querySelectorAll('.delete')

const inputFile = document.getElementById("file")
const fileLabel = document.getElementById("file-label");

const BASE_URL = window.location.origin


inputFile.addEventListener("change", (e)=> {
    fileLabel.innerHTML = e.target.files[0].name
})

form.addEventListener("submit",(e)=> {
    e.preventDefault()
    
    const file = inputFile.files[0]

    const formData = new FormData()
    formData.append('file',file)

    fetch(`${BASE_URL}/api/nmapper`,{
        method:"POST",
        body: formData
    }).then(res => res.json())
    .then(res => {
        alert(res.message)
        form.reset()
        window.location.reload()
        
    })
    .catch(err => {
        alert("No se ha podido cargar el archivo") 
    })
    
})

for(let i=0; i<btnDelete.length; i++){
    btnDelete[i].addEventListener("click", ()=> {
        let confirmation = confirm('Deseas eliminar el archivo?')
        if(confirmation){
            let fileId = btnDelete[i].getAttribute("data-fileid")
            

            fetch(`${BASE_URL}/api/${fileId}`, {
                method:"DELETE"
            })
                .then(res => res.json())
                .then(res => {
                    alert("Eliminado")
                    window.location.reload()
                })
                .catch(err => {
                    console.log(err);
                })


        }else{
            return
        }

    })
}
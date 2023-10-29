const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file; 


button.onclick = ()=>{
  input.click(); 
}

input.addEventListener("change", function(){
  
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); 
});



dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); 
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});


dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});


dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); 
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile(file) {
  let fileType = file.type; // Get the selected file type
  let validExtensions = ["application/pdf"]; // Add the valid PDF extension to the array

  if (validExtensions.includes(fileType)) { // Check if the user-selected file is a PDF
    let fileReader = new FileReader(); // Create a new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; // Store the user-selected file source in the fileURL variable

      // You can modify this part to display a link to the PDF instead of an image
      let pdfLink = `<a href="${fileURL}" target="_blank">Open PDF</a>`; // Create a link to the PDF
      dropArea.innerHTML = pdfLink; // Add the link inside the dropArea container
      
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not a PDF File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload PDF";
  }
}
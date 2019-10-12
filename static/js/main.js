// const formSubmit = async () => {
//   const response = await fetch("http://localhost:5000/api/encryptVideo", {
//     method: "POST",
//     body: document.getElementById("verify").value,
//     headers: {
//       "Content-Type": "multipart/form-data"
//     }
//   });
//   const json = await response.json()
//   var downloadLink = document.createElement("a")
//   downloadLink.href = json["link"]
//   downloadLink.text = "Download"
//   document.body.appendChild(downloadLink)
// }

// function createLink(link) {
//   var paragraph = document.getElementById("paragraph")
//   var a = document.createElement("a")
//   a.href = link
//   a.innerHTML = "Link"
//   paragraph.appendChild(a)
// }

// const submitForm = async (e) => {
//   // e.preventDefault();
//   console.log("hello")
//   var formData = new FormData(document.getElementById("myForm"))
//   console.log(formData)
//   // formData.append("verify", document.getElementById("verify").value)
//   const response = await fetch("/api/encryptVideo", {
//     method: "POST",
//     body: formData
//   });
//   const json = await response.json()
//   console.log(response)
//   console.log(json)
//   createLink(json["link"])
// }

const submitEncryptForm = async () => {
  var container = document.getElementById("encryptDownloadArea")
  removeChildElements(container)
  createSpinner(container)
  var formData = new FormData(document.getElementById("encryptForm"))
  const response = await fetch("/api/encryptVideo", {
    method: "POST",
    body: formData
  });
  const json = await response.json()
  removeChildElements(container)
  var a = document.createElement("a")
  a.href = json["link"]
  a.innerHTML = "Encrypted Video Download"
  container.appendChild(a)
}



function createSpinner(container) {
  var spinner = document.createElement("i")
  spinner.className = "fa fa-spinner w3-spin"
  spinner.style = "font-size:64px"
  container.appendChild(spinner)
}

function removeChildElements(container) {
  while (container.firstChild) {
    container.removeChild(container.firstChild)
  }
}

const submitVerifyForm = async () => {
  var container = document.getElementById("verifyDownloadArea")
  removeChildElements(container)
  createSpinner(container)
  var formData = new FormData(document.getElementById("verifyForm"))
  const response = await fetch("/api/verifyVideo", {
    method: "POST",
    body: formData
  });
  const json = await response.json()
  removeChildElements(container)
  showVerificationResult(container, json["result"])
}

function showVerificationResult(container, result) {
  if (result) {
    var checkmark = document.createElement('i')
    checkmark.className = "fa fa-check"
    checkmark.style = "font-size:64px"
    container.appendChild(checkmark)
  }
  else {
    var xmark = document.createElement('i')
    xmark.className = "fa fa-times"
    xmark.style = "font-size:64px"
    container.appendChild(xmark)
  }
}
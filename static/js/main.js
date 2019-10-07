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
  var formData = new FormData(document.getElementById("encryptForm"))
  const response = await fetch("/api/encryptVideo", {
    method: "POST",
    body: formData
  });
  const json = await response.json()
  var container = document.getElementById("encryptContainer")
  var a = document.createElement("a")
  a.href = json["link"]
  a.innerHTML = "Encrypted Video Download"
  container.appendChild(a)
}

const submitVerifyForm = async () => {
  var formData = new FormData(document.getElementById("verifyForm"))
  const response = await fetch("/api/verifyVideo", {
    method: "POST",
    body: formData
  });
  const json = await response.json()
  var container = document.getElementById("verifyContainer")
  var a = document.createElement("label")
  a.innerHTML = String(json["result"])
  container.appendChild(a)
}
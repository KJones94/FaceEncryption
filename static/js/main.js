const formSubmit = async () => {
  const response = await fetch("http://localhost:5000/api/encryptVideo", {
    method: "POST",
    body: document.getElementById("verify").value
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
  const json = await response.json()
  var downloadLink = document.createElement("a")
  downloadLink.href = json["link"]
  downloadLink.text = "Download"
  document.body.appendChild(downloadLink)
}
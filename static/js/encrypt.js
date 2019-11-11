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
  if (result === 2) {
    var question = document.createElement('i')
    question.className = "fa fa-question"
    question.style = "font-size:64px"
    container.appendChild(question)
  }
  else if (result === 1) {
    var checkmark = document.createElement('i')
    checkmark.className = "fa fa-check"
    checkmark.style = "font-size:64px"
    container.appendChild(checkmark)
  }
  else if (result === 0) {
    var xmark = document.createElement('i')
    xmark.className = "fa fa-times"
    xmark.style = "font-size:64px"
    container.appendChild(xmark)
  }
}
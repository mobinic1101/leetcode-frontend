console.log("problem.js loaded");



let container = document.getElementById("container");
// result_button
let testResultDetail = document.createElement("p")
let resultButton = document.createElement("button");
resultButton.classList.add("btn");
resultButton.classList.add("btn-outline-secondary");
resultButton.style.display = "flex";
resultButton.style.marginTop = "2%";
resultButton.style.width = "100%";
resultButton.addEventListener("click", (e) => {
  container.append(testResultDetail)
})

document.getElementById("file-form").addEventListener("submit", (e) => {
  e.preventDefault();
  let submitButton = document.getElementById("file-form-submit-btn");
  let python_file = document.getElementById("file").files[0];

  if (!python_file) {
    alert("Please select a file first");
    return; // Stop execution here
  }
  if (!python_file.name.endsWith(".py")) {
    alert("Please select a Python(<filename>.py) file");
    return; // Stop execution here
  }

  // Only if both checks pass, proceed with the fetch:
  submitButton.disabled = true;
  submitButton.innerText = "Uploading, please wait...";

  let formData = new FormData();
  formData.append("python_file", python_file);

  let code_running_url = document.getElementById("file-form").action;
  fetch(code_running_url, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
        if (!response.ok) {
          response.json().then(data => {
            resultButton.classList.replace('btn-outline-secondary', 'btn-outline-danger')
            resultButton.innerHTML = data.detail
            container.append(resultButton)
            return
          })
        }
        else if (response.ok) {
          response.json().then(data=> {
            resultButton.innerHTML = data.message + "please wait..."
            let executionId = document.createElement("p").innerHTML = "execution_id: " + data.execution_id
            container.append(resultButton, executionId)
            setTimeout(() => {
                let code_result_url = document.getElementById("file-form").dataset.codeResultUrl + data.execution_id + "/";
                console.log("code_result_url: ", code_result_url)
                fetch(code_result_url, {
                  method: 'GET',
                  credentials: 'include'
                })
                .then(response => {
                  switch (response.status) {
                    case 404:
                      resultButton.innerHTML = "Error: Timeout exceed"
                      return
                    case 422:
                      resultButton.innerHTML = "Error"
                    case 200:
                      // switch the resultButton to green or red depending on data.all_passed
                      // assign an event listener to button to bring the user to test_result page and show them their test result.
                      // display failed ones with red and success ones with green.
                      response.json().then(data=>{
                        testResultDetail.innerHTML = JSON.stringify(data["testcase_compare_result"], null, 4)
                        if (data["all_passed"]) {
                          resultButton.classList.replace('btn-outline-secondary', 'btn-outline-success')
                          resultButton.innerHTML = "All testcases passed! show in detail"
                          return


                        } else {
                          resultButton.classList.replace('btn-outline-secondary', 'btn-outline-danger')
                          resultButton.innerHTML = "Some testcases failed show in detail"
                          return
                        }
                      })
                  }
                })
                .catch(error => {
                  resultButton.innerHTML = "sorry: An error occurred."
                })
                
            }, 5000);

          })

}})

    .catch((error) => {
      console.error("Error:", error);
      window.alert("An error occurred: " + error.message);
    })
    .finally(() => {
      submitButton.disabled = false;
      submitButton.innerText = "Submit";
    });
});

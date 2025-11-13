//For homepage
const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

const submitBtn = document.getElementById("submitdata");
submitBtn.addEventListener("click", btnHandler);

function btnHandler(event){
    event.preventDefault();
    
    const form = document.getElementById("inpform");
    const data = Array.from(form.elements);

    // console.log(data[0].value);
    // data.forEach(elements => {
    //     console.log(elements.value);
    // });

    params = JSON.stringify({
        "name":data[0].value,
        "phone":data[1].value,
        "email":data[2].value,
        "city":data[3].value,
        "state":data[4].value,
        "country":data[5].value,
        "pincode":data[6].value,
    });

    const xhr = new XMLHttpRequest();

    xhr.open("POST", "pathtosubmit/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrf);

    xhr.onload = function (){
        if(this.status == 200){
            alert("Your form has been submitted");
        }
        else{
            console.log(this.responseText);
        }
    }

    xhr.send(params);
}
const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

//Event delegation
const tblParent = document.querySelector(".tableDiv");

//Edit
tblParent.addEventListener("click", (e) => {
    if(e.target.classList.contains("editIcon")){
        console.log("Edit", e.target.dataset.id);
    }
});

//Delete
tblParent.addEventListener("click", (e) => {
    if(e.target.classList.contains("deleteIcon")){
        let id = e.target.dataset.id;
        deleteRequest(id);
    }
});


function deleteRequest(id){
    console.log(csrf);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/action/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrf);

    xhr.onload = function (){
        console.log(this.responseText);
        alert("Request sent");
    }

    params = JSON.stringify({
        "action":"delete",
        "id":id
    });

    xhr.send(params);
}

//Pop up box
const popVal = 0;   //0 hide, 1 show


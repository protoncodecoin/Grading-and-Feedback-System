// after the DOMContent event has been fired
document.addEventListener("DOMContentLoaded", async function(){

    // dom elements
    const studentSelectEl = document.querySelector("#student")
    
    // get list of unsupervisied students from the api
    const response = await getUserData("unsupervised_students");
    
    // create option ele and insert into the studentSelectEl
    const optionsHtml = response.length > 0 ? response.map((el) => {
        return `<option value="${el.id}">${el.first_name} ${el.last_name}</option>`
    }).join("") : 0;

    // insert created elements into the dom
    if(optionsHtml === 0){
        studentSelectEl.previousElementSibling.innerHTML = "<p>All students have been assigned";

        // disable assign button
        document.querySelector("#assign-btn").disabled = true;

    }else {
        studentSelectEl.insertAdjacentHTML("afterbegin", optionsHtml)
    }
    
    
    // get list of supervisors from the api
    const supervisorSelectEl = document.querySelector("#supervisor");
    const supervisors_response = await getUserData("supervisor");

    const supervisorOptionsHtml = supervisors_response.length > 0 ? supervisors_response.map((el) => {
        return `<option value="${el.id}">${el.full_name}</option>`
    }).join("") : 0;

    // insert created elements into the dom
    supervisorOptionsHtml === 0 ? supervisorOptionsHtml.innerHTML = "No supervisors available" : supervisorSelectEl.insertAdjacentHTML("afterbegin", supervisorOptionsHtml)   
})


/**
 * 
 * @param { String } endpoint Type of user to get from api
 * @returns An array of unsupervisied student objects from the api
 */
const getUserData = async (endpoint) => {
    
    try {
        const response = await fetch(`/api/${endpoint}/`);

        if (!response.ok){
            throw new Error(response)
        }

        const data = await response.json()

        console.log(data)

        return data;
        
    } catch (error) {
        // show error message
        console.log(error)
    }
}


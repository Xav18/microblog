function toggleLike(post_id){
    var button = document.getElementById(post_id).firstChild.nextSibling
    var likes = document.getElementById(post_id).lastChild.previousSibling
    action = button.innerHTML.toString().toLowerCase().trim()
    console.log(action)
    
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");

    //appel à la fonction postJson par ici
    console.log(action)
    // try {
      const response = fetch("http://localhost:5000/"+action+"/"+post_id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }).then(function(response) {
        console.log("passe la ???");
        const result = response.json();
        console.log(result)
        console.log("Success:", result);
        if (action=="like"){
          button.innerHTML="Unlike";
          likes.innerHTML++;
        }
        else{
          button.innerHTML="Like";
          likes.innerHTML--;
        }
      })

    .catch (function(error) {
      console.error("Error:", error);
    })
      
    //   const data = { username: "example" };
    //   console.log(postJSON(data));

  }

  // async function postJSON(post_id, action) {

  // }

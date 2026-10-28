let data = [];

fetch("data/tree.json")
.then(r=>r.json())
.then(x=>{

   data = x;

   render(x);

});

function render(rows){

   const root =
   document.getElementById(
     "tree"
   );

   root.innerHTML = "";

   rows.forEach(row=>{

      const div =
        document.createElement(
          "div"
        );

      div.className =
        "item";

      div.style.marginLeft =
        (row.level * 20)
        + "px";

      div.textContent =
        row.code
        + " "
        + row.title;

      div.onclick=()=>{

         document
         .getElementById(
          "code"
         )
         .innerText =
         row.code;

         document
         .getElementById(
          "title"
         )
         .innerText =
         row.title;

         document
         .getElementById(
          "fterm"
         )
         .innerText =
         row.fterm || "";

      };

      root.appendChild(div);

   });

}

document
.getElementById(
 "searchBtn"
)
.onclick = ()=>{

    const q =
    document
    .getElementById(
      "search"
    )
    .value
    .toUpperCase();

    document
    .querySelectorAll(
      ".item"
    )
    .forEach(x=>{

       x.classList
       .remove("hit");

       if(
         x.textContent
         .toUpperCase()
         .includes(q)
       ){

          x.classList
           .add("hit");

       }

    });

};

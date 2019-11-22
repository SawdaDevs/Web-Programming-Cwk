$(document).ready(() => {
   $('#id_dob').attr('type', 'date');
    console.log('loaded!!')

    $(".deleteButton").on("click", function(){
        console.log(this.id);
        // const oId = $(this).attr('id');
        // console.log('ither one' +  oId);


        const id = this.id;
        $.ajax({
            url: '{% url deleteItem %}',
            method:"DELETE",
            data: { 'id' : id },
            success: ()=>{
                //redirect back to all page?
                alert("this delete worked")
            },
            error: ()=>{
                alert("this delete for item did not work");
                //stay on page
            }

        })
    })
});